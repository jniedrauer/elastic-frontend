from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import DataRequired, Email


class EmailPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
