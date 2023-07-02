import uuid
from werkzeug.security import generate_password_hash
from models.client_model import Client, db


class ClientRepository:

    @staticmethod
    def create_client(first_name, last_name, pesel, is_gender_male, email, password):
        hashed_password = generate_password_hash(password, method='sha256')

        new_owner = Client(id=str(uuid.uuid4()), first_name=first_name,
                           last_name=last_name, is_gender_male=is_gender_male,
                           pesel=pesel, email=email, password=hashed_password)
        db.session.add(new_owner)
        db.session.commit()

    @staticmethod
    def get_one_by_id(user_id):
        client = Client.query.get(user_id)
        if not client:
            return None

        user_data = {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'created_at': client.created_at,
            'updated_at': client.updated_at,
            'email': client.email,
            'status': client.email,
            'is_email_confirmed': client.is_email_confirmed,
            'is_gender_male': client.is_gender_male,
            'pesel': client.pesel
        }

        return user_data
