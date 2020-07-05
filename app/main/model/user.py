from . import Identity
from .. import db, flask_bcrypt
import datetime
import jwt
from ..config import key


class User(Identity):
    """ User Model for storing user related details """
    __tablename__ = "user"

    public_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    user_type = db.Column(db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    num_of_children = db.Column(db.Integer)
    country = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50))
    dp_url = db.Column(db.String(1000))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
