import pymysql
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL
import sys
sys.path.insert(0, './routes')
from team import *
from user import *

api = Api(app)

class Index(Resource):
    def get(self, name):
        return {'Ton nom est' : name}

class Home(Resource):
    def get(self):
        return {'message':'Welcome Friends'}

#Routes for team
api.add_resource(allTeam, '/team')
api.add_resource(Stats, '/stat/<int:id>')

#Routes for user
api.add_resource(user, '/addUser')
api.add_resource(AllUser, '/users')
api.add_resource(UserStat, '/stat')

api.add_resource(Home, '/')
api.add_resource(Index, '/index/<name>')

if __name__ == '__main__':
    app.run()
