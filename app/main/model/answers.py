from . import Identity
from .. import db


class Answers(Identity):
    __tabelname__ = "answers"
    text = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    locale = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
