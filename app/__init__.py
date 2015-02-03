import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from gevent.monkey import patch_all
from psycogreen.gevent import patch_psycopg

from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

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

from app.apis import api_month_expense_stats
from app.apis import api_expense
from app.apis import api_category
from app.apis import api_frequency
from app.apis import api_nature
from app import app_fe
