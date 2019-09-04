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

class traitemant():
    def checkExist(team):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT id FROM team WHERE name = {}".format(team)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            sql = 'INSERT INTO `team`(`name`) VALUES ("{}")'.format(team)
            cursor.execute(sql)
            conn.commit()
            team_id = cursor.lastrowid
            return team_id
        id_team = rows['id']
        return id_team

    def insertMatch():
        return test


def getDuration(filename):
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

class postVideo(Resource):
    def post(self):
        destpath="/mnt/c/Users/nour/Documents/ProjetLib/Git/StatFive/video"
        parser = reqparse.RequestParser()
        parser.add_argument('video', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('teamA', type=str, required=True, help='name blue team')
        parser.add_argument('teamB', type=str, required=True, help='name red team')
        args = parser.parse_args()
        video = args['video']
        print(args)
        return "TEst"
        if args:
            video = args['video']
            filename = "myMatch"+str(date.today())+".mp4"
            matchName = "Match"+ str(date.today())
            video.save(os.path.join(destpath,filename))
            filepath = destpath+"/"+filename
            duration = getDuration(filepath)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = 'INSERT INTO `match_played`(`name`, `duration`,`path`) VALUES("{}", "{}", "{}")'.format( matchName, str(duration) ,filepath)
            cursor.execute(sql)
            conn.commit()
            return jsonify({'about':'Uploaded'})
        else:
            print(args['video'])
            print(args)
            return jsonify({'about':'no file uploaded'})
