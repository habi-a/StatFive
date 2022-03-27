FROM debian:11

# Create Workdir
COPY . /app
RUN mkdir -p /app/.tmp
WORKDIR /app

RUN apt-get update -y | apt-get upgrade -y

# Install Python and Virtual Env
RUN apt-get install -y python3 python3-pip python3-dev python3-venv protobuf-compiler python3-pil python3-lxml python3-tk git
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install --upgrade pip

# Install Tensorflow
RUN apt-get install -y python3-opencv
RUN pip3 install tensorflow
RUN pip3 install Cython
RUN pip3 install requests

# Protbuf compilation
RUN curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protoc-3.19.4-osx-x86_64.zip
RUN unzip -o $PROTOC_ZIP -d .tmp/protoc
RUN rm -f protoc-3.19.4-osx-x86_64.zip
RUN .tmp/protoc/bin/protoc ./protos/*.proto --python_out=.
