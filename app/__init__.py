from flask import Blueprint
from flask_restplus import Api

from .main.controller.auth_controller import api as auth_ns
from .main.controller.movie import api as movie_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.user_rating_controller import api as user_rating_ns
from .main.controller.wish_list_controller import api as wish_list_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
          title='UMOT API',
          version='1.0',
          description='Umot API Endpoints',
          authorizations=authorizations
          )

api.add_namespace(movie_ns, path='/movie')
api.add_namespace(user_ns, path='/user')
api.add_namespace(user_rating_ns, path='/user_rating')
api.add_namespace(wish_list_ns, path='/wish_list')
api.add_namespace(auth_ns)
