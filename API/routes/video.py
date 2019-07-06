import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
import werkzeug 

class postVideo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        #parser.add_argument('video', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('red', type=dict, location='json')
        parser.add_argument('blue', type=dict, location='json')
        args = parser.parse_args()
        print(args)
        return args
