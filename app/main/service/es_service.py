from elasticsearch import helpers

from .. import get_current_configs
from .. import get_es_instance


def add_bulk(model_list):
    es = get_es_instance()
    actions = get_actions(model_list)

    try:
        response = helpers.bulk(es, actions=actions)
        print(response)

    except Exception as e:
        raise e


def search(query):
    current_config = get_current_configs()
    search_index = current_config.SEARCH_INDEX
    es = get_es_instance()
    results = es.search(
        index=search_index,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "bool_prefix",
                    "fields": [
                        "title",
                        "title._2gram",
                        "title._3gram",
                        "original_title",
                        "original_title._2gram",
                        "original_title._3gram"
                    ]
                }
            },
            "sort": [
                {"vote_count": {"order": "desc"}},
                {"_score": {"order": "desc"}}
            ]
        },
    )

    return [movie["_source"] for movie in results['hits']['hits']]


def search_all(query, size=1000):
    current_config = get_current_configs()
    search_index = current_config.SEARCH_INDEX
    es = get_es_instance()
    results = es.search(
        index=search_index,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "bool_prefix",
                    "fields": [
                        "title",
                        "title._2gram",
                        "title._3gram",
                        "original_title",
                        "original_title._2gram",
                        "original_title._3gram"
                    ]
                }
            },
            "sort": [
                {"vote_count": {"order": "desc"}},
                {"_score": {"order": "desc"}}
            ]
        },
        size=size
    )

    return [movie["_source"] for movie in results['hits']['hits']]


def get_actions(model_list):
    current_config = get_current_configs()
    search_index = current_config.SEARCH_INDEX
    actions = []

    for model in model_list:
        action = {
            '_index': search_index,
            '_id': model.id,
            'doc_type': 'title',
            'id': model.id,
            'tmdb_id': model.tmdb_id,
            'img': model.img,
            'title': model.title,
            'original_title': model.original_title,
            'release_date': model.release_date,
            'vote_count': model.vote_count,
            'timeout': 30
        }
        actions.append(action)
    return actions
