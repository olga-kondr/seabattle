import os
import random
from datetime import datetime
from flaskr import app, get_session, set_session
from flaskr.sea_battle.board import Board
from flaskr.models import db, Session, Game, Player, Move
from flask import (
    redirect,
    url_for,
    jsonify,
    request,
    abort,
    make_response
)


@app.route("/api/move/<game_id>", methods=['POST'])
def move(game_id):
    the_game = Game.query.filter_by(id=game_id).first_or_404()

    if not app.config['DEBUG']:
        if the_game.session.key != get_session().key:
            return make_response(jsonify(error='Your game was not found'), 404)

    if the_game.winner is not None:
        app.logger.warning('The game is over')
        return make_response(jsonify(error='The game is over'), 400)

    if not request.is_json:
        app.logger.warning('Incorrect request content type')
        abort(415)
        return

    data = request.get_json()

    player = data.get('player')
    if player == Player.First.name:
        player = Player.First
    elif player == Player.Second.name:
        player = Player.Second
    else:
        app.logger.warning('Missing correct player')
        return make_response(jsonify(error='Missing correct player'), 400)
    if player != the_game.move:
        app.logger.warning('Not your turn')
        return make_response(jsonify(error='Not your turn'), 400)

    x = data.get('x')
    y = data.get('y')

    the_move = make_move(player, x, y, the_game)
    is_winner = find_victory(player, the_game)

    if is_winner:
        save_winner(player, the_game)

    db.session.add(the_move)
    db.session.add(the_game)
    db.session.commit()

    response = {
        'winner': str(player.name) if is_winner else None,
        'move': str(the_game.move.name) if not is_winner else None,
        'score': the_move.score
    }

    return response


def make_move(player, x, y, the_game):
    if player == Player.First:
        board = Board.load(the_game.board2)
        is_hit = board.shot(x, y)
        if not is_hit:
            the_game.move = Player.Second
    else:
        board = Board.load(the_game.board1)
        random.seed(os.urandom(128))
        x = random.randint(0, board.board_size - 1)
        y = random.randint(0, board.board_size - 1)
        is_hit = board.shot(x, y)
        if not is_hit:
            the_game.move = Player.First
        
    the_move = Move(player=player, move_x=x, move_y=y, score=10 if is_hit else 0)
    the_game.moves.append(the_move)

    return the_move


def find_victory(player, the_game):
    coords = [(m.move_x, m.move_y) for m in the_game.moves if m.player == player]
    if player == Player.First:
        board = Board.load(the_game.board2)
    else:
        board = Board.load(the_game.board1)
    return board.is_win(coords)


def save_winner(player, the_game):
    the_game.finished_at = datetime.now()
    the_game.winner = player
