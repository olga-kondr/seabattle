import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.flaskenv', verbose=True)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
