FROM debian:stretch

RUN apt-get update -y | apt-get upgrade -y

# Create directory
RUN mkdir -p /app
RUN mkdir -p /tensorflow/models
RUN mkdir -p /tmp/cocoapi

# Python
RUN apt-get install -y python
RUN apt-get install -y git python-pip python-dev
RUN pip install --upgrade pip

# OpenCV
RUN apt-get install -y python-opencv

# Tensorflow
RUN pip install tensorflow

# Tensorflow object detection API
RUN apt-get install -y protobuf-compiler python-pil python-lxml python-tk
RUN pip install Cython
RUN pip install contextlib2
RUN pip install jupyter
RUN pip install matplotlib
RUN cp -r /usr/local/lib/python2.7/dist-packages/tensorflow

# Tensorflow models
RUN git clone https://github.com/tensorflow/models /tensorflow/models

# COCO API
RUN git clone https://github.com/cocodataset/cocoapi.git /tmp/cocoapi
RUN make /tmp/cocoapi/PythonAPI
RUN cp -r /tmp/cocoapi/PythonAPI/pycocotools /tensorflow/models/research

# Protbuf compilation
WORKDIR /tensorflow/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
ENV PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

# Get application source codes
COPY . /app
RUN cp -r /app/rsc/ssd_mobilenet_v1_coco_11_06_2017 /tensorflow/models/research/object_detection

# Test installation
CMD python object_detection/builders/model_builder_test.py
