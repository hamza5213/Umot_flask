from sqlalchemy.dialects.postgresql import JSONB

from . import Identity
from .. import db


class MovieRawComplete(Identity):
    __tabelname__ = "movie_raw_complete"
    tmdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    original_title = db.Column(db.String, nullable=False)
    original_language = db.Column(db.String, nullable=False)
    backdrop_path = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    poster_path = db.Column(db.String, nullable=False)
    overview = db.Column(db.String, nullable=False)
    runtime = db.Column(db.INTEGER, nullable=False)
    videos = db.Column(db.String, nullable=False)
    credits = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date)
    spoken_languages_json = db.Column(JSONB)
    spoken_languages = db.Column(db.String)
    movie_imdb_genres = db.relationship("MovieImdbGenres", back_populates="movie_raw_complete")
    awards_count = db.relationship("AwardsCount", uselist=False, backref="movie_raw_complete")
    keywords_json = db.Column(JSONB)
    credits_json = db.Column(JSONB)
    release_date_c = db.Column(db.Date)
    vote_count = db.Column(db.Integer)


class AwardsCount(db.Model):
    __tabelname__ = "awards_count"
    tmdb_id = db.Column(db.Integer, db.ForeignKey('movie_raw_complete.tmdb_id'), nullable=False, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
