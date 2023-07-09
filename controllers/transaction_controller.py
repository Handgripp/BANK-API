from flask import Blueprint, jsonify, request
from controllers.auth_controller import token_required
from models.account_model import Account
from models.transaction_model import Transaction
from repositories.transaction_repository import TransactionRepository
from services.nbpapi_service import CurrencyExchange

transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route("/transactions", methods=["POST"])
@token_required
def transactions(current_user):
    transaction_type = request.args.get('type')

    if transaction_type == 'transfer':
        account_number_from = request.json['account_number_from']
        account_number_to = request.json['account_number_to']
        amount = request.json['amount']
        account_from = Account.query.filter_by(account_number=account_number_from).first()
        account_to = Account.query.filter_by(account_number=account_number_to).first()
        user_account = Account.query.filter(Account.client_id == current_user.id).all()
        if account_from not in user_account:
            return jsonify({'error': 'Account not found'}), 404
        currency_from = CurrencyExchange(currency=account_from.currency)
        currency_to = CurrencyExchange(currency=account_to.currency)
        if not currency_from or not currency_to:
            return jsonify({'error': 'Bad Gateway'}), 502
        exchange_from = currency_from.get_currency()
        exchange_to = currency_to.get_currency()

        transaction = TransactionRepository.transaction(account_number_from, account_number_to, amount,
                                                        exchange_from, exchange_to)

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


@transaction_blueprint.route("/accounts/<account_number>/transactions/<transaction_id>", methods=["GET"])
@token_required
def get_transaction(current_user, transaction_id, account_number):
    transaction = TransactionRepository.get_transaction_by_id(transaction_id)

    if not str(transaction['id']) == str(transaction_id):
        return jsonify({'error': 'No transaction found'}), 404

    if not account_number == transaction['account_number_from']:
        return jsonify({'error': 'No account found'}), 404

    if not transaction:
        return jsonify({'error': 'No transaction found'}), 404

    return jsonify(transaction), 201


@transaction_blueprint.route("/accounts/<account_number>/transactions", methods=["GET"])
@token_required
def get_transactions(current_user, account_number):
    transaction = TransactionRepository.get_transactions_by_account(account_number)

    if not transaction:
        return jsonify({'error': 'No transaction found'}), 404

    return jsonify(transaction), 201
