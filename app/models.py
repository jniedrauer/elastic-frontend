import datetime
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
