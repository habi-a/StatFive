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
<<<<<<< HEAD
from stats import *

api = Api(app)

=======

api = Api(app)

class Index(Resource):
    def get(self, name):
        return {'Ton nom est' : name}

>>>>>>> 993db78dcaa7e5683db8964e36067d7def262f6f
class Home(Resource):
    def get(self):
        return {'message':'Welcome Friends'}

<<<<<<< HEAD
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

api.add_resource(Home, '/')
=======
#Routes for team
api.add_resource(allTeam, '/team')
api.add_resource(Stats, '/stat/<int:id>')

#Routes for user
api.add_resource(user, '/addUser')
api.add_resource(AllUser, '/users')
api.add_resource(UserStat, '/stat')

api.add_resource(Home, '/')
api.add_resource(Index, '/index/<name>')
>>>>>>> 993db78dcaa7e5683db8964e36067d7def262f6f

if __name__ == '__main__':
    app.run()
