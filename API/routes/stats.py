import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs

class StatUserById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('Select mail, name, firstname, stats.kilometre, stats.passe, stats.but FROM users INNER JOIN stats ON user_id = {}').format(id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class AllStatUser(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT users.firstname, users.lastname, stats.kilometre, stats.passe, stats.but stats.date FROM users RIGHT OUTER JOIN stats ON stats.user_id = users.id')
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class AllStatTeam(Resource):
    def get(self):
         conn = mysql.connect()
         cursor = conn.cursor(pymysql.cursors.DictCursor)
         cursor.execute('SELECT * FROM team RIGHT OUTER JOIN team_stats ON team.id = team_stats.team_id')
         rows = cursor.fetchall()
         resp = jsonify(rows)
         resp.status_code = 200
         return resp

class StatTeamById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT team.name, team_stats.but, team_stats.passe, team_stats.km, team_stats.possesion, team_stats.date FROM team INNER JOIN team_stats ON team_stats.team_id=team.id AND team.id={} ORDER BY team_stats.date'.format(id)
        cursor.execute(sql)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class StatTeam(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('result', type=dict, location='json')
        args = parser.parse_args()
        
        return args