from . import Identity
from .. import db


class PlatformScores(Identity):
    __tabelname__ = "platform_scores"
    provider_id = db.Column(db.Integer, nullable=False)
    answer_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
