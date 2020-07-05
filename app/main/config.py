import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ZQoDwgqKJgLvrCui9sQ65uUrvZV1DKYzAzL')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ABC123ssi@127.0.0.1:5432/umot'
    ELASTIC_SEARCH_HOST = 'http://127.0.0.1:9200/'
    SEARCH_INDEX = 'movie_search_2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class QAConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ABC123umot@18.222.13.116:5432/umot'
    ELASTIC_SEARCH_HOST = 'http://127.0.0.1:9200/'
    SEARCH_INDEX = 'movie_search'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ''
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = True
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    qa=QAConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY