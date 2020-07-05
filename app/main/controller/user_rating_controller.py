from flask import request
from flask_restplus import Resource
import json

from ..util.dtos import UserRatingDto
from ..util.decorator import token_required
from ..service.user_rating_service import mark_movie_watched, rate_movie

api = UserRatingDto.api
_movie_watched = UserRatingDto.movie_watched
_user_rating = UserRatingDto.user_rating


@api.route('/rate')
class UserRate(Resource):
    @api.doc('Rate a movie', security='apikey')
    @token_required
    @api.expect(_user_rating, validate=True)
    def post(current_user, self):
        """Rate a movie """
        data = request.json
        data['user_id'] = current_user['user_id']
        return rate_movie(data=data)


@api.route('/mark_watched')
class UserMarkWatched(Resource):
    @api.doc('Mark a movie watched', security='apikey')
    @api.expect(_movie_watched, validate=True)
    @token_required
    def post(current_user, self):
        """Mark a movie watched"""
        data = request.json
        data['user_id'] = current_user['user_id']
        return mark_movie_watched(data=data)