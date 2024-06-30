docker:
#	ct=$(cat build/buildct)
#	ctx=$((ct + 1))
#	echo "$ct" > build/buildct
#	echo $ct $ctx
	@echo current build $ct, time is $tm
	docker build -t alphagamedev/damienos --build-arg TIME="$(time)" .

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
