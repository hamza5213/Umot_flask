from . import Identity
from .. import db


class PlatformRecommendation(Identity):
    __tabelname__ = "platform_recomendation"
    user_id = db.Column(db.Integer, nullable=False)
    question_response = db.Column(db.String, nullable=False)
    created_on = db.Column(db.String, nullable=False)
    platforms = db.Column(db.String, nullable=False)
