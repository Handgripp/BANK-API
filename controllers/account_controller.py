import random
import string

from flask import jsonify, Blueprint, request
from jsonschema import validate, ValidationError
from controllers.auth_controller import token_required

from repositories.account_repository import AccountRepository
from schemas.account_schema import create_account_schema

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route("/accounts", methods=["POST"])
@token_required
def create_account(current_user):
    data = request.json
    try:
        validate(data, create_account_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    user_type = current_user.user_type

    owner_id = None
    client_id = None

    if user_type == "owner":
        owner_id = current_user.id
    else:
        client_id = current_user.id

    account_number = ''.join(random.choices(string.digits, k=26))

    AccountRepository.create_account(
        account_number,
        data['account_type'],
        data['currency'],
        owner_id,
        client_id
    )

    return jsonify({'message': 'New account created'}), 201
