import json

from flask_restplus import Namespace, fields


class MovieDto:
    api = Namespace('movie', description='Movie Related Operations')

    movie_response = api.model('movie_response', {
        'statusCode': fields.String(required=True, description='Status Code'),
        'data': fields.String(required=True),
        'message': fields.String(required=True, description='Response'),
        'success': fields.String(required=True)
    })

    movie_search = api.model('movie_search', {
        'query': fields.String(required=True, description='Movie Title')
    })
    submit_response = api.model('submit_response', {
        'response': fields.List(required=True, description='List of question and answers', cls_or_instance=fields.Raw,
                                min_items=1)
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
        'postcode': fields.String(required=False, description='user postcode'),
        'dp_url': fields.String(required=False, description='user display picture url'),
        'platform_config': fields.String(required=False, description='user selected platform in json'),
        'medium_config': fields.String(required=False, description='user selected medium in json')
    })

    user_register = api.model('user_register', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'gender': fields.String(required=True, description='user gender'),
        'dob': fields.Date(required=True, description='user data of birth'),
        'num_of_children': fields.Integer(required=False, description='number of children a user has'),
        'country': fields.String(required=True, description='user country'),
        'postcode': fields.String(required=False, description='user postcode'),
        'dp_url': fields.String(required=False, description='user display picture url'),
        'platform_config': fields.String(required=False, description='user selected platform in json'),
        'medium_config': fields.String(required=False, description='user selected medium in json')
    })

    user_update = api.model('user_update', {
        'gender': fields.String(required=True, description='user gender'),
        'dob': fields.Date(required=True, description='user data of birth'),
        'num_of_children': fields.Integer(required=False, description='number of children a user has'),
        'country': fields.String(required=True, description='user country'),
        'postcode': fields.String(required=False, description='user postcode'),
        'dp_url': fields.String(required=False, description='user display picture url'),
        'platform_config': fields.String(required=False, description='user selected platform in json'),
        'medium_config': fields.String(required=False, description='user selected medium in json')
    })

class UserRatingDto:
    api = Namespace('user_rating', description='user rate and mark a movie watched')

    movie_watched = api.model('movie_watched', {
        'movie_id': fields.Integer(required=False, description='movie ID')
    })

    watched_history = api.model('watched_history', {
        'movie_id': fields.Integer(required=True, description='movie ID')
    })

    user_rating = api.model('user_rating', {
        'movie_id': fields.Integer(required=False, description='movie ID'),
        'rating': fields.Integer(required=False, description='rating given by user')
    })

class WishListDto:
    api = Namespace('wish_list', description='user add movie to wish list and get list back')

    wish_list = api.model('wish_list', {
        'movie_id': fields.Integer(required=True, description='movie ID')
    })

def get_response(statusCode, data, message, success):
    return {
        'data': json.dumps(data),
        "message": message,
        "success": success
    }, statusCode
