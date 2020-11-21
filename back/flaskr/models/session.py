from flaskr.models import db


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    games = db.relationship('Game', back_populates='session')

