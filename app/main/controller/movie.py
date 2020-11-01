from flask_restplus import Resource, reqparse

from ..service import logging_service
from ..service import movie_service
from ..service.recommendation_service import submit_response, get_questions_list, \
    get_recommendations, get_platform_questions_list, submit_platform_response, get_platforms_recommendations
from ..util.decorator import token_required
from ..util.dtos import get_response, MovieDto

_logger = logging_service.get_logger(__name__)
api = MovieDto.api
_movie_search = MovieDto.movie_search
_response = MovieDto.movie_response
_movie_response = MovieDto.submit_response

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


@api.route('/actor_search')
class ActorSearch(Resource):

    @api.doc('Actor Name')
    @api.param('name', 'Actor Name')
    @api.marshal_with(_response)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='name cannot be null')
            args = parser.parse_args()
            query = args['name']

            if query != None and query != '':
                data = movie_service.search_actor(query)
                return get_response(200, data, 'Success', True)
            else:
                return get_response(300, [], 'query is null', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/tag_search')
class TagSearch(Resource):

    @api.doc('Tag Title')
    @api.param('title', 'Tag Title')
    @api.marshal_with(_response)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str, help='title cannot be null')
            args = parser.parse_args()
            query = args['title']

            if query != None and query != '':
                data = movie_service.search_tags(query)
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
    @api.param('country', 'Country')
    @api.marshal_with(_response)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('query', type=str, help='query cannot be null')
            parser.add_argument('country', type=str, help='country cannot be null')
            args = parser.parse_args()
            query = args['query']
            country = args['country']

            if query != None and query != '':
                data = movie_service.search_all(query, country)
                return get_response(200, data, 'Success', True)
            else:
                return get_response(300, [], 'query is null', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/<int:id>')
class GetMovie(Resource):

    @api.doc('Get Movie')
    @api.param('country', 'Country')
    @api.marshal_with(_response)
    def get(self, id):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('country', type=str, help='country cannot be null')
            args = parser.parse_args()
            country = args['country']
            if id > 0:
                movie = movie_service.get(id, country)
                return get_response(200, movie, 'Success', True)
            else:
                return get_response(300, [], 'Invalid Id', False)

        except Exception as e:
            _logger.error(e)
            return get_response(300, [], str(e), False)


@api.route('/recommendation/submit_response')
class SubmitResponse(Resource):

    @api.doc('Submit questionnaire response', security='apikey')
    @api.expect(_movie_response, validate=True)
    @token_required
    @api.marshal_with(_response)
    def post(current_user, self):

        response = api.payload['response']
        locale = api.payload['locale']

        if locale == 'null':
            locale = 'en'

        try:
            submit_response(response, locale, current_user['user_id'])
            return get_response(200, 'Success', 'Success', True)
        except Exception as e:
            return get_response(500, [], e, 'false')


@api.route('/platform_recommendation/submit_response')
class SubmitPlatformResponse(Resource):

    @api.doc('Submit questionnaire response', security='apikey')
    @api.expect(_movie_response, validate=True)
    @token_required
    @api.marshal_with(_response)
    def post(current_user, self):

        response = api.payload['response']
        locale = api.payload['locale']

        if locale == 'null':
            locale = 'en'

        try:
            res = submit_platform_response(response, locale, current_user['user_id'])
            return get_response(200, res, 'Success', True)
        except Exception as e:
            return get_response(500, [], e, 'false')


@api.route('/get_plaform_recommendation')
class GetPlatformRecommendation(Resource):

    @api.doc('Get Recommendation', security='apikey')
    @api.marshal_with(_response)
    @token_required
    def get(current_user, self):
        try:
            platforms = get_platforms_recommendations(current_user['user_id'])
            return get_response(200, platforms, 'Success', True)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/get_recommendation')
class GetRecommendation(Resource):

    @api.doc('Get Recommendation', security='apikey')
    @api.marshal_with(_response)
    @token_required
    def get(current_user, self):
        try:
            movies = get_recommendations(current_user['user_id'])
            return get_response(200, movies, 'Success', True)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/get_platform_question')
class GetPlatformQuestions(Resource):

    @api.doc('Get Platform Questions')
    @api.marshal_with(_response)
    @api.param('locale', 'The user locale')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locale', type=str, help='query cannot be null')
        args = parser.parse_args()
        locale = args['locale']
        if locale == None:
            locale = 'en'
        try:
            questions = get_platform_questions_list(locale)
            return get_response(200, questions, 'Success', True)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/get_question')
class GetQuestions(Resource):

    @api.doc('Get Questions')
    @api.marshal_with(_response)
    @api.param('locale', 'The user locale')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locale', type=str, help='query cannot be null')
        args = parser.parse_args()
        locale = args['locale']
        if locale == None:
            locale = 'en'

        try:
            questions = get_questions_list(locale)
            return get_response(200, questions, 'Success', True)
        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)


@api.route('/sync_es')
class SyncES(Resource):

    @api.doc('Sync DataBase with Elastic Search')
    @api.marshal_with(_response)
    def get(self):
        try:

            # movie_service.sync_es()
            return get_response(200, [], 'Success', True)

        except Exception as e:
            _logger.error(e)
            return get_response(500, [], str(e), False)
