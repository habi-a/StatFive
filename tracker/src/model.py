#!/usr/bin/env python3
# pylint: disable=import-error,consider-using-with,wrong-import-position,unspecified-encoding,line-too-long

"""Load Tensorflow object detection"""

import pathlib
import sys

from google.protobuf import text_format

import tensorflow as tf

# Import protos
sys.path.append("./object_detection")
from protos import string_int_label_map_pb2


def load_model(model_name):
    """Load tensorflow model"""
    model_url = 'http://download.tensorflow.org/models/object_detection/' + model_name + '.tar.gz'

    model_dir = tf.keras.utils.get_file(
        fname=model_name,
        origin=model_url,
        untar=True,
        cache_dir=pathlib.Path('.tmp').absolute()
    )
    model = tf.saved_model.load(model_dir + '/saved_model')
    return model


def load_labels(labels_name):
    """Load labels of the model"""
    labels_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
    labels_url += labels_name

    labels_path = tf.keras.utils.get_file(
        fname=labels_name,
        origin=labels_url,
        cache_dir=pathlib.Path('.tmp').absolute()
    )

    labels_file = open(labels_path, 'r')
    labels_string = labels_file.read()

    labels_map = string_int_label_map_pb2.StringIntLabelMap()
    try:
        text_format.Merge(labels_string, labels_map)
    except text_format.ParseError:
        labels_map.ParseFromString(labels_string)

    labels_dict = {}
    for item in labels_map.item:
        labels_dict[item.id] = item.display_name

    return labels_dict
