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
            parser.add_argument('password', required=True, type=str, help='Password to create user')
            parser.add_argument('c_password', required=True, type=str, help='Confirm password to create user')
            parser.add_argument('lastname', required=True, type=str, help='Lastname')
            parser.add_argument('firstname', required=True, type=str, help='Firstname')
            args = parser.parse_args()
            print(args)
            email = args['email']
            password = hashlib.sha256(args['password'].encode()).hexdigest()
            password2 =  hashlib.sha256(args['c_password'].encode()).hexdigest()
            firstname = args['firstname']
            lastname = args['lastname']
            role = 0
            if password == password2:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                sqlQuery= 'SELECT firstname FROM users WHERE mail = "{}"'.format(email)
                cursor.execute(sqlQuery)
                rows = cursor.fetchall()
                if len(rows) == 0:
                    sqlQuery = 'INSERT INTO users ( mail, name, firstname, password, role) VALUES ("{}", "{}", "{}", "{}", "{}")'.format(email, lastname, firstname, password, role)
                    cursor.execute(sqlQuery)
                    conn.commit()
                    return jsonify({'Email': args['email'], 'Role': role, 'Firstame':args['firstname'], 'Lastname':args['lastname'], 'status':200})
                else:
                    return jsonify({'about':'Mail exist'})
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

class userByName(Resource):
    def get(self, name):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT firstname, lastname, mail, role FROM users WHERE firstname LIKE %s', name+'%')
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class userById(Resource):
    def get(self, id):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT firstname, lastname, mail, role FROM users WHERE id ={}').format(id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

class login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=inputs.regex('^[^\W][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4}$'), required=True, help='Email address to login')
        parser.add_argument('password', type=str, required=True, help='Password to login')
        args = parser.parse_args()
        email = args['email']
        password = hashlib.sha256(args['password'].encode()).hexdigest()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql ='SELECT firstname, name, mail, role FROM users WHERE  mail= "{}" AND password = "{}"'.format(email, password)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            error = {'about': 'Error Connection', 'Connected':False, 'email': email, 'password': args['password']}
            return jsonify(error)
        co= {'Connected':True, 'User':rows}
        resp = jsonify(co)
        return resp
