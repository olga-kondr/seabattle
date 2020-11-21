from flaskr import app, get_session, set_session
from flaskr.sea_battle.board import Board
from flaskr.models import db, Session, Game, Player
from flask import (
    redirect,
    url_for,
    jsonify,
    request,
    abort,
    make_response
)


@app.route("/api/start", methods=['POST'])
def start():
    if not request.is_json:
        app.logger.warning('Incorrect request content type')
        abort(415)
        return

    data = request.get_json()
    board_size = data.get('boardSize')
    if board_size is None:
        app.logger.warning('Missing board size')
        return make_response(jsonify(error='Missing boardSize'), 400)
    if board_size not in [10, 15]:
        app.logger.warning(f"Incorrect board size {board_size}")
        return make_response(jsonify(error='Incorrect boardSize'), 400)

    session = get_session()
    if not session:
        session = Session.create_session()
        set_session(session)

    board1 = Board(board_size).generate()
    board2 = Board(board_size).generate()

    game = Game(
        session=session, 
        board1=board1.to_json(), 
        board2=board2.to_json(),
        move=Player.First
    )
    
    db.session.add(game)
    db.session.commit()

    return redirect(url_for('game', game_id=game.id))



