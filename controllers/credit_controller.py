from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError

from models.account_model import Account
from models.credit_model import CreditPayments
from repositories.transaction_repository import TransactionRepository
from repositories.credit_repositories import CreditRepository
from controllers.auth_controller import token_required
from schemas.credit_schema import create_credit_schema

credit_blueprint = Blueprint('credit', __name__)


@credit_blueprint.route("/credits", methods=["POST"])
@token_required
def create_credit(current_user):
    data = request.json

    try:
        validate(data, create_credit_schema)
    except ValidationError as e:
        return jsonify({'error': 'Invalid request body', 'message': str(e)}), 400
    account_client = Account.query.filter_by(account_number=data["account_number_client"]).first()
    user_account = Account.query.filter(Account.client_id == current_user.id).all()
    if account_client not in user_account:
        return jsonify({'error': 'Forbidden'}), 403

    transaction = TransactionRepository.deposit(data["account_number_client"], data["amount_credit"])
    amount_credit = data['amount_credit'] + (data['amount_credit'] * 5 / 100)
    if transaction:
        credit = CreditRepository.create_credit(
            current_user.id,
            data['account_number_client'],
            amount_credit,
            data['loan_term'],
            5,
        )

        loan_payment = amount_credit / data['loan_term']
        start_date = datetime.strptime(data['payment_date'], "%Y-%m-%d")
        payment_dates = []
        for i in range(data['loan_term']):
            payment_date = start_date + relativedelta(months=i)
            payment_dates.append(payment_date)

        remaining_installments = data['loan_term']
        remaining_amount = amount_credit

        for payment_date in payment_dates:
            CreditRepository.credit_payments(
                credit,
                current_user.id,
                data['account_number_client'],
                payment_date.date(),
                remaining_amount,
                remaining_installments,
                loan_payment,
                False
            )
            remaining_installments -= 1
            remaining_amount -= loan_payment

        return jsonify({'message': 'Credit created'}), 201
    else:
        return jsonify({'error': 'Credit failed'}), 400


@credit_blueprint.route("/credits/<credit_id>", methods=["GET"])
@token_required
def credit_payments(current_user, credit_id):
    credit_id = CreditPayments.query.filter_by(credit_id=credit_id).first()
    if not credit_id:
        return jsonify({'error': "Bad request"}), 404

    for i in range(credit_id.loan_term, -1, -1):
        print(i)

    return jsonify({}), 201
