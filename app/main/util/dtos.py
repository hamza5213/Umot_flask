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


def get_response(statusCode, data, message, success):
    return {
        "statusCode": statusCode,
        'data': json.dumps(data),
        "message": message,
        "success": success
    }
