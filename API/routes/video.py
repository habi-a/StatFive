import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs

class postVideo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('result', type=dict, location='json')
        args = parser.parse_args()
        return args