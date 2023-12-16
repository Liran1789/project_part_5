import requests
from data_manager.data_manager_interface import DataManagerInterface
from data_manager.data_models import db, User, Movie, Review


class SQLiteDataManager(DataManagerInterface):

    def __init__(self):
        self.db = db

    def get_all_users(self):
        user_list = self.db.session.query(User).order_by(User.user_id).all()
        return user_list

    def add_new_user(self, username):
        self.db.session.add(username)
        self.db.session.commit()

    def get_user_movies(self, user_id):
        movie_lst = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
        return movie_lst

    def add_movie(self, user_id, movie_name):
        API_KEY = '62c2fad2'
        res = requests.get(f'https://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}')
        movie_info = res.json()
        movie = Movie(name=movie_info['Title'],
                      director=movie_info['Director'],
                      year=movie_info['Year'],
                      rating=movie_info['imdbRating'],
                      poster=movie_info['Poster'],
                      user_id=user_id)
        self.db.session.add(movie)
        self.db.session.commit()

    def delete_movie(self, user_id, movie_id):
        Movie.query.filter(Movie.user_id == user_id).filter(Movie.movie_id == movie_id).delete()
        self.db.session.commit()

    def update_movie_rating(self, movie, rating):
        movie.rating = int(rating)
        self.db.session.commit()

    def get_movie(self, movie_id):
        movie = self.db.session.get(Movie, movie_id)
        return movie

    def get_user(self, user_id):
        user = self.db.session.get(User, user_id)
        return user

    def add_review(self, user_id, movie_id, review_text, rating):
        review = Review(user_id=user_id,
                        movie_id=movie_id,
                        review_text=review_text,
                        rating=rating)
        self.db.session.add(review)
        self.db.session.commit()
