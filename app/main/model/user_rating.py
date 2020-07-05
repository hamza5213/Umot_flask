from . import Identity
from .. import db


class UserRating(Identity):
    """ User Model for storing user ratings and which movies has watched """
    __tablename__ = "user_rating"

    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer)
