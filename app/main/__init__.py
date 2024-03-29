from elasticsearch import Elasticsearch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

es = None
current_configs = None
db = SQLAlchemy()


def create_app(config_name):
    global es, current_configs
    app = Flask(__name__)
    current_configs = config_by_name[config_name]
    app.config.from_object(current_configs)
    db.init_app(app)
    es = Elasticsearch([current_configs.ELASTIC_SEARCH_HOST])

    return app


def get_current_configs():
    return current_configs


def get_es_instance():
    return es
