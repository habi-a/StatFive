#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Python
sudo apt-get install python
sudo apt-get install python-pip python-dev

# OpenCV
sudo apt-get install python-opencv

# Tensorflow
pip install tensorflow

# Tensorflow object detection API
sudo apt-get install -y protobuf-compiler python-pil python-lxml python-tk
pip install --user Cython
pip install --user contextlib2
pip install --user jupyter
pip install --user matplotlib

# Get tensorflow installation path
TENSORFLOW_PATH=$(pip show tensorflow | grep Location | awk '{print $2}')/tensorflow

# Install models
cd $TENSORFLOW_PATH
git clone https://github.com/tensorflow/models

# COCO API
cd /tmp
git clone https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
make
cp -r pycocotools $TENSORFLOW_PATH/models/research/

# Add Libraries to PYTHONPATH
echo "export PYTHONPATH=$PYTHONPATH:$TENSORFLOW_PATH/models/research/:$TENSORFLOW_PATH/models/research/slim" > ~/.bashrc

# Protbuf compilation
cd $TENSORFLOW_PATH/models/research/
protoc object_detection/protos/*.proto --python_out=.

# Get frozen model
cd $DIR
cp -r rsc/ssd_mobilenet_v1_coco_11_06_2017/ $TENSORFLOW_PATH/models/research/object_detection/

# Symbolic link
ln -s $TENSORFLOW_PATH ./
