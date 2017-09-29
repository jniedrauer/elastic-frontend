from flask import redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required
from . import app, db
from .forms import EmailForm, EmailPasswordForm, PasswordForm
from .util import ts, send_email
from .models import User


@app.route('/')
def index():
    if current_user.is_authenticated:
        return 'authenticated'
    else:
        return redirect('/login', code=302)


@app.route('/accounts/create', methods=['GET', 'POST'])
def create_account():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        app.logger.info('User registered: %s', form.email.data)
        user = User(
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()

        # Now we'll send the email confirmation link
        subject = 'Confirm your email'

        token = ts.dumps(form.email.data, salt=app.config['INVITE_KEY'])

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'email/activate.html',
            confirm_url=confirm_url,
            admin_email=app.config['ADMIN_EMAIL'])

        success = send_email(form.email.data, subject, html, logger=app.logger)
        if not success:
            app.logger.error('Email send failed')

        return redirect(url_for('index'))

    app.logger.info('Invalid entry')
    return render_template('accounts/create.html', form=form)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt=app.config['INVITE_KEY'], max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()

    if form.validate_on_submit():
        app.logger.debug('Login attempt for %s', form.email.data)
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = 'Password reset requested'

        token = ts.dumps(user.email, salt=app.config['RESET_KEY'])

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url,
            admin_email=app.config['ADMIN_EMAIL'])

        send_email(user.email, subject, html, logger=app.logger)

        return redirect(url_for('index'))
    return render_template('reset.html', form=form)


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt=app.config['RESET_KEY'], max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reset_with_token.html', form=form, token=token)
