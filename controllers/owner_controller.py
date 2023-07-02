import datetime
import jwt
from flask import jsonify, Blueprint, request, current_app
from jsonschema import validate, ValidationError
from controllers.auth_controller import token_required
from models.owner_model import Owner
from repositories.owner_repository import OwnerRepository
from schemas.owner_schema import create_owner_schema
from services.email_service import send_mail

owner_blueprint = Blueprint('owner', __name__)


@owner_blueprint.route("/owners", methods=["POST"])
def create_owner():
    rabbitmq = current_app.config["RABBITMQ"]
    data = request.json
    try:
        validate(data, create_owner_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    email = Owner.query.filter_by(email=data['email']).first()

    if email:
        return jsonify({'error': 'Owner with that email already exists'}), 409

    OwnerRepository.create_owner(
        data['first_name'],
        data['last_name'],
        data['email'],
        data['password']
    )
    token = jwt.encode(
        {'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
         'user_type': 'client'},
        'thisissecret',
        algorithm='HS256')
    send_mail(data['email'], "Email confirmation",
              f"<html><body><a href='http://127.0.0.1:5000/owners/confirm-email?token={token}'>URL</a></body></html>")
    rabbitmq.send(body="ping", routing_key="ping.message")

    return jsonify({'message': 'New user created'}), 201


@owner_blueprint.route("/owners/<user_id>", methods=["GET"])
@token_required
def get_one(current_user, user_id):
    user_data = OwnerRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200


@owner_blueprint.route("/owners/confirm-email", methods=["GET"])
def confirm_email():
    token = request.args.get('token')
    data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
    if not token:
        return jsonify({'error': 'Bad request'}), 400

    owner = Owner.query.filter_by(email=data['email']).first()

    if not owner or owner.is_email_confirmed:
        return jsonify({'error': 'Bad request'}), 400

    OwnerRepository.confirm_email(owner)

    return jsonify({'message': 'Email confirmed'}), 200
