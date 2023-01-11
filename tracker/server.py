#!/usr/bin/env python3

"""Micro API for handling analyse requests"""

from time import strftime
import json
from flask import Flask, request
from redis import Redis
from rq import Queue
from rq.job import Job

from src import tracker


app = Flask(__name__)

# Connection to Redis
conn = Redis(host='redis', port=6379)
q = Queue(connection=conn)

@app.route('/')
def hello():
    """Home request"""
    return "Statfive Tracker by habi_a"

@app.route('/analyse', methods=['POST'])
def analyse():
    """Put in a queue analyse request"""
    request_data = request.get_json()
    match_id = request_data['match_id']
    id_red = request_data['id_red']
    id_blue = request_data['id_blue']
    video_match = request_data['video_match']
    show = request_data['show']
    callback = request_data['callback']

    job = q.enqueue(tracker.tracker, args=(match_id, id_red, id_blue, video_match, show, callback), timeout=500)
    task = job.get_id()
    result = {
        "Task": task,
        "Time": strftime('%a, %d %b %Y %H:%M:%S')
    }
    return json.dumps({"result":result})

@app.route("/results", methods=['GET'])
def get_results():
    """Get number of jobs finished in queue"""
    numbers = len(q.jobs)
    return json.dumps(numbers)

@app.route("/results/<job_key>", methods=['GET'])
def get_result_job(job_key):
    """Get results of one job finished in queue"""
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    return "pending", 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
