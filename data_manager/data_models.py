from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), unique=True)
    movies = db.relationship('Movie', backref='user', lazy='select')
    reviews = db.relationship('Review', backref='user', lazy='select')

    def __repr__(self):
        return f"{self.name}"


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.String)
    rating = db.Column(db.Integer)
    poster = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    reviews = db.relationship('Review', backref='movie', lazy='select')

    def __repr__(self):
        return f"{self.name} was produced by {self.director}(Rating: {self.rating})"


class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    review_text = db.Column(db.String)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.review_text} | User: {self.user_id} (Rating: {self.rating})"
