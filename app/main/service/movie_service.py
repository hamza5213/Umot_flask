import json

from ..model.movie_imdb_genres import MovieImdbGenres
from ..model.movie_raw_complete import MovieRawComplete
from ..model.movie_search import MovieSearch
from ..model.person import Person
from ..model.providers import Providers
from ..model.service_provider import ServiceProvider
from ..model.tags import Tags
from ..service import es_service


def get_all():
    movies = MovieSearch.query.filter(MovieSearch.release_date != '0001-01-01 BC').order_by(MovieSearch.id).all()
    return movies


def search_actor(name):
    actors = Person.query.filter(Person.name_lower.like('%' + name + '%')).order_by(Person.popularity.desc()).limit(
        20).all()
    result = [];
    for actor in actors:
        result.append({'name': actor.name, 'id': actor.id})
    return result


def search_tags(name):
    tags = Tags.query.filter(Tags.name.like('%' + name + '%')).limit(20).all()
    result = [];
    for tag in tags:
        result.append({'name': tag.name, 'id': tag.id})
    return result


def get(id, locale='US'):
    movie_raw = MovieRawComplete.query.outerjoin(MovieImdbGenres).filter(MovieRawComplete.tmdb_id == id).first()

    results = ServiceProvider.query \
        .join(Providers) \
        .filter(ServiceProvider.tmdb_id == (id), ServiceProvider.locale == locale, ServiceProvider.batch_id == 1).all()

    providers = []

    for res in results:
        providers.append({
            'category': res.category,
            'img': res.img,
            'price': res.price,
            'quality': res.quality,
            'url': res.url,
            'provider_name': res.providers.name
        })

    movie = {
        'background_img': movie_raw.backdrop_path,
        'credits': json.loads(movie_raw.credits),
        'id': movie_raw.id,
        'original_title': movie_raw.original_title,
        'poster_img': movie_raw.poster_path,
        'release_date': movie_raw.release_date,
        'runtime': movie_raw.runtime,
        'title': movie_raw.title,
        'providers': providers,
        'videos': json.loads(movie_raw.videos)["results"],
        'synopsis': movie_raw.overview,
        'genres': [genre.name for genre in movie_raw.movie_imdb_genres] if len(movie_raw.movie_imdb_genres) > 0 else [
            genre["name"] for genre in json.loads(movie_raw.genres)]
    }

    return movie


def search_movie(query):
    return es_service.search(query)


def search_all(query, locale='US'):
    movies = es_service.search_all(query)
    ids = [movie['tmdb_id'] for movie in movies]
    results = ServiceProvider.query \
        .join(Providers) \
        .filter(ServiceProvider.tmdb_id.in_(ids), ServiceProvider.locale == locale, ServiceProvider.batch_id == 1).all()

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
