import json
import requests
from data_manager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):

    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as file1:
            info = json.load(file1)

        users_list = {key: value['name'] for key, value in info.items()}

        return users_list

    def get_user_movies(self, user_id):
        with open(self.filename, "r") as file1:
            info = json.load(file1)

        user_movies_list = {field['id']: field['name'] for key, value in info.items() if int(key) == user_id for k, v in
                            value.items() if type(v) == list for field in v}

        return user_movies_list

    def add_new_user(self, name):
        with open(self.filename, "r") as file1:
            info = json.load(file1)

        _new_id = len(info) + 1
        new_dict = {'name': name, 'movies': []}
        info[_new_id] = new_dict

        with open(self.filename, "w") as outfile:
            json.dump(info, outfile, indent=4)

    def add_movie(self, user_id, movie_name):

        API_KEY = '62c2fad2'
        res = requests.get(f'https://www.omdbapi.com/?apikey={API_KEY}&t={movie_name}')
        movie_info = res.json()

        new_movie = {
            "id": "",
            "name": movie_info['Title'],
            "director": movie_info['Director'],
            "year": movie_info['Year'],
            "rating": movie_info['imdbRating']
        }

        with open(self.filename, "r") as file1:
            info = json.load(file1)

        for key, value in info.items():
            if int(key) == user_id:
                for k, v in value.items():
                    if type(v) == list:
                        new_movie["id"] = (len(v) + 1)
                        v.append(new_movie)

        with open(self.filename, "w") as outfile:
            json.dump(info, outfile, indent=4)

    def update_movie_rating(self, user_id, movie_id, new_rating):
        with open(self.filename, "r") as file1:
            info = json.load(file1)

        for key, value in info.items():
            if int(key) == user_id:
                for k, v in value.items():
                    if type(v) == list:
                        v[int(movie_id) - 1]['rating'] = new_rating

        with open(self.filename, "w") as outfile:
            json.dump(info, outfile, indent=4)

    def delete_movie(self, user_id, movie_id):
        with open(self.filename, "r") as file1:
            info = json.load(file1)

        for key, value in info.items():
            if int(key) == user_id:
                for k, v in value.items():
                    if type(v) == list:
                        v.pop(int(movie_id - 1))

        with open(self.filename, "w") as outfile:
            json.dump(info, outfile, indent=4)
