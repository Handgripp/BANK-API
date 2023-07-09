import random
import string
from flask import jsonify, Blueprint, request
from jsonschema import validate, ValidationError
from controllers.auth_controller import token_required
from models.account_model import Account
from models.client_model import Client
from models.owner_model import Owner
from repositories.account_repository import AccountRepository
from schemas.account_schema import create_account_schema

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route("/accounts", methods=["POST"])
@token_required
def create_account(current_user):
    if current_user.status == "Deleted":
        return jsonify({'error': 'Bad request'}), 400

    data = request.json
    try:
        validate(data, create_account_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400

    user_type = current_user.user_type
    mail_confirmed_owner = None
    mail_confirmed_client = None

    if user_type == "owner":
        mail_confirmed_owner = Owner.query.filter_by(id=current_user.id, is_email_confirmed=True).first()
    else:
        mail_confirmed_client = Client.query.filter_by(id=current_user.id, is_email_confirmed=True).first()

    if not mail_confirmed_owner and not mail_confirmed_client:
        return jsonify({'error': 'Email not confirmed'}), 409

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


@account_blueprint.route("/accounts/<account_number>", methods=["GET"])
@token_required
def get_account(current_user, account_number):
    account_data = AccountRepository.get_account_by_id(account_number)

    if not account_data:
        return jsonify({'error': 'No account found!'}), 404

    return jsonify(account_data), 200


@account_blueprint.route("/accounts", methods=["GET"])
@token_required
def get_accounts(current_user):
    account_data = AccountRepository.get_accounts_by_user_id(current_user.id)

    if not account_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(account_data), 200


@account_blueprint.route("/accounts/<account_number>", methods=["DELETE"])
@token_required
def delete_account(current_user, account_number):
    delete_type = request.args.get('type')
    account = Account.query.filter_by(account_number=account_number).first()
    if account.status == "Deleted":
        return jsonify({'error': 'Bad request'}), 400

    if delete_type == "soft":
        AccountRepository.soft_delete(account_number)
        return jsonify({'message': 'Account deleted'}), 200

    elif delete_type == "hard":
        AccountRepository.hard_delete(account_number)
        return jsonify({'message': 'Account deleted'}), 200

    return jsonify({'error': 'User has not been deleted '}), 404
