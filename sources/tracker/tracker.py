#!/usr/bin/env python3

import cv2
import os
import platform
import requests
import sys
import tensorflow as tf

# Import local functions
sys.path.append("src")
from ball import *
from draw import *
from goals import *
from model import *
from objects import *
from stats import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


if __name__ == '__main__':

    # Args variables
    if len(sys.argv) != 6:
        print("Usage: tracker.py <match_id> <red_id> <blue_id> <path_video> <send_data>")
        sys.exit(0)

    match_id = sys.argv[1]
    id_red = sys.argv[2]
    id_blue = sys.argv[3]
    video_match = str(sys.argv[4])
    send_data = sys.argv[5]

    # HTTP Request info (To submit results)
    SERVER_URL = 'https://api.statfive.fr/api/'
    API_ENDPOINT = 'match/result'

    # Video Recorder
    filename = video_match
    cap = cv2.VideoCapture(filename)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    out = cv2.VideoWriter(OBJECT_DETECTION_PATH + 'tracker/video/match' + match_id + '.avi', fourcc, 10, (width, height))
    goal_t1, goal_t2 = define_goals(width, height)
    data = init_data(match_id, id_red, id_blue)
    team_owner_of_ball = []
    already_scored = False

    # Loading model
    MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
    saved_model = load_model(MODEL_NAME)

    # Loading default model signature and labels.
    model = saved_model.signatures['serving_default']
    LABELS_NAME = 'mscoco_label_map.pbtxt'
    labels = load_labels(LABELS_NAME)

    # Print versions
    print('Python version:', platform.python_version())
    print('Tensorflow version:', tf.__version__)
    print('Keras version:', tf.keras.__version__)

    # Main loop
    while (True):
        loc = {}
        loc_ball = { "ref": () }
        loc_foot = []
        ball_visible = { "ref": False }
        ret, image_np = cap.read()

        if not ret:
            break
        detections = detect_objects_on_image(image_np, model)
        image_with_detections = draw_detections_on_image(image_np, detections, labels, goal_t1, goal_t2, loc, loc_foot, loc_ball, ball_visible)
        already_scored = compute_goals(data, already_scored, loc_ball, goal_t1, goal_t2, ball_visible)
        team_owner_of_ball = find_possession_ball(team_owner_of_ball, loc_ball["ref"], loc_foot, ball_visible)

        cv2.imshow('image', image_with_detections)
        out.write(image_with_detections)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    compute_possession(data, team_owner_of_ball)
    print(data)

    # Send stats
    if send_data == 1:
        print("[HTTP] Sending data...")
        resp = requests.post(SERVER_URL + API_ENDPOINT, data = data)
