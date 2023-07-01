from flask import jsonify, Blueprint, request
from jsonschema import validate, ValidationError
from models.client_model import Client
from repositories.client_repository import ClientRepository
from schemas.client_schema import create_client_schema

client_blueprint = Blueprint('client', __name__)


@client_blueprint.route("/client", methods=["POST"])
def create_client():
    data = request.json
    try:
        validate(data, create_client_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    email = Client.query.filter_by(email=data['email']).first()

    if email:
        return jsonify({'error': 'Owner with that email already exists'}), 409

    ClientRepository.create_client(
        data['first_name'],
        data['last_name'],
        data['pesel'],
        data['is_gender_male'],
        data['email'],
        data['password']
    )

    return jsonify({'message': 'New user created'}), 201
