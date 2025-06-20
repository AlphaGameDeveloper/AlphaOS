# AlphaOS Makefile — cross-platform ISO builder with PyInstaller
PROJECT=AlphaOS
ALPINE_VER=3.18.4
PYTHON_VER=3.8.18-r0
ARCH=x86_64
ROOTFS_DIR=build/rootfs
ISO_DIR=build/iso
DOWNLOADS=build/downloads
OUT_ISO=build/$(PROJECT).iso
ALPINE_TARBALL=$(DOWNLOADS)/alpine-minirootfs-$(ALPINE_VER)-$(ARCH).tar.gz

# PyInstaller config
PYINSTALLER_BUILD=build/pybin
MAIN_SCRIPT=main.py  # Change this to your actual main script

# Detect OS (Mac or Linux)
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	SUDO := 
	MOUNT_CMD := gsudo mount
	GRUB_RESCUE := grub-mkrescue
	QEMU_CMD := qemu-system-x86_64
else
	SUDO := sudo
	MOUNT_CMD := sudo mount --bind
	GRUB_RESCUE := grub-mkrescue
	QEMU_CMD := qemu-system-x86_64
endif

# Docker common args for all commands
DOCKER_COMMON_ARGS=--rm

# Define a shell macro to run docker with optional image (defaults to ubuntu:22.04)
define DOCKER_RUN
	$(if $(2), \
		docker run $(DOCKER_COMMON_ARGS) --privileged -v "$(PWD)":/alphaos -w /alphaos $(2) sh -xc $(1), \
		docker run $(DOCKER_COMMON_ARGS) --privileged -v "$(PWD)":/alphaos -w /alphaos ubuntu:22.04 bash -xc $(1))
endef

.PHONY: all download extract chroot setup-kernel setup-initramfs pyinstaller-build copy-assets setup-iso build-iso test clean

all: $(OUT_ISO)

$(ALPINE_TARBALL):
	mkdir -p $(DOWNLOADS)
	wget -O $@ https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/$(ARCH)/alpine-minirootfs-$(ALPINE_VER)-$(ARCH).tar.gz

download: $(ALPINE_TARBALL)

extract:
	rm -rf $(ROOTFS_DIR)
	mkdir -p $(ROOTFS_DIR)
	@echo "Extracting Alpine rootfs..."
	$(call DOCKER_RUN,"\
		apt update >/dev/null && apt install -y tar rsync >/dev/null && \
		mkdir -p /tmp/rootfs && \
		tar --no-same-owner --no-same-permissions -xzf $(ALPINE_TARBALL) -C /tmp/rootfs && \
		rm -rf $(ROOTFS_DIR) && \
		mkdir -p $(ROOTFS_DIR) && \
		rsync -a --no-perms --no-owner --no-group /tmp/rootfs/ $(ROOTFS_DIR)/")

chroot:
	@echo "Preparing chroot environment inside Docker container..."
	$(call DOCKER_RUN,"\
		apt update >/dev/null && apt install -y mount && \
		cp /etc/resolv.conf $(ROOTFS_DIR)/etc/ && \
		mount --bind /dev $(ROOTFS_DIR)/dev && \
		umount $(ROOTFS_DIR)/dev")

setup-kernel:
	@echo "Installing kernel inside a real chroot..."
	docker run $(DOCKER_COMMON_ARGS) --privileged \
		-v "$(PWD)/$(ROOTFS_DIR)":/mnt \
		alpine:3.18 sh -xc "\
			mkdir -p /mnt/etc/apk && \
			echo 'http://dl-cdn.alpinelinux.org/alpine/v3.18/main' > /mnt/etc/apk/repositories && \
			echo 'http://dl-cdn.alpinelinux.org/alpine/v3.18/community' >> /mnt/etc/apk/repositories && \
			apk update && apk add --no-cache util-linux && \
			mount -t proc none /mnt/proc && \
			mount --rbind /sys /mnt/sys && mount --make-rslave /mnt/sys && \
			mount --rbind /dev /mnt/dev && mount --make-rslave /mnt/dev && \
			chroot /mnt /bin/sh -c 'apk update && apk add linux-lts && ls -la /lib/modules' && \
			umount -l /mnt/proc && umount -l /mnt/sys && umount -l /mnt/dev"

setup-initramfs:
	@KVER=$$(docker run $(DOCKER_COMMON_ARGS) -v "$(PWD)/$(ROOTFS_DIR)":/mnt alpine:3.18 sh -c "ls /mnt/lib/modules | head -n 1"); \
	if [ -z "$$KVER" ]; then \
		echo "No kernel modules found. Cannot build initramfs."; exit 1; \
	fi; \
	echo "Kernel version found: $$KVER"; \
	docker run $(DOCKER_COMMON_ARGS) --privileged \
		-v "$(PWD)/$(ROOTFS_DIR)":/mnt \
		alpine:3.18 sh -c "\
			mkdir -p /mnt/etc/apk && \
			echo 'http://dl-cdn.alpinelinux.org/alpine/v3.18/main' > /mnt/etc/apk/repositories && \
			echo 'http://dl-cdn.alpinelinux.org/alpine/v3.18/community' >> /mnt/etc/apk/repositories && \
			mount -t proc none /mnt/proc && \
			mount --rbind /sys /mnt/sys && mount --make-rslave /mnt/sys && \
			mount --rbind /dev /mnt/dev && mount --make-rslave /mnt/dev && \
			chroot /mnt /bin/sh -c \"ls -l /lib/modules/$$KVER && apk update && apk add mkinitfs && mkinitfs $$KVER\" && \
			umount -l /mnt/proc && umount -l /mnt/sys && umount -l /mnt/dev"

pyinstaller-build:
	rm -rf $(PYINSTALLER_BUILD)
	mkdir -p $(PYINSTALLER_BUILD)
	@echo "Compiling Python scripts with PyInstaller..."
	$(call DOCKER_RUN,"\
		apk add --no-cache binutils && \
		pip install pyinstaller >/dev/null && \
		pyinstaller --onefile $(MAIN_SCRIPT) --distpath $(PYINSTALLER_BUILD)", python:3.8-alpine)

copy-assets: setup-initramfs pyinstaller-build
	$(call DOCKER_RUN,"rm -f $(ROOTFS_DIR)/sbin/init && cp init $(ROOTFS_DIR)/sbin/init")
	mkdir -p $(ROOTFS_DIR)/opt/alphaos/
	cp $(PYINSTALLER_BUILD)/* $(ROOTFS_DIR)/opt/alphaos/
	mkdir -p $(ROOTFS_DIR)/etc/alphaos/
	cp -r configs/* $(ROOTFS_DIR)/etc/alphaos/
	mkdir -p $(ROOTFS_DIR)/usr/share/doc/alphaos/
	cp -r documents/* $(ROOTFS_DIR)/usr/share/doc/alphaos/
	mkdir -p $(ROOTFS_DIR)/opt/alphaos/tools/
	cp -r tools/* $(ROOTFS_DIR)/opt/alphaos/tools/
	cp requirements.txt $(ROOTFS_DIR)/opt/alphaos/

setup-iso: copy-assets
	rm -rf $(ISO_DIR)
	mkdir -p $(ISO_DIR)/boot/grub
	cp -a $(ROOTFS_DIR)/* $(ISO_DIR)/
	cp $(ROOTFS_DIR)/boot/vmlinuz-lts $(ISO_DIR)/boot/vmlinuz
	cp $(ROOTFS_DIR)/boot/initramfs-* $(ISO_DIR)/boot/
	@echo "set default=0\nset timeout=5\nmenuentry \"AlphaOS\" {\n linux /boot/vmlinuz root=/dev/sr0 quiet\n initrd /boot/initramfs-lts\n}" > $(ISO_DIR)/boot/grub/grub.cfg

build-iso:
	$(call DOCKER_RUN,"apk add --no-cache grub xorriso && grub-mkrescue -o build/AlphaOS.iso build/iso --modules='normal part_msdos ext2 multiboot efi fat iso9660' --compress=xz", alpine:3.18)

test:
	$(QEMU_CMD) -cdrom $(OUT_ISO) -m 512M -nographic

clean:
	rm -rf build

$(OUT_ISO): download extract chroot setup-kernel setup-initramfs pyinstaller-build copy-assets setup-iso build-iso
