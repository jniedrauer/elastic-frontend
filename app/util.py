from itsdangerous import URLSafeTimedSerializer
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from . import app


ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def send_email(email, subject, html, logger=None):
    sgclient = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_APIKEY'])
    source = Email(app.config['NOREPLY_EMAIL'])
    dest = Email(email)
    content = Content('text/html', html)

    mail = Mail(source, subject, dest, content)

    if logger:
        logger.debug('Sending email from %s to %s', app.config['NOREPLY_EMAIL'], email)
    response = sgclient.client.mail.send.post(request_body=mail.get())
    if logger:
        logger.debug('Sendgrid code: %s, reply: %s', response.status_code, response.body)
    return response.status_code == 202
