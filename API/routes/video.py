import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
import werkzeug, os
from subprocess import check_output, CalledProcessError, STDOUT
import time, json
from datetime import date
import os

class traitement():
    def checkExist(self, team):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT id FROM team WHERE name = "{}"'.format(team)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            sql = 'INSERT INTO `team`(`name`) VALUES ("{}")'.format(team)
            cursor.execute(sql)
            conn.commit()
            team_id = cursor.lastrowid
            return team_id
        id_team = rows[0]['id']
        return id_team

    def getDuration(self, filename):
        command = [
            'ffprobe', 
            '-v', 
            'error', 
            '-show_entries', 
            'format=duration', 
            '-of', 
            'default=noprint_wrappers=1:nokey=1', 
            filename
            ]

        try:
            output = check_output( command, stderr=STDOUT ).decode()
            temps = output.split('\n')
            final = time.strftime("%M:%S", time.gmtime(float(temps[0])))
            return final

        except CalledProcessError as e:
            output = e.output.decode()
            return output
    
    def insertMatch(self, video):
        destpath="/app/video"
        filename = "myMatch"+str(date.today())+".mp4"
        matchName = "Match"+ str(date.today())
        video.save(os.path.join(app.instance_path, destpath,filename))
        filepath = destpath+"/"+filename
        #duration = self.getDuration(filepath)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO `match_played`(`name`, `duration`,`ground`,`path`) VALUES("{}", "{}",{}, "{}")'.format( matchName, "40:00" , 1, filepath)
        cursor.execute(sql)
        conn.commit()
        match_id = cursor.lastrowid
        return match_id
    
    def getFilepath(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT path FROM match_played WHERE id = {}'.format(id)
        cursor.execute(sql)
        rows = cursor.fetchall()
        path = rows[0]['path']
        return path
    
    def lunch(self, match_id, filepath):
        myCmd = os.popen('python /tensorflow/models/research/object_detection/tracker/tracker.py'+' '+ str(match_id) + ' ' + str(id_red) +' '+ str(id_blue) + ' ' +filepath).read()
        return myCmd

class postVideo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('video', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('teamA', type=str, required=True, help='name blue team')
        parser.add_argument('teamB', type=str, required=True, help='name red team')
        args = parser.parse_args()
        test = traitement()
        id_match = test.insertMatch(args['video'])
        id_blue = test.checkExist(args['teamA'])
        id_red = test.checkExist(args['teamB'])
        path = test.getFilepath(id_match)
        lunch = test.lunch(id_match, path, id_blue, id_red)

class postStat(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('result', type=dict, location= 'json')
        args = parser.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO `team_has_match_played`(`match_id`, `team_id`, `goals`, `possesion`, `color`, `ended`) VALUES ({},{},{},{},blue,1)'.format(args["result"]["id"], args["result"]["blue"]["id"], args["result"]["blue"]["score"], args["result"]["blue"]["possession"])
        sql2 = 'INSERT INTO `team_has_match_played`(`match_id`, `team_id`, `goals`, `possesion`, `color`, `ended`) VALUES ({},{},{},{},red,1)'.format(args["result"]["id"], args["result"]["red"]["id"], args["result"]["red"]["score"], args["result"]["red"]["possession"])
	cursor.execute(sql)
	cursor.execute(sql2)
        conn.commit()
        return jsonify({'about':'Les stats sont uploads'})
