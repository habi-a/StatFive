#!/usr/bin/env python3

from src.color import *


def detect_team_on_image(image, detection_label, x1, x2, y1, y2, loc, loc_foot, xaverage):
    coords = (x1, y1)

    if detection_label == "person":
        crop_img = image[y1:y2,x1:x2]
        color = detect_color(crop_img)
        if color == "red" :
            loc[coords] = 'TEAM_1'
            loc_foot.append((xaverage, y2, 'TEAM_1'))
        elif color == "blue" :
            loc[coords] = 'TEAM_2'
            loc_foot.append((xaverage, y2, 'TEAM_2'))
        elif color == "not_sure":
            loc[coords] = 'not_sure'
    else:
        loc[coords] = ""
    return
