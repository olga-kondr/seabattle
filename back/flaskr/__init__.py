import datetime
from flask import Flask, jsonify
from flaskr.models import db

app = Flask(__name__)
app.config.from_object("flaskr.config.Config")
app.permanent_session_lifetime = datetime.timedelta(days=365)

db.init_app(app)

from flaskr.models import *


@app.route("/")
def hello_world():
    return jsonify(hello="world")
