FROM --platform=linux/amd64 debian:11

RUN apt-get update -y && apt-get install -y wget gcc g++ make
RUN wget -qO- https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs python
COPY ./ /app
WORKDIR /app
RUN rm -rf node_modules
RUN npm install