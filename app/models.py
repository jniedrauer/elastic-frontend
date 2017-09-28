from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)


class User(db.Model):

    # [...] columns and properties

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
