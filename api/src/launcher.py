import mimetypes
import os

from flask import Flask, jsonify, redirect, url_for, Response, send_file
from flasgger import Swagger, swag_from
from flask_cors import CORS
from flask_mail import Mail
from pathlib import Path

from .models import db, mail
from . import config


def create_app(config_key='development'):
    app = Flask(__name__)

    app.config.from_object(config.app_config[config_key])
    config.send_mail = Mail(app)

    db.init_app(app)
    mail.init_app(app)
    Swagger(app)
    CORS(app)

    from .controllers.users_controllers import user_api as user_blueprint
    from .controllers.team_controllers import team_api as team_blueprint
    from .controllers.match_controllers import match_api as match_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(team_blueprint, url_prefix='/api/team')
    app.register_blueprint(match_blueprint, url_prefix='/api/match')

    @app.route('/')
    def index():
        return redirect(url_for('flasgger.apidocs'))

    @app.route('/get-video/<path>', methods=['GET'])
    def video(path: str):
        response = Response()

        str_file_path = './src/files'
        file_folder = os.path.abspath(str_file_path)
        file_path = Path(file_folder)

        if not file_path.exists():
            response.status_code = 400
            return response

        final_filepath = file_path / path
        if not final_filepath.exists():
            response.status_code = 404
            return response

        return send_file(final_filepath)

    return app
