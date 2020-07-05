from . import Identity
from .. import db


class Recommendations(Identity):
    __tabelname__ = "recomendations"
    user_id = db.Column(db.Integer, nullable=False)
    question_response = db.Column(db.String, nullable=False)
    created_on = db.Column(db.String, nullable=False)
    movies = db.Column(db.String, nullable=False)
