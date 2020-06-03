import os

from flask import render_template
from flask_mail import Message

from app import create_app
from app import mail


def send_email(recipient, subject, template, **kwargs):
    try:
        app = os.getenv('APP_NAME', 'FLASK')
        msg = Message(
            subject + '' + app,
            sender=os.getenv('MAIL_DEFAULT_SENDER', 'flask-admin@gmail.com'),
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)
        return True
    except Exception as e:
        print('Failed to send email: ' + str(e))
        return False
