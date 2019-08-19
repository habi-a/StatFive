FROM debian:stretch

RUN apt-get update -y | apt-get upgrade -y

# Create directory
RUN mkdir -p /app
RUN mkdir -p /tensorflow/models
RUN mkdir -p /tmp/cocoapi

# Python
RUN apt-get install -y python python3
RUN apt-get install -y git python-pip python-dev python3-pip python3-dev
RUN pip install --upgrade pip
RUN pip3 install --upgrade pip

# OpenCV
RUN apt-get install -y python-opencv

# Flask
RUN pip3 install flask flask-restful

# Dependencies API
RUN pip3 install pymysql
RUN pip3 install flask-mysql

# Tensorflow
RUN pip install tensorflow

# Tensorflow object detection API
RUN apt-get install -y protobuf-compiler python-pil python-lxml python-tk
RUN pip install Cython
RUN pip install contextlib2
RUN pip install jupyter
RUN pip install matplotlib

# Tensorflow models
RUN git clone https://github.com/tensorflow/models /tensorflow/models

# COCO API
RUN git clone https://github.com/cocodataset/cocoapi.git /tmp/cocoapi
RUN make /tmp/cocoapi/PythonAPI
RUN cp -r /tmp/cocoapi/PythonAPI/pycocotools /tensorflow/models/research

# Protbuf compilation
WORKDIR /tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
ENV PYTHONPATH $PYTHONPATH:/tensorflow/models/research:/tensorflow/models/research/slim

# Get application source codes
RUN mkdir -p /tensorflow/models/research/object_detection/tracker
COPY ./tracker /tensorflow/models/research/object_detection/tracker
RUN mv /tensorflow/models/research/object_detection/tracker/ssdlite_mobilenet_v2_coco_2018_05_09 /tensorflow/models/research/object_detection
WORKDIR /tensorflow/models/research/object_detection/tracker

# Run API
COPY ./API /app
WORKDIR /app
ENTRYPOINT [ "python3" ]
CMD [ "api.py" ]
