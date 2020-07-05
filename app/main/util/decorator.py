from functools import wraps
from flask import request

from app.main.service.auth_helper import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(token, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        user_type = token.get('user_type')
        if user_type != "admin":
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(token, *args, **kwargs)

    return decorated

def premium_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        user_type = token.get('user_type')
        if user_type != "premium":
            response_object = {
                'status': 'fail',
                'message': 'premium token required'
            }
            return response_object, 401

        return f(token, *args, **kwargs)

    return decorated