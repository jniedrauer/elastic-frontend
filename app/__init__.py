import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if os.environ.get('FLASK_CONFIG'):
    app.config.from_envvar('FLASK_CONFIG')
else:
    app.config.from_object('flask_config_debug')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from .models import User
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

from . import views
