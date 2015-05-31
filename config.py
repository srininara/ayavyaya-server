import os
basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'expense.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://grihasthi_app:grihasthi_app1!@localhost/grihasthi_db'
SQLALCHEMY_ECHO=False
SQLALCHEMY_POOL_SIZE = 15
DEBUG = True
