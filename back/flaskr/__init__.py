import datetime
from flask import Flask, jsonify
from flask import session as flask_session
from flaskr.models import db

app = Flask(__name__)
app.config.from_object("flaskr.config.Config")
app.permanent_session_lifetime = datetime.timedelta(days=365)

db.init_app(app)

@app.route("/_health")
def health():
    return jsonify(status='ok')


def get_session():
    session_key = flask_session.get('session')
    if not session_key:
        return None
    return Session.query.filter_by(key=session_key).first()


def set_session(session_obj):
    flask_session['session'] = session_obj.key


from flaskr.models import *
from flaskr.api import *
