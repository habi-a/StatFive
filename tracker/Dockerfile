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
COPY . /tensorflow/models/research/object_detection/tracker
RUN mv /tensorflow/models/research/object_detection/tracker/ssdlite_mobilenet_v2_coco_2018_05_09 /tensorflow/models/research/object_detection
WORKDIR /tensorflow/models/research/object_detection/tracker

# Install Jupyter Notebook
RUN jupyter notebook --generate-config --allow-root
RUN echo "c.NotebookApp.password = u'sha1:3b8bc52d8df6:90f9ce15265259a7be39faeca36fd0cc4c7a98bd'" >> /root/.jupyter/jupyter_notebook_config.py
EXPOSE 8888
CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/tensorflow/models/research/object_detection/tracker", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
