from marshmallow import fields, Schema
import datetime
from . import db

from werkzeug.security import check_password_hash, generate_password_hash


class Complex(db.Model):
    """
    Complex Model
    """
    __tablename__ = 'complex'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
        }
