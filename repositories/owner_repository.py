import uuid
from werkzeug.security import generate_password_hash
from models.owner_model import Owner, db


class OwnerRepository:

    @staticmethod
    def create_owner(first_name, last_name, email, password):
        hashed_password = generate_password_hash(password, method='sha256')

        new_owner = Owner(id=str(uuid.uuid4()), first_name=first_name,
                          last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_owner)
        db.session.commit()

    @staticmethod
    def get_one_by_id(user_id):
        owner = Owner.query.get(user_id)
        if not owner:
            return None

        user_data = {
            'id': owner.id,
            'first_name': owner.first_name,
            'last_name': owner.last_name,
            'created_at': owner.created_at,
            'updated_at': owner.updated_at,
            'email': owner.email,
            'status': owner.email,
            'is_email_confirmed': owner.is_email_confirmed
        }

        return user_data

    @staticmethod
    def confirm_email(owner):
        owner.is_email_confirmed = True
        db.session.commit()


