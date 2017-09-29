import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if os.environ.get('FLASK_CONFIG'):
    app.config.from_envvar('FLASK_CONFIG')
else:
    app.config.from_object('flask_config_debug')


bcrypt = Bcrypt(app)


db = SQLAlchemy(app)
from .models import User
db.create_all()


from flask_login import LoginManager
from .models import User
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

from .auth import auth
app.register_blueprint(auth)

from . import views
