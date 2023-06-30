import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from extensions import db


class Owner(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180))
    status = db.Column(db.String(7))
    is_email_confirmed = db.Column(db.Boolean, default=False)

