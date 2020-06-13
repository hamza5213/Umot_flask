from . import Identity
from .. import db


class MovieSearch(Identity):
    __tabelname__ = "movie_search"
    tmdb_id = db.Column(db.Integer, nullable=False)
    vote_count = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    original_title = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date)
