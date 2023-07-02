from flask import jsonify, Blueprint, request
from jsonschema import validate, ValidationError

from controllers.auth_controller import token_required
from models.client_model import Client
from repositories.client_repository import ClientRepository
from schemas.client_schema import create_client_schema

client_blueprint = Blueprint('client', __name__)


@client_blueprint.route("/clients", methods=["POST"])
def create_client():
    data = request.json
    try:
        validate(data, create_client_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    email = Client.query.filter_by(email=data['email']).first()
    pesel = Client.query.filter_by(pesel=data['pesel']).first()

    if email:
        return jsonify({'error': 'Client with that email already exists'}), 409

    if pesel:
        return jsonify({'error': 'Client with that pesel already exists'}), 409


    ClientRepository.create_client(
        data['first_name'],
        data['last_name'],
        data['pesel'],
        data['is_gender_male'],
        data['email'],
        data['password']
    )

    return jsonify({'message': 'New user created'}), 201


@client_blueprint.route("/clients/<user_id>", methods=["GET"])
@token_required
def get_one(current_user, user_id):
    user_data = ClientRepository.get_one_by_id(user_id)

    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200
