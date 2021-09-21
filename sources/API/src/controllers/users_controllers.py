import random
import string

from flask import request, json, Response, Blueprint, g
from flasgger import swag_from

from ..specs import specs_users
from ..auth.authentication import Auth
from ..helper import custom_response
from ..helper.user_mail import send_verification_code_mail
from ..models.user import User
from ..models.stats import Stats
from ..models import db

user_api = Blueprint('users', __name__)


@user_api.route('/create', methods=['POST'])
@swag_from(specs_users.create)
def create():
    req_data = request.get_json()

    user_in_db = User.get_user_by_email(req_data['email'])
    if user_in_db:
        message = {'error': True, 'message': 'Email déjà existant, veuillez en choisir un autre.', 'data': None}
        return custom_response(message, 400)
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
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

    user = user_in_db.to_json()
    user['token'] = Auth.generate_token(user_in_db.id)

    return custom_response({'error': False, 'message': 'Utilisateur bien login.', 'data': user}, 201)


@user_api.route('/<int:id>', methods=['GET'])
@swag_from(specs_users.user_by_id)
def get_user_by_id(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)

    user = user_in_db.to_json()

    return custom_response({'error': False, 'message': 'Utilisateur by id.', 'data': user}, 200)


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
def all_team():
    users_in_db = User.query.all()
    users = []
    for user in users_in_db:
        users.append(user.to_json())
    return custom_response({'error': False, 'message': 'Liste de user.', 'data': users}, 200)


@user_api.route('/stat_user_by_id/<int:id>', methods=['GET'])
@swag_from(specs_users.stat_user_by_id)
def stat_user_by_id(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)
    stats_in_db = Stats.query.filter_by(user=user_in_db).all()
    stats = []
    for stat in stats_in_db:
        stats.append(stat.to_json())

    data = {**user_in_db.to_json(), **{'stats': stats}}
    return custom_response({'error': False, 'message': 'Liste de stats by id.', 'data': data}, 200)
