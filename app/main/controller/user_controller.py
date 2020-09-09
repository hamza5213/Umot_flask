from flask import request
from flask_restplus import Resource

from ..service import logging_service
from ..service.user_service import save_new_user, get_all_users, get_a_user, update_existing_user, make_user_premium
from ..util.decorator import admin_token_required, token_required
from ..util.dtos import UserDto, get_response

api = UserDto.api
_logger = logging_service.get_logger(__name__)
_user = UserDto.user
_user_register = UserDto.user_register
_user_update = UserDto.user_update


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users', security='apikey')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(current_user, self):
        """List all registered users"""
        try:
            return get_all_users()
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user_register, validate=True)
    def post(self):
        """Creates a new User """
        try:
            data = request.json
            return save_new_user(data=data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        try:
            user = get_a_user(public_id)
            if not user:
                api.abort(404)
            else:
                return user
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)

@api.route('/update/')
class UpdateUser(Resource):

    @api.doc('Update User Information!', security='apikey')
    @api.expect(_user_update, validate=True)
    @token_required
    def post(current_user, self):
        """Update an existing user"""
        try:
            data = request.json
            data['user_id'] = current_user['user_id']
            return update_existing_user(data=data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/update/premium/')
class UpdateUserPremium(Resource):

    @api.doc('Update User to Pemium', security='apikey')
    @token_required
    def post(current_user, self):
        """Update an existing user to premium status"""
        try:
            make_user_premium(current_user['user_id'])
            return get_response(500, [], 'Success', False)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)
