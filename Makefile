docker:
#	ct=$(cat build/buildct)
#	((ct++))
#	echo "$ct" > build/buildct
#	tm=$(date)
	docker build -t alphagamedev/damienos .

rm:
	docker container rm damienos -f

run: rm docker container

container:
	docker run --rm -it --name damienos alphagamedev/damienos

small: rm
	docker run --rm -it --name damienos -v .:/docker/ -v ./configs:/data/.config alphagamedev/damienos

setupWorkspace:
	mkdir build
	echo "1" > build/buildct
	echo "$(date)" > build/buildtm
