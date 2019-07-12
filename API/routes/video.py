import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
import werkzeug, os

class postVideo(Resource):
    def post(self):
        destpath="/mnt/c/Users/nour/Documents/ProjetLib/Git/StatFive/video"
        parser = reqparse.RequestParser()
        parser.add_argument('video', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        if args:
            video = args['video']
            filename = "myMatch.mp4"
            print(video)
            video.save(os.path.join(destpath,filename))
            return jsonify({'about':'Uploaded'})
        else:
            print(args['video'])
            return args
