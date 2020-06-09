from ..model.movie_search import MovieSearch
from ..service import es_service


def get_all():
    movies = MovieSearch.query.order_by(MovieSearch.id).all()
    return movies


def search_movie(query):
    return es_service.search(query)


def sync_es():
    movies = get_all()
    es_service.add_bulk(movies)
