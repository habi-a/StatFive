#!/usr/bin/env python3

from ball import *


def init_data(match_id, id_red, id_blue):
    data = {
        "result": {
            "id": int(match_id),
            "red": {
                "id": int(id_red),
                "score": 0,
                "possession": 0
            },
            "blue": {
                "id": int(id_blue),
                "score": 0,
                "possession": 0
            }
        }
    }
    return data


def compute_goals(data, already_scored, loc_ball, loc_goal_t1, loc_goal_t2, ball_visible):
    if not already_scored and ball_is_in_the_goal(loc_ball, loc_goal_t1, ball_visible):
        data["result"]["red"]["score"] += 1
        already_scored = True
    elif not already_scored and ball_is_in_the_goal(loc_ball, loc_goal_t2, ball_visible):
        data["result"]["blue"]["score"] += 1
        already_scored = True
    elif already_scored and ball_visible and not ball_is_in_the_goal(loc_ball, loc_goal_t1, ball_visible) and not ball_is_in_the_goal(loc_ball, loc_goal_t2, ball_visible):
        already_scored = False
    return already_scored


def compute_possession(data, team_owner_of_ball):
    data["result"]["red"]["possession"] = get_pourcent_array_occurence(team_owner_of_ball, 'TEAM_1')
    data["result"]["blue"]["possession"] = get_pourcent_array_occurence(team_owner_of_ball, 'TEAM_2')
    return
