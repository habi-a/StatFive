FROM tensorflow/tensorflow:2.7.1

# Install Python, Flask & Redis
RUN apt-get update
RUN apt-get install -y git python3-opencv unzip redis-server
RUN pip3 install --upgrade pip
RUN pip3 install flask requests redis rq

# Tensorflow models
RUN git clone https://github.com/tensorflow/models /tensorflow/models
COPY . /app
RUN mkdir /app/.tmp
WORKDIR /app
RUN mv /tensorflow/models/research/object_detection /app

# Protbuf compilation
RUN curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protoc-3.19.4-linux-x86_64.zip 
RUN unzip -o protoc-3.19.4-linux-x86_64.zip -d .tmp/protoc
RUN rm -f protoc-3.19.4-linux-x86_64.zip
RUN .tmp/protoc/bin/protoc object_detection/protos/*.proto --python_out=.

ENV FLASK_APP=server
ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "python3", "server.py" ]