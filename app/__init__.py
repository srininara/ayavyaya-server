import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from gevent.monkey import patch_all
from psycogreen.gevent import patch_psycopg

patch_all()
patch_psycopg()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = BASE_DIR + '/fe/'
app = Flask(__name__, static_url_path='', static_folder=STATIC_DIR)
app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True

api = Api(app)

from app import api_expense
from app import api_month_expense_stats
from app import app_fe
