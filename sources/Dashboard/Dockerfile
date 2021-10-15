FROM debian:buster

RUN apt-get update -y && apt-get install -y wget gcc g++ make
RUN wget -qO- https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs
COPY ./ /app
WORKDIR /app
RUN npm install