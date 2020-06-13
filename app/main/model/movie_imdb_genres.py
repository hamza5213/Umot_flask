from . import Identity
from .. import db


class MovieImdbGenres(Identity):
    __tabelname__ = "movie_imdb_genres"
    tmdb_id = db.Column(db.Integer, db.ForeignKey("movie_raw_complete.tmdb_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    imdb_id = db.Column(db.String, nullable=False)
    movie_raw_complete = db.relationship("MovieRawComplete")
