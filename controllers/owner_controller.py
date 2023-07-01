from flask import jsonify, Blueprint, request
from jsonschema import validate, ValidationError
from models.owner_model import Owner
from repositories.owner_repository import OwnerRepository
from schemas.owner_schema import create_owner_schema

owner_blueprint = Blueprint('owner', __name__)


@owner_blueprint.route("/owner", methods=["POST"])
def create_owner():

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

    return jsonify({'message': 'New user created'}), 201
