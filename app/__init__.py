from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Create and configure app
# [...]

bcrypt = Bcrypt(app)

from .models import User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "signin"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()
