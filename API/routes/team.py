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
        parser = reqparse.RequestParser()
        parser.add_argument('red', type=dict, location='json')
        parser.add_argument('blue', type=dict, location='json')
        args = parser.parse_args()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlRed = 'INSERT INTO `team`(`name`) VALUES({})'.format()
        sqlBlue = 'INSERT INTO `team`(`name`) VALUES({})'.format()
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
