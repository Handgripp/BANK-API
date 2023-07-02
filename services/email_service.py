from flask import current_app
from flask_mail import Message


def send_mail(send_to, subject, body):
    mail = current_app.config['MAIL']
    msg = Message(recipients=[send_to])
    msg.html = body
    msg.subject = subject
    mail.send(msg)
