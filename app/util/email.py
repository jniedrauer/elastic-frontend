import smtplib
from email.mime.text import MIMEText
from .. import app


def send_email(email, subject, html):
    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['From'] = app.config['ADMIN_EMAIL']
    msg['To'] = email
    s = smtplib.SMTP('localhost')
    s.sendmail(app.config['ADMIN_EMAIL'], [email], msg.as_string())
    s.quit()
