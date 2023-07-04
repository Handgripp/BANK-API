from datetime import datetime
import uuid
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Transaction(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_number_from = db.Column(db.String(26), db.ForeignKey('account.account_number'))
    account_number_to = db.Column(db.String(26), db.ForeignKey('account.account_number'))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(8))


