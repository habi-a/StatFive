import random
import string

from flask import request, json, Response, Blueprint, g
from flasgger import swag_from
from datetime import datetime

from ..models.complex import Complex
from ..specs import specs_users
from ..auth.authentication import Auth
from ..helper import custom_response, video_url_for
from ..helper.user_mail import send_verification_code_mail, send_reset_password_mail
from ..models.user import User, UserPending, UserHasTeam
from ..models.stats import Stats
from ..models import db
from ..models.match import Match
from ..models.team import TeamHasMatchPlayed, Team

user_api = Blueprint('users', __name__)


@user_api.route('/create', methods=['POST'])
@swag_from(specs_users.create)
def create():
    req_data = request.get_json()

    user_in_db = User.get_user_by_email(req_data['email'])
    if user_in_db:
        message = {'error': True, 'message': 'Email déjà existant, veuillez en choisir un autre.', 'data': None}
        return custom_response(message, 400)
    code = ''.join(random.choices(string.digits, k=6))
    send_verification_code_mail('Votre code de validation est le', req_data['email'], code)
    password = User.hash_password(req_data['password'])
    user = User(
        firstname=req_data['firstname'],
        name=req_data['lastname'],
        mail=req_data['email'],
        password=password,
        role=0,
        code=code,
        verification=False
    )
    user.save()
    return custom_response({'error': False, 'message': 'Utilisateur bien enregistré.', 'data': None}, 201)


@user_api.route('/verification_code/<string:code>', methods=['GET'])
@swag_from(specs_users.verification_code)
@Auth.auth_required
def verification_code(code):
    user_in_db = User.get_one_user(g.user['id'])
    if code != user_in_db.code:
        message = {'error': True, 'message': 'Code pas bon.', 'data': None}
        return custom_response(message, 400)
    user_in_db.verification = True
    db.session.commit()
    return custom_response({'error': False, 'message': 'Code bon.', 'data': None}, 200)


@user_api.route('/login', methods=['POST'])
@swag_from(specs_users.login)
def login():
    req_data = request.get_json()

    user_in_db = User.get_user_by_email(req_data['email'])
    if not user_in_db:
        message = {'error': True, 'message': 'Le compte n\'existe pas.', 'data': None}
        return custom_response(message, 404)

    if not user_in_db.check_password(req_data['password']):
        message = {'error': True, 'message': 'Mauvais mot de passe.', 'data': None}
        return custom_response(message, 401)

    user = user_in_db.to_json(True)
    user['token'] = Auth.generate_token(user_in_db.id)

    return custom_response({'error': False, 'message': 'Utilisateur bien login.', 'data': user}, 201)


@user_api.route('/mail-reset-password', methods=['POST'])
def mail_reset_password():

    req_data = request.get_json()

    user_in_db = User.get_user_by_email(req_data['email'])
    if not user_in_db:
        message = {'error': True, 'message': 'Le compte n\'existe pas.', 'data': None}
        return custom_response(message, 404)

    m_pending = UserPending.query.filter_by(type="reset_password", user_id=user_in_db.id).first()
    if m_pending:
        m_pending.delete()

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    m_pending: UserPending = UserPending(
        type="reset_password", code=code,
        expired=False,
        created_at=datetime.utcnow(),
        user_id=user_in_db.id
    )
    m_pending.save()
    send_reset_password_mail('Votre lien pour changer de mot de passe', req_data['email'], code)

    return custom_response({'error': False, 'message': 'get me', 'data': None}, 200)


@user_api.route('/confirm-reset-password', methods=['POST'])
def confirm_reset_password():

    req_data = request.get_json()

    m_pending = UserPending.query.filter_by(type="reset_password", code=req_data['code']).first()
    if not m_pending:
        message = {'error': True, 'message': 'Le pending n\'existe pas.', 'data': None}
        return custom_response(message, 404)

    m_user: User = m_pending.user

    m_user.password = User.hash_password(req_data['password'])
    db.session.delete(m_pending)
    db.session.commit()

    return custom_response({'error': False, 'message': 'mot de passee change', 'data': m_user.to_json()}, 200)


def get_data_complex(complex_id):
    matchs_in_db = Match.query.filter_by(complex_id=complex_id).all()
    nb_but = 0

    for match in matchs_in_db:
        li_team_has_match_played = TeamHasMatchPlayed.query.filter_by(match_id=match.id).all()
        for team_has_match_played in li_team_has_match_played:
            nb_but += team_has_match_played.goals

    return {'nb_match': len(matchs_in_db), 'nb_but': nb_but}


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():

    user_in_db = User.query.filter_by(id=g.user['id']).first()

    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)

    user = user_in_db.to_json(True)

    if user['complex_id']:
        user['stats'] = get_data_complex(user['complex_id'])
    elif user['role'] == 2:
        li_complex_in_db = Complex.query.all()
        li_complex_data = []
        for complex_in_db in li_complex_in_db:
            complex_data = complex_in_db.to_json()
            complex_data['stats'] = get_data_complex(complex_in_db.id)
            li_complex_data.append(complex_data)
        user['complexes'] = li_complex_data
    else:
        data = []
        li_m_user_has_team = UserHasTeam.query.filter_by(user_id=g.user['id']).all()
        for m_user_has_team in li_m_user_has_team:
            team_in_db = Team.query.filter_by(id=m_user_has_team.team_id).first()
            data_team = team_in_db.to_json()
            data_team['nb_but'] = 0
            li_team_has_match_played = TeamHasMatchPlayed.query.filter_by(team_id=team_in_db.id).all()
            for team_has_match_played in li_team_has_match_played:
                data_team['nb_but'] += team_has_match_played.goals
            data.append(data_team)
        user['teams'] = data

    return custom_response({'error': False, 'message': 'get me', 'data': user}, 200)


@user_api.route('/<int:id>', methods=['GET'])
@swag_from(specs_users.user_by_id)
@Auth.auth_required
def get_user_by_id(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)

    user = user_in_db.to_json()

    return custom_response({'error': False, 'message': 'Utilisateur by id.', 'data': user}, 200)


@user_api.route('/<int:id>', methods=['PUT'])
@swag_from(specs_users.update_user_by_id)
@Auth.auth_required
def update_user(id):
    req_data = request.get_json()

    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)

    user_in_db.description = req_data['description']
    user_in_db.post = req_data['post']

    db.session.commit()

    user = user_in_db.to_json()

    return custom_response({'error': False, 'message': 'Update Utilisateur by id.', 'data': user}, 200)


@user_api.route('/<string:name>', methods=['GET'])
@swag_from(specs_users.user_by_name)
def get_user_by_name(name):
    user_in_db = User.query.filter_by(name=name).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)

    user = user_in_db.to_json()

    return custom_response({'error': False, 'message': 'Utilisateur by name.', 'data': user}, 200)


@user_api.route('/all_user', methods=['GET'])
@swag_from(specs_users.all_user)
@Auth.auth_required
def all_user():
    users_in_db = User.query.all()
    users = []
    for user in users_in_db:
        if user.role != 2:
            users.append(user.to_json(True))
    return custom_response({'error': False, 'message': 'Liste de user.', 'data': users}, 200)


@user_api.route('/stat_user_by_id/<int:id>', methods=['GET'])
@swag_from(specs_users.stat_user_by_id)
@Auth.auth_required
def stat_user_by_id(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)
    stats_in_db = Stats.query.filter_by(user=user_in_db).all()
    stats = []
    for stat in stats_in_db:
        stats.append(stat.to_json())

    data = {**user_in_db.to_json(True), **{'stats': stats}}
    return custom_response({'error': False, 'message': 'Liste de stats by id.', 'data': data}, 200)
