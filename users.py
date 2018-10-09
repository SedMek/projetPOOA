class Series:
    """
    This class defines series objects
    """
    id_counter = 0

    def __init__(self, id, title, nb_seasons):
        self.id = id  # Id is the same ID from TMDB. It's already unique by definition in TMDB
        self.title = title
        self.nb_seasons = nb_seasons

    def __repr__(self):
        return """
        id: {}
        title: {}
        nb_seasons: {}
        """.format(self.id, self.title, self.nb_seasons)

    def __str__(self):
        return self.__repr__()


class User:
    """
    This class defines user objects
    """
    id_counter = 0

    def __init__(self, first_name, last_name, login, fav_series):
        self.id = User.id_counter + 1  # TODO Maybe we should use Hash code for the id
        User.id_counter += 1
        self.login = login  # TODO Maybe we should use Hash code for login
        # TODO Should we store the password in the user instance, or keep it in a seperate file
        self.first_name = first_name
        self.last_name = last_name
        self.fav_series = fav_series

    def add_series(self, series_id):
        if series_id == 0:  # if the user doesn't want to add any series
            pass
        else:
            self.fav_series.append(series_id)

    def __repr__(self):
        return "id: {}\nfirst_name: {}\nlast_name: {}\nlogin: {}\nfav_series: {}".format(self.id, self.first_name,
                                                                                         self.last_name, self.login,
                                                                                         self.fav_series)

    def __str__(self):
        return self.__repr__()


def main():
    seddik = User("Seddik", "Mekki", "SedMek", [])
    print(seddik)


if __name__ == "__main__":
    main()
