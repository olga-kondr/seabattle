import enum
from flaskr.models import db


class Player(enum.Enum):
    First = 1
    Second = 2


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    board1 = db.Column(db.Text)
    board2 = db.Column(db.Text)
    winner = db.Column(db.Enum(Player),  nullable=True)
    move = db.Column(db.Enum(Player),  nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    finished_at = db.Column(db.DateTime)
    
    session = db.relationship('Session', back_populates='games')
    moves = db.relationship('Move', back_populates='game')
