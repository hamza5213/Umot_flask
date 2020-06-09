from flask import Blueprint
from flask_restplus import Api

from .main.controller.movie import api as movie_ns

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='UMOT API',
          version='1.0',
          description='machine learning api'
          )

api.add_namespace(movie_ns, path='/movie')
