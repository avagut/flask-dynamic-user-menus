"""Create the main app structure of the Macros System."""

import os.path
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# import logging
# logging.basicConfig(filename='error.log',level=logging.DEBUG)

app = Flask(__name__, instance_relative_config=True)
if os.path.isfile('instance/flask.cfg'):
    app.config.from_pyfile('flask.cfg')
else:
    app.config.from_object('config')
    
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
bcrypt = Bcrypt(app)
#toolbar = DebugToolbarExtension(app)

from src.users.models import User #keep it low to prevent circular ref
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(userid):
    """Specify the user id for the user being loaded at login."""
    return User.query.filter(User.user_id == int(userid)).first()

# toolbar = DebugToolbarExtension(app)

# BluePrints Listing
from src.users.views import users_blueprint
from src.navigation.views import nav_blueprint

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(nav_blueprint)
