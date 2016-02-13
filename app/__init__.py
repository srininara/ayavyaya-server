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

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        import logging
        log_file_path = app.config['LOG_FILE_PATH']
        log_file_size = app.config['LOG_FILE_SIZE']
        log_file_count = app.config['LOG_FILE_COUNT']
        log_format = app.config['LOG_FORMAT']
        log_level = app.config['LOG_LEVEL']
        handler = logging.handlers.RotatingFileHandler(log_file_path,maxBytes=log_file_size, backupCount=log_file_count)
        handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)

db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True

api = Api(app)

from app.apis import api_month_expense_stats
from app.apis import api_expense
from app.apis import api_category
from app.apis import api_frequency
from app.apis import api_nature
from app import app_fe
