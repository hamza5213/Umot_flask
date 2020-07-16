from flask import request
from flask_restplus import Resource
import json

from ..util.dtos import UserRatingDto, get_response
from ..util.decorator import token_required
from ..service.user_rating_service import mark_movie_watched, rate_movie, get_watched_history
from ..service import logging_service

api = UserRatingDto.api
_logger = logging_service.get_logger(__name__)
_movie_watched = UserRatingDto.movie_watched
_watched_history = UserRatingDto.watched_history
_user_rating = UserRatingDto.user_rating


@api.route('/rate')
class UserRate(Resource):
    @api.doc('Rate a movie', security='apikey')
    @token_required
    @api.expect(_user_rating, validate=True)
    def post(current_user, self):
        """Rate a movie """
        try:
            data = request.json
            data['user_id'] = current_user['user_id']
            return rate_movie(data=data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/mark_watched')
class UserMarkWatched(Resource):
    @api.doc('Mark a movie watched', security='apikey')
    @api.expect(_movie_watched, validate=True)
    @token_required
    def post(current_user, self):
        """Mark a movie watched"""
        try:
            data = request.json
            data['user_id'] = current_user['user_id']
            return mark_movie_watched(data=data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)

@api.route('/watched_history')
class WatchHistory(Resource):
    @api.doc('list_of_watched_movies', security='apikey')
    @token_required
    @api.marshal_list_with(_watched_history, envelope='data')
    def get(current_user, self):
        """List all watched movies"""
        try:
            data = {}
            data['user_id'] = current_user['user_id']
            return get_watched_history(data)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)