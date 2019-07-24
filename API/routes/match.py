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
        cursor.execute('SELECT team_has_match_played.goals, team_has_match_played.possesion, team_has_match_played.color, team.name, match_played.duration FROM team_has_match_played INNER JOIN match_played ON team_has_match_played.match_id = match_played.id INNER JOIN team ON team_has_match_played.team_id = team.id')
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'about':'no matchs found'})
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

#Recuperer le dernier id s
#cursor.lastrowid