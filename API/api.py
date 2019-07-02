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
from stats import *

api = Api(app)

class Home(Resource):
    def get(self):
        return {'message':'Welcome Friends'}

#Route for log

#Routes for Team
api.add_resource(allTeam, '/team')
api.add_resource(teamById, '/team/<int:id>')
api.add_resource(teamByName, '/team/<string:name>')

#Routes for Users
api.add_resource(user, '/addUser')
api.add_resource(userById, '/user/<int:id>')
api.add_resource(userByName, '/user/<string:name>')
api.add_resource(AllUser, '/users')

#Routes for Stats
api.add_resource(StatUserById, '/stat/user/<int:id>')
api.add_resource(AllStatUser, '/stat/user')
api.add_resource(AllStatTeam, '/stat/team')
api.add_resource(StatTeamById, '/team/stat/<int:id>')
api.add_resource(StatTeam, '/team/results')

api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run()
