from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_new_user(self, username):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_name):
        pass

