from . import db


class Match(db.Model):
    """
    Match Model
    """
    __tablename__ = 'match_played'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    ground = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String, nullable=False)
    finish = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'ground': self.ground,
            'path': self.path,
            'finish': self.finish
        }
