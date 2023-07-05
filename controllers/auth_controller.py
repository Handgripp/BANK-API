import datetime
from functools import wraps
import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from models.client_model import Client
from models.owner_model import Owner

auth_blueprint = Blueprint('login', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
            current_user = Owner.query.filter_by(id=data['id']).first()
            if not current_user:
                current_user = Client.query.filter_by(id=data['id']).first()
                if not current_user:
                    return jsonify({'error': 'User not found'}), 401
            current_user.user_type = data["user_type"]
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Token is invalid!'}), 401

    return decorated


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data['email'] or not data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401

    owner = Owner.query.filter_by(email=data['email']).first()
    client = Client.query.filter_by(email=data['email']).first()

    if owner and check_password_hash(owner.password, data['password']):
        if not owner.is_email_confirmed:
            return jsonify({'error': 'Email not confirmed'}), 401
        token = jwt.encode(
            {'id': str(owner.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
             'user_type': 'owner'},
            'thisissecret',
            algorithm='HS256')
        return jsonify({'token': token}), 200

    if client and check_password_hash(client.password, data['password']):
        if not client.is_email_confirmed:
            return jsonify({'error': 'Email not confirmed'}), 401
        token = jwt.encode(
            {'id': str(client.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
             'user_type': 'client'},
            'thisissecret',
            algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

