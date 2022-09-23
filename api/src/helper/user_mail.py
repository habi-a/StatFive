import os
import random
import string

from typing import Dict
from flask import render_template
from flask_mail import Message as Message_mail
from ..models import mail

# from app.launcher import mail
# from common.helper.settings import get_settings


def send_verification_code_mail(message: str, email: str, code: str) -> str:
    """Sends a verification code mail to a user or prospect
    :param code:
    :param message text displayed in the mail body before the randomly generated code
    :param email mail address where to send the mail
    :return the randomly generated code
    """

    sender = os.environ.get('MAIL_USERNAME', 'noreply@statfive.fr')

    msg = Message_mail('Votre code de vérification', sender=sender, recipients=[email])
    msg.html = render_template("send_code.html",
                               code=code,
                               message=message
                               )
    try:
        mail.send(msg)
    except Exception as err:
        print(f"Exception while sending verification mail to {email} : {str(err)}")
        pass

    return code


def send_reset_password_mail(message: str, email: str, code: str) -> str:
    sender = os.environ.get('MAIL_USERNAME', 'noreply@statfive.fr')
    url = os.environ.get('URL_WEB', 'https://dashboard.statfive.fr/')

    msg = Message_mail('Votre lien pour réinitialiser votre mot de passe', sender=sender, recipients=[email])

    msg.html = render_template("reset_password.html",
                               code=code,
                               url=url,
                               message=message
                               )
    try:
        mail.send(msg)
    except Exception as err:
        print(f"Exception while sending verification mail to {email} : {str(err)}")
        pass

    return code


def send_match_finish(message: str, email: str, url_match: str):
    sender = os.environ.get('MAIL_USERNAME', 'noreply@statfive.fr')

    msg = Message_mail('match_finish', sender=sender, recipients=[email])

    msg.html = render_template("match_finish.html",
                               url=url_match,
                               message=message
                               )
    try:
        mail.send(msg)
    except Exception as err:
        print(f"Exception while sending verification mail to {email} : {str(err)}")
        pass
