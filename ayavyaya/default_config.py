import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

# Database config
# SQLALCHEMY_DATABASE_URI = 'postgresql://grihasthi_app:grihasthi_app1!@localhost/grihasthi_db'
# SQLALCHEMY_DATABASE_URI = 'postgresql://ayavyaya_app:ayavyaya_app1@localhost/ayavyaya_db'
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'postgresql://ayavyaya_dev:ayavyaya_dev@192.168.1.50/ayavyaya_dev'
SQLALCHEMY_POOL_SIZE = 15


DEBUG = True

# Logging config
LOG_FILE_PATH = os.path.join(basedir, 'logs/ayavyaya/app.log')
LOG_FILE_SIZE = 1000000
LOG_FILE_COUNT = 5
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s: line %(lineno)d]'
LOG_LEVEL = logging.INFO
