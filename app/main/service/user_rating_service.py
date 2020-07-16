from app.main import db
from app.main.model.user_rating import UserRating
from ..model.movie_raw_complete import MovieRawComplete
from ..util.validators import Validator

def mark_movie_watched(data):
    movie = MovieRawComplete.query.filter_by(tmdb_id=data['movie_id']).first()
    if not movie:
        return { "success": False, "message": "Invalid Movie ID."}, 400

    ratingEntry = UserRating.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    if not ratingEntry:
        new_rating_entry = UserRating(user_id=data['user_id'], movie_id=data['movie_id'], rating=None)
        save_changes(new_rating_entry)
        return { "success": True, "message": "Movie Marked Watched"}, 201
    else:
        return { "success": True, "message": "This movie is already marked watched by the user"}, 200

def rate_movie(data):
    movie = MovieRawComplete.query.filter_by(tmdb_id=data['movie_id']).first()
    if not movie:
        return { "success": False, "message": "Invalid Movie ID."}, 400
    if not Validator.validateMovieRating(rating=data['rating']):
        return { "success": False, "message": "Rating must be between 0 and 5"}, 400

    ratingEntry = UserRating.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    if not ratingEntry:
        new_rating_entry = UserRating(user_id=data['user_id'], movie_id=data['movie_id'], rating=data['rating'])
        save_changes(new_rating_entry)
        return { "success": True, "message": "Movie Rated successfully."}, 200
    else:
        ratingEntry.rating = data['rating']
        db.session.commit()
        return { "success": True, "message": "Movie Rated successfully."}, 200

def get_watched_history(data):
    return UserRating.query.filter_by(user_id=data['user_id']).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()