import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs

class Json():
    #method to create json for one match
    def create(self, datas):
        fake = []
        final = []
        i = 0
        while i < len(datas):
            new_data = { 
                'match_id' : datas[i]['match_id'],
                'match_name' : datas[i]['match_name'],
                'durée' : datas[i]['duration'],
                datas[i]['color']:{
                        'team_name' : datas[i]['name'],
                        'goals' : datas[i]['goals'],
                        'possesion' : datas[i]['possesion']
                }
            }
            fake.append(new_data)
            i+=1
        #Parse premiere list
        i = 0
        j = i+1
        while i < len(fake):
            if fake[i]['match_id'] == fake[i+1]['match_id']:
                dico1 = fake[i]
                dico2 = fake[i+1]
                dico1.update(dico2)
                final.append(dico1)
                i += 1
            i+=1
        return final

class StatUserById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('Select mail, name, firstname, stats.kilometre, stats.passe, stats.but FROM users INNER JOIN stats ON user_id = {}').format(id)
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'about':'no stats found for this user'})
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class AllStatUser(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT users.firstname, users.lastname, stats.kilometre, stats.passe, stats.but stats.date FROM users RIGHT OUTER JOIN stats ON stats.user_id = users.id')
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'about':'no stats users found'})
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class AllStatTeam(Resource):
    def get(self):
         conn = mysql.connect()
         cursor = conn.cursor(pymysql.cursors.DictCursor)
         cursor.execute('SELECT * FROM team RIGHT OUTER JOIN team_stats ON team.id = team_stats.team_id')
         rows = cursor.fetchall()
         if not rows:
            return jsonify({'about':'no stats found'})
         resp = jsonify(rows)
         resp.status_code = 200
         return resp

class StatTeamById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT team.name, team_stats.but, team_stats.passe, team_stats.km, team_stats.possesion FROM team INNER JOIN team_stats ON team_stats.team_id=team.id AND team.id={}'.format(id)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'about':'no stats found'})
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class statMatchById(Resource):
    def get(self, id):
        parsing = Json()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT team_has_match_played.match_id ,team_has_match_played.goals, team_has_match_played.possesion, team_has_match_played.color, team.name, match_played.duration, match_played.name AS `match_name` FROM team_has_match_played INNER JOIN match_played ON team_has_match_played.match_id = match_played.id INNER JOIN team ON team_has_match_played.team_id = team.id WHERE team_has_match_played.match_id ={}'.format(id)
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        match = parsing.create(rows)
        print(match)
        if not rows:
            return jsonify({'about':'no match found'})
        resp = jsonify(match)
        resp.status_code = 200
        return resp

class addStatTeam(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('result', type=dict, location='json')
        args = parser.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlRed = 'INSERT INTO `team_has_match_played`(`match_id`, `goals`, `possesion`, `color`, `ended`) VALUES({},{},{},{},{},{})'.format(args['result']['id'], args['result']['red']['score'], args['result']['red']['possession'], 'red', 1)
        sqlBlue = 'INSERT INTO `team_has_match_played`(`match_id`, `goals`, `possesion`, `color`, `ended`) VALUES({},{},{},{},{},{})'.format(args['result']['id'], args['result']['blue']['score'], args['result']['blue']['possession'], 'blue', 1)
        cursor.execute(sqlRed)
        cursor.execute(sqlBlue)
        conn.commit()
        return "Created"