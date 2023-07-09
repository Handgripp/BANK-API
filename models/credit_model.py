import uuid
from sqlalchemy import Date
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Credit(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'))
    account_number = db.Column(db.String(26), db.ForeignKey('account.account_number'))
    amount_credit = db.Column(db.Integer)
    loan_term = db.Column(db.Integer)
    interest_rate = db.Column(db.Integer)


class CreditPayments(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_id = db.Column(UUID(as_uuid=True), db.ForeignKey('credit.id'))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'))
    account_number = db.Column(db.String(26), db.ForeignKey('account.account_number'))
    payment_date = db.Column(Date)
    amount_credit = db.Column(db.Integer)
    remaining_installments = db.Column(db.Integer)
    loan_payment = db.Column(db.Integer)
    is_paid = db.Column(db.Boolean, default=False)
