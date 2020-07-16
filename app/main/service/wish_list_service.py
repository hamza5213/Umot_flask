from app.main import db
from app.main.model.wish_list import WishList
from ..model.movie_raw_complete import MovieRawComplete

def add_movie_to_wish_list(data):
    movie = MovieRawComplete.query.filter_by(tmdb_id=data['movie_id']).first()
    if not movie:
        return { "success": False, "message": "Invalid Movie ID."}, 400

    wishlistEntry = WishList.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    if not wishlistEntry:
        new_wish_list_entry = WishList(user_id=data['user_id'], movie_id=data['movie_id'])
        save_changes(new_wish_list_entry)
        return { "success": True, "message": "Movie added to wishlist"}, 201
    else:
        return { "success": True, "message": "This movie is already added in the wishlist"}, 200

def get_wish_list(data):
    return WishList.query.filter_by(user_id=data['user_id']).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()