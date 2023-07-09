import json
from datetime import date

from flask import current_app

from models.client_model import Client
from models.credit_model import CreditPayments
from models.account_model import Account
from extensions import db


def process_credit_payments():
    current_date = date.today()

    credit_payments = CreditPayments.query.filter_by(payment_date=current_date).all()

    for payment in credit_payments:

        accounts = Account.query.filter_by(account_number=payment.account_number).first()
        if accounts:
            if accounts.balance >= payment.loan_payment and not payment.is_paid:

                accounts.balance -= payment.loan_payment
                payment.is_paid = True
            elif accounts.balance < payment.loan_payment and not payment.is_paid:
                email = Client.query.filter_by(id=accounts.client_id).first()
                rabbitmq = current_app.config["RABBITMQ"]
                mail = {
                    'email': email.email,
                    'subject': "Loan payment",
                    'body': "You have not paid your loan installment"
                }
                rabbitmq.send_message(json.dumps(mail))

    db.session.commit()
