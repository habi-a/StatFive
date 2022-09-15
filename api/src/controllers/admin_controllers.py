from flask import request, Blueprint

from ..models import db
from ..models.user import User
from ..models.complex import Complex
from ..auth.authentication import Auth
from ..helper import custom_response

import statistics

admin_api = Blueprint('admin', __name__)


@admin_api.route('/make-admin/<int:id>', methods=['GET'])
@Auth.super_admin_required
def make_admin(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)
    user_in_db.role = 1 if user_in_db.role == 0 else 0
    db.session.commit()
    return custom_response({'error': False, 'message': 'make-admin', 'data': user_in_db.to_json()}, 200)


@admin_api.route('/list-complex', methods=['GET'])
@Auth.super_admin_required
def list_complex():
    li_complex_m = Complex.query.all()
    li_complex = []

    for complex_m in li_complex_m:
        li_complex.append(complex_m.to_json())
    return custom_response({'error': False, 'message': 'list-complex', 'data': li_complex}, 200)


@admin_api.route('/user-to-complex/<int:id>/<int:complex_id>', methods=['GET'])
@Auth.super_admin_required
def user_to_complex(id, complex_id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)
    complex_in_db = Complex.query.filter_by(id=complex_id).first()
    if not complex_in_db:
        message = {'error': True, 'message': 'Le complex existe pas.', 'data': None}
        return custom_response(message, 404)
    user_in_db.complex_id = complex_in_db.id
    db.session.commit()
    return custom_response({'error': False, 'message': 'make-admin', 'data': None}, 200)


@admin_api.route('/user-dissociate-complex/<int:id>', methods=['DEL'])
@Auth.super_admin_required
def user_del_complex(id):
    user_in_db = User.query.filter_by(id=id).first()
    if not user_in_db:
        message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
        return custom_response(message, 404)
    user_in_db.complex_id = None
    db.session.commit()
    return custom_response({'error': False, 'message': 'user-dissociate-complex', 'data': None}, 200)