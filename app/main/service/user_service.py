import datetime
import uuid

from app.main import db
from app.main.model.user import User
from app.main.service import db_operations
from ..util.validators import Validator


def save_new_user(data):
    if not Validator.validateEmail(data['email']):
        return { "success": False, "message": "Invalid Email Address."}, 400
    if not Validator.validateGender(data['gender']):
        return { "success": False, "message": "Invalid Gender. Gender value must be 'male', 'female' or 'other'."}, 400
    if not Validator.validateDOB(data['dob']):
        return { "success": False, "message": "Invalid date OR date format. Expected format: YYYY-MM-DD."}, 400
    if not Validator.validateJSON(data['platform_config']):
        return { "success": False, "message": "Platform JSON is not parseable."}, 400
    if not Validator.validateJSON(data['medium_config']):
        return { "success": False, "message": "Medium JSON is not parseable."}, 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id = str(uuid.uuid4()),
            email = data['email'],
            username = data['username'],
            password = data['password'],
            user_type = "regular",
            registered_on = datetime.datetime.utcnow(),
            gender = data['gender'],
            dob = data['dob'],
            num_of_children = data['num_of_children'] if "num_of_children" in data else None,
            country = data['country'],
            postcode = data['postcode'] if "postcode" in data else None,
            dp_url = data['dp_url'] if "dp_url" in data else None,
            platform_config = data['platform_config'] if "platform_config" in data else None,
            medium_config = data['medium_config'] if "medium_config" in data else None
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_existing_user(data):
    if not Validator.validateGender(data['gender']):
        return { "success": False, "message": "Invalid Gender. Gender value must be 'male', 'female' or 'other'."}, 400
    if not Validator.validateDOB(data['dob']):
        return { "success": False, "message": "Invalid date OR date format. Expected format: YYYY-MM-DD."}, 400
    if not Validator.validateJSON(data['platform_config']):
        return { "success": False, "message": "Platform JSON is not parseable."}, 400
    if not Validator.validateJSON(data['medium_config']):
        return { "success": False, "message": "Medium JSON is not parseable."}, 400
    
    user = User.query.filter_by(id=data['user_id']).first()
    if user:
        user.gender = data['gender']
        user.dob = data['dob']
        user.username = data['username']
        user.num_of_children = data['num_of_children'] if "num_of_children" in data else None
        user.country = data['country']
        user.postcode = data['postcode'] if "postcode" in data else None
        user.dp_url = data['dp_url'] if "dp_url" in data else None
        user.platform_config = data['platform_config'] if "platform_config" in data else None
        user.medium_config = data['medium_config'] if "medium_config" in data else None
        
        db.session.commit()
        return { "success": True, "message": "User updated successfully."}, 200
    else:
        response_object = {
            "success": False,
            'message': 'User does not exists.',
        }
        return response_object, 404


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def make_user_premium(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.user_type = 'premium'
        db_operations.add_to_db(user)
