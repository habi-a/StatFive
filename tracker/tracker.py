#!/usr/bin/env python

from __future__ import division
import numpy as np
import os
import six.moves.urllib as urllib
import requests
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from PIL import Image
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
OBJECT_DETECTION_PATH = '/tensorflow/models/research/object_detection/'
sys.path.append(OBJECT_DETECTION_PATH)

from utils import label_map_util
from utils import visualization_utils as vis_util


# Command-line argument
if len(sys.argv != 2):
  print("Match id needed")
  sys.exit(0)
match_id = sys.argv[1]

# HTTP Request info (To submit chronos)
SERVER_URL = 'http://localhost:5000'
API_ENDPOINT = '/team/results'
data = {
  "result": {
    "id": match_id, 
    "red": {
      "score": 0,
      "possession": 50
    },
    "blue": {
      "score": 0,
      "possession": 50
    }
  }
}

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
PATH_TO_CKPT = OBJECT_DETECTION_PATH + MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = OBJECT_DETECTION_PATH + 'data/mscoco_label_map.pbtxt'

NUM_CLASSES = 90


# Load model
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

# Load labels
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def count_nonblack_np(img):
  """Return the number of pixels in img that are not black.
  img must be a Numpy array with colour values along the last axis.

  """
  return img.any(axis=-1).sum()

def detect_team(image, show = False):
  # define the list of boundaries
  i = 0
  boundaries = [
    ([17, 15, 100], [50, 56, 200]), #red
    ([86, 31, 4], [220, 88, 50]) #blue
  ]

  for (lower, upper) in boundaries:
    ## create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    ## find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    tot_pix = count_nonblack_np(image)
    color_pix = count_nonblack_np(output)

    ratio = color_pix/tot_pix
    if ratio > 0.01 and i == 0:
      return 'red'
    elif ratio > 0.01 and i == 1:
      return 'blue'

    i += 1

    ## for debugging
#    if show == True:
#      cv2.imshow("images", np.hstack([image, output]))
#      if cv2.waitKey(0) & 0xFF == ord('q'):
#        cv2.destroyAllWindows()
  return 'not_sure'


# Functions to find who scored
def ball_is_in_the_goal(loc_ball, loc_goal, ball_visible):
  if not ball_visible:
    return False
  
  if loc_ball[0] > loc_goal['xmin'] and loc_ball[0] < loc_goal['xmax'] and loc_ball[1] > loc_goal['ymin'] and loc_ball[1] < loc_goal['ymax']:
    return True
  return False
  

# Functions to find owner of ball
def distance(pt_1, pt_2):
  pt_1 = np.array((pt_1[0], pt_1[1]))
  pt_2 = np.array((pt_2[0], pt_2[1]))
  return np.linalg.norm(pt_1-pt_2)
def closest_node(node, nodes):
  pt = []
  dist = 9999999
  for n in nodes:
    if distance(node, n) <= dist:
      dist = distance(node, n)
      pt = n
  return pt
def find_team_nearest_ball(loc_ball, loc_foot):
  closest_coord = closest_node(loc_ball, loc_foot)
  for x, y, team in loc_foot:
    if x == closest_coord[0] and y == closest_coord[1]:
      return team
  return 'TEAM_1'

def get_pourcent_array_occurence(array, element):
  return array.count(element) / len(array) * 100


# [Debug] to view Color Mask
filename = './five-a-side.jpg'
image = cv2.imread(filename)
resize = cv2.resize(image, (640,360))
detect_team(resize, show=True)


# Video Recorder
fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
out = cv2.VideoWriter('./soccer_out.avi', fourcc, 10, (640,360))
filename = './five-a-side.mp4'
cap = cv2.VideoCapture(filename)


# Init stats
team_owner_of_ball = []
already_scored = False



# Running the tensorflow session
with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    counter = 0
    while (True):
      ret, image_np = cap.read()
      counter += 1
      if ret:
        h = image_np.shape[0]
        w = image_np.shape[1]

      if not ret:
        break
      if counter % 1 == 0:
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        
        # Each box represents a part of the image where a particular object was detected.
        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = detection_graph.get_tensor_by_name('detection_scores:0')
        classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        # Actual detection.
        (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=3,
          min_score_thresh=0.6)

        frame_number = counter

        # Variables helper stats
        loc = {}
        loc_ball = []
        loc_foot = []
        ball_visible = False

        # Position goals
        loc_goal_t1 = {}
        loc_goal_t2 = {}
        loc_goal_t1['ymin'] = int(h * 0.22)
        loc_goal_t1['xmin'] = int(w * 0.46)
        loc_goal_t1['ymax'] = int(h * 0.255)
        loc_goal_t1['xmax'] = int(w * 0.53)
        loc_goal_t2['ymin'] = int(h * 0.75)
        loc_goal_t2['xmin'] = int(w * 0.01)
        loc_goal_t2['ymax'] = int(h * 1)
        loc_goal_t2['xmax'] = int(w * 0.92)

        for n in range(len(scores[0])):
          if scores[0][n] > 0.50:
            # Calculate position
            ymin = int(boxes[0][n][0] * h)
            xmin = int(boxes[0][n][1] * w)
            ymax = int(boxes[0][n][2] * h)
            xmax = int(boxes[0][n][3] * w)
            yaverage = int((ymin + ymax) / 2)
            xaverage = int((xmin + xmax) / 2)

            # Find label corresponding to that class
            for cat in categories:
              if cat['id'] == classes[0][n]:
                label = cat['name']

              ## Extract every item
              if label == 'person':
                ### Crop them
                crop_img = image_np[ymin:ymax, xmin:xmax]
                color = detect_team(crop_img)
                if color != 'not_sure':
                  coords = (xmin, ymin)
                  if color == 'red':
                    loc[coords] = 'TEAM_1'
                    loc_foot.append((xaverage, ymax, 'TEAM_1'))
                  else:
                    loc[coords] = 'TEAM_2'
                    loc_foot.append((xaverage, ymax, 'TEAM_2'))
                  #### Draw foot boxes
                  cv2.rectangle(image_np, (xmin, yaverage), (xmax, ymax), (238, 120, 42), 2)
              
              if label == 'sports ball':
                loc_ball = ((xaverage, yaverage))
                ball_visible = True


        # Print color next to the person
        for key in loc.keys():
          text_pos = str(loc[key])
          cv2.putText(image_np, text_pos, (key[0], key[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0), 2) # Text in black

        # Find the team in possession of the ball 
        if ball_visible == True:
          team_owner_of_ball.append(find_team_nearest_ball(loc_ball, loc_foot))
        else:
          ## Take the latest team seen with the ball
          if team_owner_of_ball:
            team_owner_of_ball.append(team_owner_of_ball[-1])

        # Draw goals
        cv2.rectangle(image_np, (loc_goal_t1['xmin'], loc_goal_t1['ymin']), (loc_goal_t1['xmax'], loc_goal_t1['ymax']), (255, 153, 255), 2)
        cv2.rectangle(image_np, (loc_goal_t2['xmin'], loc_goal_t2['ymin']), (loc_goal_t2['xmax'], loc_goal_t2['ymax']), (255, 153, 255), 2)

        # Detect if there is a goal
        if not already_scored and ball_is_in_the_goal(loc_ball, loc_goal_t1, ball_visible):
          data["result"]["blue"]["score"] += 1
          already_scored = True
        elif not already_scored and ball_is_in_the_goal(loc_ball, loc_goal_t2, ball_visible):
          data["result"]["red"]["score"] += 1
          already_scored = True
        elif already_scored and ball_visible and not ball_is_in_the_goal(loc_ball, loc_goal_t1, ball_visible) and not ball_is_in_the_goal(loc_ball, loc_goal_t2, ball_visible):
          already_scored = False


#      cv2.imshow('image', image_np)
#      out.write(image_np)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break

# Calcul stats
data["result"]["red"]["possession"] = get_pourcent_array_occurence(team_owner_of_ball, 'TEAM_1')
data["result"]["blue"]["possession"] = get_pourcent_array_occurence(team_owner_of_ball, 'TEAM_2')

# Print stats
print('Score:')
print('RedTeam', data["result"]["red"]["score"], '-', data["result"]["blue"]["score"], 'BlueTeam')
print()
print('Possession:')
print('RedTeam', int(round(data["result"]["red"]["possession"])), '% -', int(round(data["result"]["blue"]["possession"])), '% BlueTeam')

# Send stats
print("[HTTP] Sending data...")
resp = requests.post(SERVER_URL + API_ENDPOINT, data = data)
