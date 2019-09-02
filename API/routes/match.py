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
                print(dico1)
                dico2 = fake[i+1]
                print(dico2)
                dico1.update(dico2)
                final.append(dico1)
                i += 1
            i+=1
        return final

class AllMatchByDate(Resource):
    def get(self):
        test = Json()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT team_has_match_played.match_id ,team_has_match_played.goals, team_has_match_played.possesion, team_has_match_played.color, team.name, match_played.duration, match_played.name AS `match_name` FROM team_has_match_played INNER JOIN match_played ON team_has_match_played.match_id = match_played.id INNER JOIN team ON team_has_match_played.team_id = team.id')
        rows = cursor.fetchall()
        matchs =test.create(rows)
        if not rows:
            return jsonify({'about':'no matchs found'})
        resp = jsonify(matchs)
        resp.status_code = 200
        return resp

#Recuperer le dernier id s
#cursor.lastrowid