import json

from flask_restplus import Namespace, fields


class MovieDto:
    api = Namespace('movie', description='Search Movie')

    movie_response = api.model('movie_response', {
        'statusCode': fields.String(required=True, description='Status Code'),
        'data': fields.String(required=True),
        'message': fields.String(required=True, description='Response'),
        'success': fields.String(required=True)
    })

    movie_search = api.model('movie_search', {
        'query': fields.String(required=True, description='Movie Title')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'user_type': fields.String(required=True, description='user type'),
        'public_id': fields.String(description='user Identifier'),
        'gender': fields.String(required=True, description='user gender'),
        'dob': fields.Date(required=True, description='user data of birth'),
        'num_of_children': fields.String(required=False, description='number of children a user has'),
        'country': fields.String(required=True, description='user country'),
        'postcode': fields.String(required=False, description='user postcode')
    })

    user_register = api.model('user_register', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'gender': fields.String(required=True, description='user gender'),
        'dob': fields.Date(required=True, description='user data of birth'),
        'num_of_children': fields.Integer(required=False, description='number of children a user has'),
        'country': fields.String(required=True, description='user country'),
        'postcode': fields.String(required=False, description='user postcode')
    })

def get_response(statusCode, data, message, success):
    return {
        "statusCode": statusCode,
        'data': json.dumps(data),
        "message": message,
        "success": success
    }
