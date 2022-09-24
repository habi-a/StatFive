from flask import request, json, Response, Blueprint, g
from flasgger import swag_from

from ..models.user import UserHasTeam
from ..specs import specs_team
from ..models.team import Team, TeamHasMatchPlayed
from ..auth.authentication import Auth
from ..helper import custom_response

import statistics

team_api = Blueprint('team', __name__)


@team_api.route('/all_team', methods=['GET'])
@swag_from(specs_team.all_team)
@Auth.auth_required
def all_team():
    team_in_db = Team.query.filter_by(id=g.user['id']).all()
    teams = []
    for team in team_in_db:
        teams.append(team.to_json())
    return custom_response({'error': False, 'message': 'Liste de team.', 'data': teams}, 200)


@team_api.route('/average_team', methods=['GET'])
@swag_from(specs_team.average_team)
@Auth.auth_required
def average_team():
    team_in_db = Team.query.all()
    teams = []
    for team in team_in_db:
        data = {'name': team.name}
        li_avg = []
        for t_match_p in team.team_match_played:
            li_avg.append(t_match_p.goals)
        data['moyenne_goal'] = 0 if not li_avg else int(statistics.mean(li_avg))
        teams.append(data)

    return custom_response({'error': False, 'message': 'Liste average goal team.', 'data': teams}, 200)


@team_api.route('', methods=['GET'])
@swag_from(specs_team.team_by_id)
@Auth.auth_required
def get_team_by_id():
    # team_in_db = Team.query.filter_by(id=id).first()
    # if not team_in_db:
    #     message = {'error': True, 'message': 'La team existe pas.', 'data': None}
    #     return custom_response(message, 404)

    li = []
    li_m_user_has_team = UserHasTeam.query.filter_by(user_id=g.user['id']).all()
    for m_user_has_team in li_m_user_has_team:
        team_in_db = Team.query.filter_by(id=m_user_has_team.team_id).first()
        data = {'team': team_in_db.to_json(), 'user': []}
        two_li_m_user_has_team = UserHasTeam.query.filter_by(team_id=team_in_db.id).all()
        for two_m_user_has_team in two_li_m_user_has_team:
            data['user'].append(two_m_user_has_team.user.to_json())

        li.append(data)

    return custom_response({'error': False, 'message': 'Team by id.', 'data': li}, 200)


@team_api.route('/stat_team_by_id/<int:id>', methods=['GET'])
@swag_from(specs_team.stat_team_by_id)
@Auth.auth_required
def stat_team_by_id(id):
    team_in_db = Team.query.filter_by(id=id).first()
    if not team_in_db:
        message = {'error': True, 'message': 'La team existe pas.', 'data': None}
        return custom_response(message, 404)
    stats = []
    for stat in team_in_db.stats:
        stats.append(stat.to_json())
    data = {**team_in_db.to_json(), **{'stats': stats}}
    return custom_response({'error': False, 'message': 'Team stats by id.', 'data': data}, 200)


@team_api.route('/<string:name>', methods=['GET'])
@swag_from(specs_team.team_by_name)
@Auth.auth_required
def get_team_by_name(name):
    team_in_db = Team.query.filter_by(name=name).first()
    if not team_in_db:
        message = {'error': True, 'message': 'La team existe pas.', 'data': None}
        return custom_response(message, 404)

    team = team_in_db.to_json()

    return custom_response({'error': False, 'message': 'Team by name.', 'data': team}, 200)


@team_api.route('/create_team', methods=['POST'])
@swag_from(specs_team.create)
@Auth.auth_required
def create_team():
    req_data = request.get_json()

    for team in req_data:
        m_team = Team(name=team['name'])
        m_team.save()
        for p in team['player']:
            m_user_has_match = UserHasTeam(team_id=m_team.id, user_id=p)
            m_user_has_match.save()

    return custom_response({'error': False, 'message': 'Team bien enregistré.', 'data': None}, 201)
