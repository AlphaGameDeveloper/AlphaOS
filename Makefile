docker:
	@echo current build $ct, time is $tm
	docker build -t alphagamedev/damienos --build-arg TIME="$$(date)" --build-arg BUILD="$$(cat build/buildct)" .

incriment_build:
	@build_number=$$(cat build/buildct); \
	new_build_number=$$((build_number + 1)); \
	echo "$$new_build_number" > build/buildct
	@echo "This is build number $$(cat build/buildct)"

banner: incriment_build
	@cat tools/aos_ascii_art.txt
	
rm:
	docker container rm damienos -f

run: banner rm docker container

container:
	docker run --rm -it --name damienos alphagamedev/damienos

small: banner rm
	docker run --rm -it --name damienos -v .:/docker/ -v ./configs:/data/.config alphagamedev/damienos

setupWorkspace: banner
	mkdir build
	echo "1" > build/buildct
