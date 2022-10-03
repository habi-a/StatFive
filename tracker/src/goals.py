#!/usr/bin/env python3

"""Goals definitions"""

def define_goals(width, height):
    """Define goalss"""
    goal_t1 = {
        "x1": int(width * 0.01),
        "y1": int(height * 0.69),
        "x2": int(width * 0.95),
        "y2": int(height)
    }
    goal_t2 = {
        "x1": int(width * 0.45),
        "y1": int(height * 0.22),
        "x2": int(width * 0.54),
        "y2": int(height * 0.26)
    }
    return goal_t1, goal_t2
