from . import Identity
from .. import db


class GenreScores(Identity):
    __tabelname__ = "genre_scores"
    answer_id = db.Column(db.Integer, nullable=False)
    comedy = db.Column(db.Integer, nullable=False)
    drama = db.Column(db.Integer, nullable=False)
    horror = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Integer, nullable=False)
    fantasy = db.Column(db.Integer, nullable=False)
    film_noir = db.Column(db.Integer, nullable=False)
    animation = db.Column(db.Integer, nullable=False)
    western = db.Column(db.Integer, nullable=False)
    documentary = db.Column(db.Integer, nullable=False)
    thriller = db.Column(db.Integer, nullable=False)
    adventure = db.Column(db.Integer, nullable=False)
    war = db.Column(db.Integer, nullable=False)
    sci_fi = db.Column(db.Integer, nullable=False)
    biography = db.Column(db.Integer, nullable=False)
    crime = db.Column(db.Integer, nullable=False)
    romance = db.Column(db.Integer, nullable=False)
    mystery = db.Column(db.Integer, nullable=False)
    history = db.Column(db.Integer, nullable=False)
    family = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.Integer, nullable=False)
    musical = db.Column(db.Integer, nullable=False)
    music = db.Column(db.Integer, nullable=False)
    adult = db.Column(db.Integer, nullable=False)
    news = db.Column(db.Integer, nullable=False)
    game_show = db.Column(db.Integer, nullable=False)
