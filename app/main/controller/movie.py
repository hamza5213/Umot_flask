from flask_restplus import Resource, reqparse

from ..service import logging_service
from ..service import movie_service
from ..util.dtos import get_response, MovieDto

_logger = logging_service.get_logger(__name__)
api = MovieDto.api
_movie_search = MovieDto.movie_search
_response = MovieDto.movie_response


@api.route('/search')
class Search(Resource):

    @api.doc('Movie Title')
    @api.param('query', 'Movie Title')
    @api.marshal_with(_response)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('query', type=str, help='query cannot be null')
            args = parser.parse_args()
            query = args['query']

            if query != None and query != '':
                data = movie_service.search_movie(query)
                return get_response(200, data, 'Success', True)
            else:
                return get_response(300, [], 'query is null', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/search/all')
class SearchAll(Resource):

    @api.doc('Movie Title')
    @api.param('query', 'Movie Title')
    @api.marshal_with(_response)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('query', type=str, help='query cannot be null')
            args = parser.parse_args()
            query = args['query']

            if query != None and query != '':
                data = movie_service.search_all(query)
                return get_response(200, data, 'Success', True)
            else:
                return get_response(300, [], 'query is null', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/<int:id>')
class SearchAll(Resource):

    @api.doc('Get Movie')
    @api.marshal_with(_response)
    def get(self, id):
        try:
            if id > 0:
                movie = movie_service.get(id)
                return get_response(200, movie, 'Success', True)
            else:
                return get_response(300, [], 'Invalid Id', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/sync_es')
class SyncES(Resource):

    @api.doc('Sync DataBase with Elastic Search')
    @api.marshal_with(_response)
    def get(self):
        try:

            movie_service.sync_es()
            return get_response(200, [], 'Success', True)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)
