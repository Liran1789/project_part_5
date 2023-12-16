from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from data_manager.data_models import User, Movie, db
from data_manager.sql_data_manager import SQLiteDataManager

api_bp = Blueprint('api', __name__, template_folder="templates")
sql_data_manager = SQLiteDataManager()


@api_bp.route("/")
def index():
    return render_template('index.html')


@api_bp.route('/users', methods=['GET'])
def users():
    user_list = sql_data_manager.get_all_users()
    return render_template('users.html', users=user_list)


@api_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    elif request.method == 'POST':
        try:
            user_name = User(name=request.form['user_name'])
            sql_data_manager.add_new_user(user_name)
            return render_template('success.html'), 201
        except Exception as error:
            return render_template('error_page.html', error=error.__repr__())


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    movie_lst = sql_data_manager.get_user_movies(user_id)
    user_name = db.session.query(User).filter(User.user_id == user_id).first()
    return render_template('user_movies.html', movie_lst=movie_lst, user_id=user_id, user_name=user_name)


@api_bp.route('/users/<user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    try:
        movie_name = request.form['movie_name']
        sql_data_manager.add_movie(user_id, movie_name)
        return render_template('success.html'), 201
    except Exception as error:
        return render_template('error_page.html', error=error.__repr__())


@api_bp.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    try:
        sql_data_manager.delete_movie(user_id, movie_id)
        return render_template('success.html'), 201
    except Exception as error:
        return render_template('error_page.html', error=error.__repr__())


@api_bp.route('/users/<user_id>/update_movie_rating/<movie_id>', methods=['GET', 'POST'])
def update_movie_rating(user_id, movie_id):
    if request.method == 'GET':
        movie = sql_data_manager.get_movie(movie_id)
        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie_name=movie.name,
                               movie_director=movie.director, movie_year=movie.year, movie_rating=movie.rating,
                               movie_poster=movie.poster)
    elif request.method == 'POST':
        try:
            movie = sql_data_manager.get_movie(movie_id)
            new_rating = request.form['new_rating']
            sql_data_manager.update_movie_rating(movie, new_rating)
            return render_template('success.html'), 201
        except Exception as error:
            return render_template('error_page.html', error=error.__repr__())


@api_bp.route('/users/<user_id>/reviews/<movie_id>', methods=['GET', 'POST'])
def reviews(user_id, movie_id):
    if request.method == 'GET':
        user = sql_data_manager.get_user(user_id)
        movie = sql_data_manager.get_movie(movie_id)
        return render_template('reviews.html',
                               reviews=movie.reviews,
                               movie_name=movie.name,
                               user_id=user_id,
                               movie_id=movie_id,
                               user_name=user.name)
    elif request.method == 'POST':
        review_text = request.form['review']
        rating = request.form['rating']
        sql_data_manager.add_review(user_id, movie_id, review_text, rating)
        return render_template('success.html'), 201


@api_bp.route("/api/users")
def get_users():
    user_list = sql_data_manager.get_all_users()
    return jsonify(f'{user_list}')


@api_bp.route("/api/users/<user_id>/movies")
def get_user_movies(user_id):
    movie_lst = sql_data_manager.get_user_movies(user_id)
    return jsonify(f'{movie_lst}')


'''@api_bp.route("/api/users/<user_id>/movies")
def add_fav_movie(movie):
    movie = Movie(name=movie_info['Title'],
                  director=movie_info['Director'],
                  year=movie_info['Year'],
                  rating=movie_info['imdbRating'],
                  poster=movie_info['Poster'],
                  user_id=user_id)
    sql_data_manager.add_movie(user_id, movie_name)
    return render_template('success.html'), 201
'''
