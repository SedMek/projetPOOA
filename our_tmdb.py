import requests
from pprint import pprint

api_key = "f3e96aa12213aa6d0925d98470ba6fec"
api_version = "3"


class Serie:
    def __init__(self, id):
        self.id = id
        self.serie_infos = requests.get('https://api.themoviedb.org/' + api_version + '/tv/' + str(
            id) + '?api_key=' + api_key + '&language=en-US').json()


class Season(Serie):
    def __init__(self, id, season_number):
        Serie.__init__(self, id)
        self.season_number = season_number
        self.season_infos = requests.get(
            'https://api.themoviedb.org/' + api_version + '/tv/' + str(id) + '/season/' + str(
                season_number) + '?api_key=' + api_key + '&language=en-US').json()


class Episode(Season):
    def __init__(self, id, season_number, episode_number):
        Season.__init__(self, id, season_number)
        self.episode_number = episode_number
        self.episode_infos = requests.get(
            'https://api.themoviedb.org/' + api_version + '/tv/' + str(id) + '/season/' + str(
                season_number) + '/episode/' + str(episode_number) + '?api_key=' + api_key + '&language=en-US').json()


class Search:
    def __init__(self, query, language="en-US"):
        self.query = query
        self.language = language
        self.basic_search_url = "http://api.themoviedb.org/" + api_version + "/search/tv?api_key=" + api_key + "&query=" + query + "&language" + self.language
        self.resp = requests.get(self.basic_search_url).json()
        self.total_pages = self.resp["total_pages"]

    def get_page(self, page=1):
        return requests.get(self.basic_search_url + "&page=" + str(page)).json()


def main():
    got = Serie(1399)
    pprint(got.serie_infos)


if __name__ == "__main__":
    main()


#new