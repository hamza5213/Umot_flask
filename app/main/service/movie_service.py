from ..model.movie_search import MovieSearch
from ..service import es_service


def get_all():
    movies = MovieSearch.query.filter(MovieSearch.release_date != '0001-01-01 BC').order_by(MovieSearch.id).all()
    return movies


def search_movie(query):
    return es_service.search(query)


def sync_es():
    movies = get_all()
    es_service.add_bulk(movies)
