FROM --platform=linux/amd64 debian:11

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python3 python3-pip python3-venv python3-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev default-libmysqlclient-dev

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip3 install wheel
RUN venv/bin/pip3 install -r requirements.txt

COPY . ./
RUN chmod +x boot.sh

ENTRYPOINT ["bash", "./boot.sh"]
