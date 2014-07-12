import os
from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = BASE_DIR+'/fe/'
app = Flask(__name__, static_url_path='', static_folder=STATIC_DIR)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app)

from app import api_expense
from app import model_expense
from app import app_fe
