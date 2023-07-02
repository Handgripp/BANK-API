from flask import current_app

rabbitmq = current_app.config['RABBITMQ']


@rabbitmq.queue(routing_key='ping.message')
def process_message(message):
    print('Received message:', message)
