from flask import redirect, render_template, url_for
from flask_login import login_required
from . import app


@app.route('/')
@login_required
def index():
    return 'hello'
