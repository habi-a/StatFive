from flask import request, Blueprint

from ..models import db
from ..models.user import User
from ..models.complex import Complex
from ..auth.authentication import Auth
from ..helper import custom_response

import statistics

complex_api = Blueprint('complex', __name__)


@complex_api.route('/create-complex', methods=['POST'])
@Auth.super_admin_required
def create_complex():
    req_data = request.get_json()
    #
    # user_in_db = User.query.filter_by(id=req_data['user_id']).first()
    # if not user_in_db:
    #     message = {'error': True, 'message': 'L\' utilisateur existe pas.', 'data': None}
    #     return custom_response(message, 404)

    complex_m = Complex(
        name=req_data['name'],
        phone=req_data['phone'],
        address=req_data['address']
    )
    complex_m.save()
    # user_in_db.complex_id = complex_m.id
    # db.session.commit()
    return custom_response({'error': False, 'message': 'Complex save', 'data': complex_m.to_json()}, 201)
