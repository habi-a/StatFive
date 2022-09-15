from functools import wraps
from flask import json, Response, request, g
from ..models.user import User
import datetime
import jwt


class Auth:

    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(mimetype='application/json',
                                response=json.dumps(
                                    {'error': 'Authentication token is not available, please login to get one'}),
                                status=400)
            else:
                token = request.headers.get('api-token')
                data = Auth.decode_token(token)
                if data['error']:
                    return Response(mimetype='application/json',
                                    response=json.dumps(data['error']),
                                    status=400)
                user_id = data['data']['user_id']
                check_user = User.get_one_user(user_id)
                if not check_user:
                    return Response(mimetype='application/json',
                                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                                    status=400)
                g.user = {'id': user_id}
                return func(*args, **kwargs)

        return decorated_auth

    @staticmethod
    def super_admin_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(mimetype='application/json',
                                response=json.dumps(
                                    {'error': 'Authentication token is not available, please login to get one'}),
                                status=400)
            else:
                token = request.headers.get('api-token')
                data = Auth.decode_token(token)
                if data['error']:
                    return Response(mimetype='application/json',
                                    response=json.dumps(data['error']),
                                    status=400)
                user_id = data['data']['user_id']
                check_user = User.get_one_user(user_id)
                if not check_user:
                    return Response(mimetype='application/json',
                                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                                    status=400)
                elif check_user.role != 2:
                    return Response(mimetype='application/json',
                                    response=json.dumps({'error': 'user not super admin'}),
                                    status=400)
                g.user = {'id': user_id}
                return func(*args, **kwargs)

        return decorated_auth

    @staticmethod
    def admin_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(mimetype='application/json',
                                response=json.dumps(
                                    {'error': 'Authentication token is not available, please login to get one'}),
                                status=400)
            else:
                token = request.headers.get('api-token')
                data = Auth.decode_token(token)
                if data['error']:
                    return Response(mimetype='application/json',
                                    response=json.dumps(data['error']),
                                    status=400)
                user_id = data['data']['user_id']
                check_user = User.get_one_user(user_id)
                if not check_user:
                    return Response(mimetype='application/json',
                                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                                    status=400)
                elif check_user.role != 2 and check_user.role != 1:
                    return Response(mimetype='application/json',
                                    response=json.dumps({'error': 'user not super admin or admin'}),
                                    status=400)
                g.user = {'id': user_id}
                return func(*args, **kwargs)

        return decorated_auth


    @staticmethod
    def generate_token(user_id):

        try:
            payload = {'exp': datetime.datetime.utcnow() + (datetime.timedelta(days=1)),
                       'iat': datetime.datetime.utcnow(),
                       'sub': user_id}
            return jwt.encode(payload, 'StatFive', 'HS256')
        except Exception as e:
            try:
                return Response(mimetype='application/json',
                                response=json.dumps({'error': 'error in generating user token'}),
                                status=400)
            finally:
                e = None
                del e

    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, 'StatFive', 'HS256')
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            try:
                re['error'] = {'message': 'token expired, please login again.'}
                return re
            finally:
                e1 = None
                del e1
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token.'}
            return re
