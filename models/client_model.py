import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Client(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    is_gender_male = db.Column(db.Boolean)
    pesel = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180))
    status = db.Column(Enum('Active', 'Deleted', name='status'), default="Active")
    is_email_confirmed = db.Column(db.Boolean, default=False)

