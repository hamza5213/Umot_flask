# class AwardsCount(db.Model):
#     __tabelname__ = "awards_count"
#     tmdb_id = db.Column(db.Integer, nullable=False, primary_key=True)
#     count = db.Column(db.Integer, db.ForeignKey('movie_raw_complete.tmdb_id') ,nullable=False)
#     movie_raw_complete = db.relationship("MovieRawComplete")
