from flask import current_app, Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from . import login_manager, bcrypt, db
from .forms import EmailForm, EmailPasswordForm, PasswordForm
from .util import ts, send_email
from .models import User


auth = Blueprint('auth', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()

    if form.validate_on_submit():
        current_app.logger.debug('Login attempt for %s', form.email.data)
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.login'))


@auth.route('/accounts/create', methods=['GET', 'POST'])
@login_required
def create_account():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        current_app.logger.info('User registered: %s', form.email.data)
        user = User(
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            return 'User already exists'

        # Now we'll send the email confirmation link
        subject = 'Confirm your email'

        token = ts.dumps(form.email.data, salt=current_app.config['INVITE_KEY'])

        confirm_url = url_for(
            'auth.confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url,
            admin_email=current_app.config['ADMIN_EMAIL'])

        success = send_email(form.email.data, subject, html, logger=current_app.logger)
        if not success:
            current_app.logger.error('Email send failed')

        return redirect(url_for('index'))

    current_app.logger.info('Invalid entry')
    return render_template('accounts/create.html', form=form)


@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt=current_app.config['INVITE_KEY'], max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = 'Password reset requested'

        token = ts.dumps(user.email, salt=current_app.config['RESET_KEY'])

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url,
            admin_email=current_app.config['ADMIN_EMAIL'])

        send_email(user.email, subject, html, logger=app.logger)

        return redirect(url_for('index'))
    return render_template('reset.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt=current_app.config['RESET_KEY'], max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('reset_with_token.html', form=form, token=token)
