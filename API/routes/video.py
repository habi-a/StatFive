import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
import werkzeug, os
from subprocess import check_output, CalledProcessError, STDOUT
import time
from datetime import date

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
            print(final)
            return final

        except CalledProcessError as e:
            output = e.output.decode()
            return output

class postVideo(Resource):
    def post(self):
        destpath="/mnt/c/Users/nour/Documents/ProjetLib/Git/StatFive/video"
        parser = reqparse.RequestParser()
        parser.add_argument('video', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
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
