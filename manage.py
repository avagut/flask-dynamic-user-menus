"""Flask Migrate Management Script."""
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import app,db

#Migrated Blueprints
from src.users import models
from src.navigation import models

if os.path.isfile('instance/flask.cfg'):
    app.config.from_pyfile('flask.cfg')
else:
    app.config.from_object('config')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    
#**Commands List**
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
# python manage.py db downgrade

