FROM  ubuntu:bionic

RUN adduser stat_five_api

WORKDIR /home/stat_five_api

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python3.7 python3-pip python3.7-venv python3-dev python3.7-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev libmysqlclient-dev

COPY requirements.txt requirements.txt
RUN python3.7 -m venv venv
RUN venv/bin/pip3 install wheel
RUN  venv/bin/pip3 install -r requirements.txt

COPY . ./
RUN chmod +x boot.sh

RUN chown -R stat_five_api:stat_five_api ./
USER stat_five_api

ENTRYPOINT ["bash", "./boot.sh"]
