import os
import random
import string
import subprocess
import requests

from flask import request, json, Response, Blueprint
from flasgger import swag_from

from ..models.user import UserHasTeam
from ..specs import specs_match
from ..models.match import Match
from ..models.team import TeamHasMatchPlayed
from ..auth.authentication import Auth
from ..helper import custom_response, video_url_for
from ..models import db

from subprocess import check_output, CalledProcessError, STDOUT

match_api = Blueprint('match', __name__)


def generate_random_number(number_of_digits: int) -> str:
    return ''.join([random.choice(string.digits) for _ in range(number_of_digits)])


@match_api.route('', methods=['POST'])
# @swag_from(specs_match.all_match)
def post_match():
    video_storage = request.files.get('video')
    if not video_storage or video_storage.content_type != 'video/mp4':
        return custom_response({'error': 'Is not a mp4 file.'}, 400)
    req_data = request.form.to_dict()

    path_file = '/app/video/'
    name_file = generate_random_number(6) + '_' + video_storage.name + '.mp4'

    video_storage.save(path_file + name_file)

    m_match = Match(name=name_file, duration="10:00", ground=1, path=path_file + name_file)
    m_match.save()
    m_team_has_match_played = TeamHasMatchPlayed(team_id=req_data['team_one'],
                                                 match_id=m_match.id,
                                                 goals=3,
                                                 possesion=70,
                                                 color=0,
                                                 ended=1)
    m_team_has_match_played.save()

    m_team_has_match_played = TeamHasMatchPlayed(team_id=req_data['team_two'],
                                                 match_id=m_match.id,
                                                 goals=2,
                                                 possesion=30,
                                                 color=1,
                                                 ended=1)
    m_team_has_match_played.save()

    x = requests.post('http://tracker-app:5000/analyse', json={
        "match_id": m_match.id,
        "id_red": req_data['team_one'],
        "id_blue": req_data['team_two'],
        "video_match": f"/app/video/{name_file}",
        "show": False,
        "callback": "http://api:5000/api/match/result"
    })

    return custom_response({'error': False, 'message': 'Sauvegarde du match.', 'data': None}, 200)


@match_api.route('/result', methods=['POST'])
# @swag_from(specs_match.all_match)
def result():
    req_data = request.get_json()
    match_id = req_data['result']['id']
    m_match = Match.query.filter_by(id=match_id).first()
    m_match.finish = True
    db.session.commit()
    m_li_team_has_match_played = TeamHasMatchPlayed.query.filter_by(match_id=match_id).all()

    result_team = req_data['result']['red']
    for m_team_has_match_played in m_li_team_has_match_played:
        m_team_has_match_played.goals = result_team['score']
        m_team_has_match_played.possesion = result_team['possession']
        db.session.commit()
        result_team = req_data['result']['blue']

    return custom_response({'error': False, 'message': 'Update match result.', 'data': None}, 200)


@match_api.route('/all_match', methods=['GET'])
@swag_from(specs_match.all_match)
@Auth.auth_required
def all_match():
    matchs_in_db = Match.query.all()
    matchs = []
    for match in matchs_in_db:
        match_data = match.to_json()
        match_data['path'] = video_url_for('video', path=match_data['name'])
        matchs.append(match_data)
    return custom_response({'error': False, 'message': 'Listes des matchs.', 'data': matchs}, 200)


@match_api.route('/stat_match_by_id/<int:id>', methods=['GET'])
@swag_from(specs_match.stat_match_by_id)
@Auth.auth_required
def stat_match_by_id(id):
    match_in_db = Match.query.filter_by(id=id).first()
    if not match_in_db:
        message = {'error': True, 'message': 'Le match existe pas.', 'data': None}
        return custom_response(message, 404)
    if not match_in_db.finish:
        message = {'error': True, 'message': 'Le match est en cours d\'analyse.', 'data': None}
        return custom_response(message, 404)

    match_data = match_in_db.to_json()
    match_data['path'] = video_url_for('video', path=match_in_db.name)

    team_has_match_played = TeamHasMatchPlayed.query.filter_by(match_id=match_in_db.id).all()

    data = {
        **match_data,
        **{'players': None},
    }

    for stat in team_has_match_played:
        user_has_teams = UserHasTeam.query.filter_by(team_id=stat.team_id).all()
        li_user = []
        for user_has_team in user_has_teams:
            li_user.append(user_has_team.user.to_json())
        if int(stat.color) == 0:
            data['team_red'] = {**stat.to_json(), **user_has_team.team.to_json(), 'players': li_user}
        else:
            data['team_blue'] = {**stat.to_json(), **user_has_team.team.to_json(), 'players': li_user}

    return custom_response({'error': False, 'message': 'Match stats by id match.', 'data': data}, 200)
