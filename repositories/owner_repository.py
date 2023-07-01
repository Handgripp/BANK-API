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
