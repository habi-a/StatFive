import pymysql
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL

class allTeam(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM team")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class createTeam(Resource):
    def post(self):
        return jsonify({'insert':'team'})

class Stats(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT team.name, team_stats.but, team_stats.passe, team_stats.km, team_stats.possesion, team_stats.date FROM team INNER JOIN team_stats ON team_stats.team_id=team.id AND team.id="+ id +"ORDER BY team_stats.date DES"
        cursor.execute(sql)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
