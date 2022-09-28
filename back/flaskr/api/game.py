from flaskr import app, get_session
from flaskr.sea_battle.board import Board
from flaskr.models import Game, Player
from flask import (
    jsonify,
)


@app.route("/api/game/<game_id>", methods=['GET'])
def game(game_id):
    the_game = Game.query.filter_by(id=game_id).first_or_404()
    
    if not app.config['DEBUG']:
        if the_game.session.key != get_session().key:
            return make_response(jsonify(error='Your game was not found'), 404)

    moves = the_game.moves

    response = {
        'winner': str(the_game.winner.name) if the_game.winner else None,
        'move': str(the_game.move.name),
        'board1': Board.load(the_game.board1).to_list(),
        'board2': hide_board(Board.load(the_game.board2).to_list(), moves),
        'created_at': the_game.created_at.isoformat(),
        'finished_at': the_game.finished_at.isoformat() if the_game.finished_at else None,
        'moves': [
            {
                'player': str(move.player.name),
                'x': move.move_x,
                'y': move.move_y,
                'score': move.score
            }
            for move in moves
        ]
    }

    return response


def hide_board(board, moves):
    moves_set = set()
    for m in moves:
        moves_set.add((m.move_x, m.move_y))

    for row_ind, row in enumerate(board):
        for col_ind, col in enumerate(board[row_ind]):
            if (row_ind, col_ind) not in moves_set:
                board[row_ind][col_ind] = '-'
                
    return board
