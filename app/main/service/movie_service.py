from ..model.movie_search import MovieSearch
from ..model.providers import Providers
from ..model.service_provider import ServiceProvider
from ..service import es_service


def get_all():
    movies = MovieSearch.query.filter(MovieSearch.release_date != '0001-01-01 BC').order_by(MovieSearch.id).all()
    return movies


def search_movie(query):
    return es_service.search(query)


def search_all(query, locale='US'):
    movies = es_service.search_all(query)
    ids = [movie['tmdb_id'] for movie in movies]
    results = ServiceProvider.query \
        .join(Providers) \
        .filter(ServiceProvider.tmdb_id.in_(ids), ServiceProvider.locale == locale).all()

    providers = {}

    for res in results:
        if res.category == 'Ads':
            continue
        if res.tmdb_id not in providers:
            providers[res.tmdb_id] = []

        providers[res.tmdb_id].append({
            'category': res.category,
            'img': res.img,
            'price': res.price,
            'quality': res.quality,
            'url': res.url,
            'provider_name': res.providers.name
        })

    for movie in movies:
        movie['providers'] = None
        if movie['tmdb_id'] in providers:
            movie['providers'] = providers[movie['tmdb_id']]

    return movies


def sync_es():
    movies = get_all()
    es_service.add_bulk(movies)
