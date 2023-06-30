from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('owner.id'))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'))
    type = db.Column(db.String(20))
    currency = db.Column(db.Integer)
    status = db.Column(db.String(7))

