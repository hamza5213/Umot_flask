from . import Identity
from .. import db


class QuestionsPlatform(Identity):
    __tabelname__ = "questions_platform"
    text = db.Column(db.String, nullable=False)
    locale = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
