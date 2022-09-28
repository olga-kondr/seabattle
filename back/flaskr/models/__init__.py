from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .game import Game, Player
from .move import Move
from .session import Session
