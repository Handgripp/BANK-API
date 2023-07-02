from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Account(db.Model):
    account_number = db.Column(db.String(26), primary_key=True)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('owner.id'), nullable=True)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'), nullable=True)
    account_type = db.Column(Enum('personal', 'savings', name='account_type'))
    currency = db.Column(Enum('PLN', 'EUR', 'GBP', 'CHF', 'USD', name='currency'))
    balance = db.Column(db.Integer, default=0)
    status = db.Column(Enum('Active', 'Deleted', name='status'), default="Active")

