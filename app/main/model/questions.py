from . import Identity
from .. import db


class Questions(Identity):
    __tabelname__ = "questions"
    text = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    locale = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)
