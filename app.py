from flask import Flask
from flask_mail import Mail
from extensions import db
from controllers.owner_controller import owner_blueprint
from controllers.client_controller import client_blueprint
from controllers.auth_controller import auth_blueprint
from controllers.account_controller import account_blueprint
# from flask_rabbitmq import RabbitMQ
from rabbitmq_pika_flask import RabbitMQ


def create_app():
    app = Flask(__name__)
    mail = Mail()
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'lorenzo.kovacek52@ethereal.emai'
    app.config['MAIL_USERNAME'] = 'lorenzo.kovacek52@ethereal.email'
    app.config['MAIL_PASSWORD'] = 'bkBFaJGekNkfXGPQvz'
    app.config['MQ_URL'] = "amqp://guest:guest@localhost:5672/"
    app.config['MQ_EXCHANGE'] = "topic_exchange"

    db.init_app(app)
    mail.init_app(app)
    rabbitmq = RabbitMQ(app, 'mail_queue')

    rabbitmq.send(body="ping", routing_key="ping.message")

    app.config['MAIL'] = mail
    app.config['RABBITMQ'] = rabbitmq

    with app.app_context():
        db.create_all()

    app.register_blueprint(owner_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(account_blueprint)

    return app
