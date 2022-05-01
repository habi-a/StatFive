from . import db
from .user import User
from .team import Team


class Stats(db.Model):
    """
    Stats Model
    """
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    kilometre = db.Column(db.Integer, nullable=False)
    passe = db.Column(db.Integer, nullable=False)
    but = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship(User, backref='stats')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'kilometre': self.kilometre,
            'passe': self.passe,
            'but': self.but
        }

