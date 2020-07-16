from . import Identity
from .. import db


class WishList(Identity):
    """ Model for storing wish list """
    __tablename__ = "wish_list"

    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
