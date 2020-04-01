#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from ayavyaya import app
from ayavyaya import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()


#/Users/narayasr/SriniRoot/MyStore/Code/altProgrammingLangs/python/my_virtualenvs/my_app_env/bin/python3.3
