from datetime import datetime
import uuid
from sqlalchemy import Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Account(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_number_from = db.Column(UUID(as_uuid=True), db.ForeignKey('account_number_from.id'))
    account_number_to = db.Column(UUID(as_uuid=True), db.ForeignKey('account_number_to.id'))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(8))


