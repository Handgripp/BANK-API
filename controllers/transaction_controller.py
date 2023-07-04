from flask import Blueprint, jsonify, request

from controllers.auth_controller import token_required
from repositories.transaction_repository import TransactionRepository

transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route("/transactions", methods=["POST"])
@token_required
def transactions(current_user):
    transaction_type = request.args.get('type')

    if transaction_type == 'transfer':
        account_number_from = request.json['account_number_from']
        account_number_to = request.json['account_number_to']
        amount = request.json['amount']

        transaction = TransactionRepository.transaction(account_number_from, account_number_to, amount)

        if transaction:
            return jsonify({'message': 'Transaction created'}), 201
        else:
            return jsonify({'error': 'Transaction failed'}), 400

    elif transaction_type == 'deposit':
        account_number_to = request.json['account_number_to']
        amount = request.json['amount']

        transaction = TransactionRepository.deposit(account_number_to, amount)

        if transaction:
            return jsonify({'message': 'Deposit created'}), 201
        else:
            return jsonify({'error': 'Deposit failed'}), 400

    else:
        return jsonify({'error': 'Invalid transaction type'}), 400
