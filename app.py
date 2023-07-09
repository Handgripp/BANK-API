from datetime import datetime
from flask import Flask
from credit_service import process_credit_payments
from extensions import db
from controllers.owner_controller import owner_blueprint
from controllers.client_controller import client_blueprint
from controllers.auth_controller import auth_blueprint
from controllers.account_controller import account_blueprint
from controllers.transaction_controller import transaction_blueprint
from controllers.credit_controller import credit_blueprint
from services.rabbitmq_service import RabbitMQ

rabbitmq_config = {
    'host': 'localhost',
    'port': 5672,
    'user': 'guest',
    'password': 'guest',
    'queue_name': 'mail_queue',
}


def check_credits(app):
    with app.app_context():
        process_credit_payments()
        print('Credits checked: %s' % datetime.now())


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SCHEDULER_API_ENABLED'] = True
    db.init_app(app)

    rabbitmq = RabbitMQ(rabbitmq_config)

    app.config['RABBITMQ'] = rabbitmq

    with app.app_context():
        db.create_all()

    app.register_blueprint(owner_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(transaction_blueprint)
    app.register_blueprint(credit_blueprint)

    return app