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
        cursor.execute("SELECT name FROM team")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        if not rows:
            return jsonify({'about':'no teams found'})
        resp.status_code = 200
        return resp

class averageTeam(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT team.name, CAST(ROUND(AVG(team_has_match_played.goals)) AS INT) AS `moyenne_goal`, ROUND(AVG(team_has_match_played.possesion)) AS `moyenne_possesion` FROM team INNER JOIN team_has_match_played ON team_has_match_played.team_id = team.id GROUP BY team.name")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        if not rows:
            return jsonify({'about':'no teams found'})
        resp.status_code = 200
        return resp

class createTeam(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('red', type=dict, location='json')
        parser.add_argument('blue', type=dict, location='json')
        args = parser.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlRed = 'INSERT INTO `team`(`name`) VALUES({})'.format(args['red']['name'])
        sqlBlue = 'INSERT INTO `team`(`name`) VALUES({})'.format(args['blue']['name'])
        cursor.execute(sqlRed)
        cursor.execute(sqlBlue)
        conn.commit()
        return jsonify({'Teams':'created'})

class teamById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM team WHERE id ={}').format(id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class teamByName(Resource):
    def get(self, name):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM team WHERE name LIKE %s", name+'%')
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
