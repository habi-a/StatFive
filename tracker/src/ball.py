#!/usr/bin/env python3
# pylint: disable=invalid-name

"""Ball Module"""

import numpy as np


def ball_is_in_the_goal(loc_ball, loc_goal, ball_visible):
    """Function to check if ball is inside the goal"""
    if not ball_visible["ref"]:
        return False
    if (loc_ball["ref"][0] > loc_goal['x1'] and loc_ball["ref"][0] < loc_goal['x2'] and
            loc_ball["ref"][1] > loc_goal['y1'] and loc_ball["ref"][1] < loc_goal['y2']):
        return True
    return False


def distance(pt_1, pt_2):
    """Function to compute distance"""
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)


def closest_node(node, nodes):
    """Function to find the closest element of an other element"""
    pattern = []
    dist = 9999999
    for n in nodes:
        if distance(node, n) <= dist:
            dist = distance(node, n)
            pattern = n
    return pattern


def find_team_nearest_ball(loc_ball, loc_foot):
    """Function to find the team closest the the ball"""
    closest_coord = closest_node(loc_ball, loc_foot)
    for x, y, team in loc_foot:
        if x == closest_coord[0] and y == closest_coord[1]:
            return team
    return 'TEAM_1'


def get_pourcent_array_occurence(array, element):
    """Function to compute ball possession"""
    return array.count(element) / len(array) * 100


def detect_ball_on_image(label, loc_ball, ball_visible, xaverage, yaverage):
    """Function to find ball in an image"""
    if label == 'sports ball':
        loc_ball["ref"] = ((xaverage, yaverage))
        ball_visible["ref"] = True


def find_possession_ball(team_owner_of_ball, loc_ball, loc_foot, ball_visible):
    """Function to find the team which has the ball"""
    if ball_visible["ref"] is True:
        team_owner_of_ball.append(find_team_nearest_ball(loc_ball, loc_foot))
    elif team_owner_of_ball:
        team_owner_of_ball.append(team_owner_of_ball[-1])
    return team_owner_of_ball
