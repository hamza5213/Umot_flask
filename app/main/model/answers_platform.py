from . import Identity
from .. import db


class AnswersPlatform(Identity):
    __tabelname__ = "answers_platform"
    text = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    locale = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
