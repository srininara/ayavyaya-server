#!/Users/narayasr/SriniRoot/MyStore/Code/altProgrammingLangs/python/my_virtualenvs/my_app_env/bin/python3.3
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app
from app import db

migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()
