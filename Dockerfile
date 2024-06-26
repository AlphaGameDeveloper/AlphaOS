FROM python:3.8

WORKDIR /docker

RUN apt update && apt install nano wget whiptail lynx -y

COPY requirements.txt /docker

RUN /usr/local/bin/python3 -m pip install -r /docker/requirements.txt

ARG BUILD=unknown

ARG TIME=unknown

RUN echo "$BUILD" > /buildct && echo "$TIME" > /buildtm

COPY . /docker

RUN mkdir /data && mv /docker/configs /data/.config

WORKDIR /data

CMD [ "/usr/local/bin/python3", "/docker/main.py", "--inContainer=TRUE" ]
