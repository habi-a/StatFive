#!/usr/bin/env python3
 
import math

from src.ball import *
from src.teams import *


def draw_detections_on_image(image, detections, labels, goal_t1, goal_t2, loc, loc_foot, loc_ball, ball_visible, show):
    image_with_detections = image
    height, width, channels = image_with_detections.shape

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 255, 0)
    label_padding = 5

    num_detections = detections['num_detections']
    if num_detections > 0:
        for detection_index in range(num_detections):
            detection_score = detections['detection_scores'][detection_index]
            detection_box = detections['detection_boxes'][detection_index]
            detection_class = detections['detection_classes'][detection_index]
            detection_label = labels[detection_class]
            detection_label_full = detection_label + ' ' + str(math.floor(100 * detection_score)) + '%'

            x1 = int(width * detection_box[1])
            y1 = int(height * detection_box[0])
            x2 = int(width * detection_box[3])
            y2 = int(height * detection_box[2])

            coords = (x1, y1)
            yaverage = int((y1 + y2) / 2)
            xaverage = int((x1 + x2) / 2)
            
            detect_team_on_image(image_with_detections, detection_label, x1, x2, y1, y2, loc, loc_foot, xaverage)
            detect_ball_on_image(detection_label, loc_ball, ball_visible, xaverage, yaverage)

            if loc[coords] != "not_sure" and show:
                image_with_detections = cv2.rectangle(
                    image_with_detections,
                    (x1, y1),
                    (x2, y2),
                    color,
                    3
                )
  
                # Draw feet
                image_with_detections = cv2.rectangle(
                    image_with_detections,
                    (x1, yaverage),
                    (x2, y2),
                    (238, 120, 42),
                    2
                )

                # Label text.
                cv2.putText(
                    image_with_detections,
                    detection_label_full,
                    (x1 + label_padding, y1 - label_padding),
                    font,
                    0.6,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA
                )

                # Team text.
                cv2.putText(
                    image_with_detections,
                    loc[coords],
                    (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.50, 
                    (255, 0, 0), 
                    2
                )

    if show:
        # Draw goal 1
        image_with_detections = cv2.rectangle(
            image_with_detections,
            (goal_t1["x1"], goal_t1["y1"]),
            (goal_t1["x2"], goal_t1["y2"]),
            (238, 120, 42),
            2
        )

        # Draw goal 2
        image_with_detections = cv2.rectangle(
            image_with_detections,
            (goal_t2["x1"], goal_t2["y1"]),
            (goal_t2["x2"], goal_t2["y2"]),
            (238, 120, 42),
            2
        )

    return image_with_detections
