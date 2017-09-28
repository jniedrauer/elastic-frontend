from flask_wtf import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import DataRequired, Email


class UsernamePasswordForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EmailPasswordForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
