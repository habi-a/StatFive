#!/usr/bin/env python3

from flask import Flask, request
import sys

app = Flask(__name__)

sys.path.append("./src")
from tracker import *

@app.route('/')
def hello():
    return "Statfive Tracker by habi_a"

@app.route('/analyse', methods=['POST'])
def analyse():
    request_data = request.get_json()
    match_id = request_data['match_id']
    id_red = request_data['id_red']
    id_blue = request_data['id_blue']
    video_match = request_data['video_match']
    show = request_data['show']
    return tracker(match_id, id_red, id_blue, video_match, show)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)