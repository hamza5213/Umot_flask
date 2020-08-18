from . import Identity
from .. import db


class Person(Identity):
    __tabelname__ = "person"
    name = db.Column(db.String, nullable=False)
    popularity = db.Column(db.Float, nullable=False)
