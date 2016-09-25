'''This is the main module which holds the entire ayavyaya server code.'''
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
from gevent.monkey import patch_all
patch_all()

# noinspection PyPep8
import os

# noinspection PyPep8
from flask import Flask
# noinspection PyPep8
from werkzeug.contrib.fixers import ProxyFix

# noinspection PyPep8
from psycogreen.gevent import patch_psycopg
patch_psycopg()

# noinspection PyPep8
from flask.ext.restful import Api
# noinspection PyPep8
from flask.ext.sqlalchemy import SQLAlchemy


# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = BASE_DIR + '/fe/'
app = Flask(__name__, static_url_path='', static_folder=STATIC_DIR)
app.config.from_object('ayavyaya.default_config')
try:
    app.config.from_envvar('AYAVYAYA_SETTINGS')
except RuntimeError:
    pass


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
        handler = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=log_file_size,
                                                       backupCount=log_file_count)
        handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)

db = SQLAlchemy(app)
db.engine.pool._use_threadlocal = True

api = Api(app)

# noinspection PyPep8
from ayavyaya.apis import api_month_expense_stats
# noinspection PyPep8
from ayavyaya.apis import api_expense
# noinspection PyPep8
from ayavyaya.apis import api_category
# noinspection PyPep8
from ayavyaya.apis import api_nature
# noinspection PyPep8
from ayavyaya import app_fe
