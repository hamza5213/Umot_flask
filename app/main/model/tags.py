from . import Identity
from .. import db


class Tags(Identity):
    __tabelname__ = "tags"
    name = db.Column(db.String, nullable=False)
