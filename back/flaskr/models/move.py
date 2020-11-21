from flaskr.models import db
from . import Player


class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    player = db.Column(db.Enum(Player),  nullable=True)
    move_x = db.Column(db.Integer)
    move_y = db.Column(db.Integer)
    score = db.Column(db.Integer)

    game = db.relationship('Game', back_populates='moves')
