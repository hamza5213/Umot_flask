from . import Identity
from .. import db


class MovieRawComplete(Identity):
    __tabelname__ = "movie_raw_complete"
    tmdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    original_title = db.Column(db.String, nullable=False)
    backdrop_path = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    poster_path = db.Column(db.String, nullable=False)
    overview = db.Column(db.String, nullable=False)
    runtime = db.Column(db.INTEGER, nullable=False)
    videos = db.Column(db.String, nullable=False)
    credits = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date)
    movie_imdb_genres = db.relationship("MovieImdbGenres", back_populates="movie_raw_complete")
