import pymysql
import hashlib
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL

class user(Resource):
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=inputs.regex('^[^\W][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4}$'), required=True, help='Email address to create user')
            parser.add_argument('password', type=str, required=True, help='Password to create user')
            parser.add_argument('c_password', type=str, required=True, help='Confirm password to create user')
            parser.add_argument('lastname', type=str, required=True, help='Lastname')
            parser.add_argument('firstname', type=str, required=True, help='Firstname')
            args = parser.parse_args()
            email = args['email']
            password = hashlib.sha256(args['password'].encode()).hexdigest()
            password2 =  hashlib.sha256(args['c_password'].encode()).hexdigest()
            firstname = args['firstname']
            lastname = args['lastname']
            if password == password2:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery = 'INSERT INTO users ( mail, lastname, firstname, password) VALUES ("{}", "{}", "{}", "{}")'.format(email, lastname, firstname, password)
                cursor.execute(sqlQuery)
                conn.commit()
                return jsonify({'Email': args['email'], 'Firstame':args['firstname'], 'Lastame':args['lastname'], 'created':'Ok'})
            
            return jsonify({'about':'Password invalid'})
            
        except Exception as e:
            return {'error' : str(e)}
    
class AllUser(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class UserStat(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("Select mail, name, firstname, stats.kilometre, stats.passe, stats.but FROM users INNER JOIN stats ON user_id = 1")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp