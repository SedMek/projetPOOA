import requests
from pprint import pprint
import storage_db

api_key = "f3e96aa12213aa6d0925d98470ba6fec"
api_version = "3"
POSTER_PATH = "https://image.tmdb.org/t/p/w200/"


class tmdbException(Exception):
    """define a class of exceptions to raise in case of invalid requests or response"""
    pass


class User:
    def __init__(self, user_object):
        self.first_name = user_object["first_name"]
        self.last_name = user_object["last_name"]
        self.login = user_object["login"]
        self.favourite_series = user_object["favourite_series"]
        self.email_notifications = user_object["email_notifications"]
        self.browser_notifications = user_object["browser_notifications"]

    def add_series_to_fav(self, series_id):
        if series_id in self.favourite_series:  # if the id already exists, remove it
            self.favourite_series.remove(series_id)

        self.favourite_series.insert(0, series_id)  # always add it in first position
        storage_db.update_user_fav_series(self)

    def remove_series_from_fav(self, series_id):
        if series_id in self.favourite_series:
            self.favourite_series.remove(series_id)
            storage_db.update_user_fav_series(self)

    def clear_fav(self):
        self.favourite_series = []
        storage_db.update_user_fav_series(self)

    def update_settings(self, **kwargs):
        self.email_notifications = "checkbox-email" in kwargs.keys()
        self.browser_notifications = "checkbox-browser" in kwargs.keys()
        storage_db.update_notification_settings(self)
        if kwargs["new_password"]:
            storage_db.update_password_in_db(self.login, kwargs["new_password"])


class Series:
    def __init__(self, id):
        self.id = id
        self.series_info = requests.get('https://api.themoviedb.org/' + api_version + '/tv/' + str(
            id) + '?api_key=' + api_key + '&language=en-US').json()
        self.id = id
        l = list(self.series_info.keys())
        """Cette boucle transofrme les attributs du json en attributs de la classe Series"""
        for i in range(len(l)):
            exec("self." + l[i] + "=self.series_info['" + l[i] + "']")
        if "status_code" in l and int(self.series_info["status_code"]) >= 2:
            raise tmdbException("You have reached the request limit allowed by TheMovieDB. Please wait...")


class Season(Series):
    def __init__(self, id, season_number):
        Series.__init__(self, id)
        self.season_number = season_number
        self.season_info = requests.get(
            'https://api.themoviedb.org/' + api_version + '/tv/' + str(id) + '/season/' + str(
                season_number) + '?api_key=' + api_key + '&language=en-US').json()


class Episode(Season):
    def __init__(self, id, season_number, episode_number):
        Season.__init__(self, id, season_number)
        self.episode_number = episode_number
        self.episode_info = requests.get(
            'https://api.themoviedb.org/' + api_version + '/tv/' + str(id) + '/season/' + str(
                season_number) + '/episode/' + str(episode_number) + '?api_key=' + api_key + '&language=en-US').json()
        print('https://api.themoviedb.org/' + api_version + '/tv/' + str(id) + '/season/' + str(
            season_number) + '/episode/' + str(episode_number) + '?api_key=' + api_key + '&language=en-US')


class Search:
    def __init__(self, query="", language="en-US"):
        self.query = query
        self.language = language
        self.basic_search_url = "http://api.themoviedb.org/" + api_version + "/search/tv?api_key=" + api_key + "&query=" + query + "&language" + self.language
        self.results = self.get_page(self)["results"]
        self.series_poster = dict()
        for result in self.results:
            try:
                self.series_poster[result['id']] = POSTER_PATH + result['poster_path']
            except:
                pass

    def get_page(self, page=1):
        return requests.get(self.basic_search_url + "&page=" + str(page)).json()


def main():
    got = Series(1399)
    pprint(got.name)


if __name__ == "__main__":
    main()

