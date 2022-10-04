from marshmallow import fields, Schema
import datetime

from . import db

from .complex import Complex

from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
    User Model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    post = db.Column(db.String(200))
    image = db.Column(db.String(200))
    role = db.Column(db.String(200))
    code = db.Column(db.String(200))
    verification = db.Column(db.Boolean)
    complex_id = db.Column(db.Integer, db.ForeignKey('complex.id'), nullable=True)
    complex: Complex = db.relationship(Complex)

    def check_password(self, password):
        """
            It will check if password passed in parameter is the same as the password from User
        """
        hashed_pass = self.password
        return check_password_hash(hashed_pass, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self, get_complex=False):

        data = {
            'id': self.id,
            'lastname': self.name,
            'firstname': self.firstname,
            'email': self.mail,
            'verification': self.verification,
            'post': self.post,
            'description': self.description,
            'role': self.role,
            'complex_id': self.complex_id
        }
        if get_complex and self.complex:
            data['complex'] = self.complex.to_json()
        return data

    @staticmethod
    def hash_password(password):
        """
            Hash the password passed in parameter
        """
        return generate_password_hash(password)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(mail=email).first()

    @staticmethod
    def get_one_user(id):
        return User.query.filter_by(id=id).first()


class UserHasTeam(db.Model):
    """
    UserHasTeam Model
    """
    __tablename__ = 'user_has_team'

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    team = db.relationship('Team')
    user = db.relationship('User')

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserPending(db.Model):
    """
    UserPending Model
    """
    __tablename__ = 'pending'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String)
    code = db.Column(db.String)
    expired = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
