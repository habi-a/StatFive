import random
import string
import unittest

from ..models import db, user
from ..models.team import Team
from ..models.user import UserHasTeam
from flask import Flask
from .. import config


def create_app(config_key='development'):
    app = Flask(__name__)
    app.config.from_object(config.app_config[config_key])
    db.init_app(app)
    return app


class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        """This test verify that we can create multiple users.
        This is a vanilla test since it doesn't attach the user to other models in database
        e.g, service, useridtag, etc.
        """

        email1 = ''.join(random.choices(string.digits, k=6))
        email1 = email1 + "@statfive.fr"
        password = ''.join(random.choices(string.digits, k=10))
        code = ''.join(random.choices(string.digits, k=6))

        m_user1 = user.User(
            firstname='firstname1',
            name='lastname1',
            mail='email1@gmail.com',
            password=password,
            role=0,
            code=code,
            verification=False
        )

        email2 = ''.join(random.choices(string.digits, k=6))
        email2 = email2 + "@statfive.fr"

        m_user2 = user.User(
            firstname='firstname2',
            name='lastname2',
            mail='email2@gmail.com',
            password=password,
            role=1,
            code=code,
            verification=False
        )

        db.session.add_all([m_user1, m_user2])
        db.session.commit()

        self.assertEqual(m_user1.firstname, 'firstname1')
        self.assertEqual(m_user1.name, 'lastname1')
        self.assertEqual(m_user1.mail, email1)
        self.assertEqual(m_user2.firstname, 'firstname2')
        self.assertEqual(m_user2.name, 'lastname2')
        self.assertEqual(m_user2.mail, email2)


class TeamModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_team(self):
        """This test verify that we can create multiple users.
        This is a vanilla test since it doesn't attach the user to other models in database
        e.g, service, useridtag, etc.
        """

        email1 = ''.join(random.choices(string.digits, k=6))
        email1 = email1 + "@statfive.fr"
        password = ''.join(random.choices(string.digits, k=10))
        code = ''.join(random.choices(string.digits, k=6))

        m_user1 = user.User(
            firstname='firstname1',
            name='lastname1',
            mail=email1,
            password=password,
            role=0,
            code=code,
            verification=False
        )

        email2 = ''.join(random.choices(string.digits, k=6))
        email2 = email2 + "@statfive.fr"

        m_user2 = user.User(
            firstname='firstname2',
            name='lastname2',
            mail=email2,
            password=password,
            role=1,
            code=code,
            verification=False
        )

        db.session.add_all([m_user1, m_user2])
        db.session.commit()

        m_team = Team(name='name')
        db.session.add(m_team)
        db.session.commit()
        m_user_has_match1 = UserHasTeam(team_id=m_team.id, user_id=m_user1.id)
        m_user_has_match2 = UserHasTeam(team_id=m_team.id, user_id=m_user2.id)
        db.session.add_all([m_user_has_match1, m_user_has_match2])
        db.session.commit()

        self.assertEqual(m_team.name, 'name')
        self.assertEqual(m_user_has_match1.user_id, m_user1.id)
        self.assertEqual(m_user_has_match2.user_id, m_user2.id)
        self.assertEqual(m_user_has_match1.team_id, m_team.id)
        self.assertEqual(m_user_has_match2.team_id, m_team.id)


if __name__ == '__main__':
    unittest.main()
