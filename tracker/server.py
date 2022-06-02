#!/usr/bin/env python3

from flask import Flask, request

from redis import Redis
from rq import Queue
from rq.job import Job
from time import strftime

import json
import sys

app = Flask(__name__)

from src import tracker

# Connection to Redis
conn = Redis(host='redis', port=6379)
q = Queue(connection=conn)

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
    callback = request_data['callback']

    job = q.enqueue(tracker.tracker, match_id, id_red, id_blue, video_match, show, callback)
    task = job.get_id()
    result = {
        "Task": task,
        "Time": strftime('%a, %d %b %Y %H:%M:%S')
    }
    return json.dumps({"result":result})

@app.route("/results", methods=['GET'])
def get_results():
    n = len(q.jobs)
    return json.dumps(n)

@app.route("/results/<job_key>", methods=['GET'])
def get_result_job(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return "pending", 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
