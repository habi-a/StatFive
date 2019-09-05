import pymysql
from app import app
from db_config import mysql
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, inputs
from flaskext.mysql import MySQL
import sys
import werkzeug, os
from subprocess import check_output, CalledProcessError, STDOUT
import time
from datetime import date

sys.path.insert(0, './routes')
from team import *
from user import *
from stats import *
from video import *
from match import *

api = Api(app)

class Home(Resource):
    def get(self):
        return {'message':'Welcome Friends'}


#Route for log
api.add_resource(login, '/login')

#Routes GET for Team
api.add_resource(allTeam, '/teams')
api.add_resource(teamById, '/team/<int:id>')
api.add_resource(teamByName, '/team/<string:name>')
api.add_resource(averageTeam, '/teams/average')

#Route for match 
api.add_resource(AllMatchByDate, '/matchs')

#Match Stat
api.add_resource(statMatchById, '/match/<int:id>')

#Routes GET AND POST for Users
api.add_resource(user, '/addUser')
api.add_resource(userById, '/user/<int:id>')
api.add_resource(userByName, '/user/<string:name>')
api.add_resource(AllUser, '/users')

#Routes GET for Stats for user or team
api.add_resource(StatUserById, '/stat/user/<int:id>')
api.add_resource(AllStatUser, '/stat/user')
api.add_resource(AllStatTeam, '/stat/team')
api.add_resource(StatTeamById, '/team/stat/<int:id>')

#Routes POST for Team & Score
api.add_resource(createTeam, '/team')
api.add_resource(addStatTeam, '/team/results')
api.add_resource(postVideo, '/video')

#Home
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run()
