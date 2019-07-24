import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs

class AllMatchByDate(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('Select * FROM team_has_match_played')
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'about':'no matchs found'})
        resp = jsonify(rows)
        resp.status_code = 200
        return resp