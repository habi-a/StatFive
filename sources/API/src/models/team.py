from . import db
from .match import Match


class Team(db.Model):
    """
    Team Model
    """
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class TeamHasMatchPlayed(db.Model):
    """
    TeamHasMatchPlayed Model
    """
    __tablename__ = 'team_has_match_played'

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_played.id'), primary_key=True)
    goals = db.Column(db.Integer, primary_key=True)
    possesion = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Integer, primary_key=True)
    ended = db.Column(db.Integer, primary_key=True)

    team: Team = db.relationship(Team, backref='team_match_played')
    match = db.relationship(Match, backref='team_match_played')

    def to_json(self):
        return {
            'match_id': self.match_id,
            'team_id': self.team_id,
            'goals': self.goals,
            'possesion': self.possesion,
            'color': self.color,
            'ended': self.ended,
        }


class TeamStats(db.Model):
    """
    TeamStats Model
    """
    __tablename__ = 'team_stats'

    id = db.Column(db.Integer, primary_key=True)
    km = db.Column(db.FLOAT, nullable=False)
    possesion = db.Column(db.FLOAT, nullable=False)
    passe = db.Column(db.Integer, nullable=False)
    but = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    team: Team = db.relationship(Team, backref='stats')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'km': self.km,
            'possesion': self.possesion,
            'passe': self.passe,
            'but': self.but
        }
