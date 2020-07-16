from flask import request
from flask_restplus import Resource
import json

from ..util.dtos import WishListDto, get_response
from ..util.decorator import premium_token_required
from ..service.wish_list_service import add_movie_to_wish_list, get_wish_list
from ..service import logging_service

api = WishListDto.api
_logger = logging_service.get_logger(__name__)
_wish_list = WishListDto.wish_list


@api.route('/')
class WishList(Resource):
    @api.doc('add_movie_to_wish_list', security='apikey')
    @premium_token_required
    @api.expect(_wish_list, validate=True)
    def post(current_user, self):
        """ Add Movie to Wish List """
        try:
            data = request.json
            data['user_id'] = current_user['user_id']
            return add_movie_to_wish_list(data=data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)

    @api.doc('movies_in_wish_list', security='apikey')
    @premium_token_required
    @api.marshal_list_with(_wish_list, envelope='data')
    def get(current_user, self):
        """Get all movies in wish list"""
        try:
            data = {}
            data['user_id'] = current_user['user_id']
            return get_wish_list(data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


