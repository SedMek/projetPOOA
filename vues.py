from flask import Flask, render_template, request, url_for, redirect
import our_tmdb
import pickle

app = Flask(__name__)
app.secret_key = "hello".encode()

POSTER_PATH = "https://image.tmdb.org/t/p/w200/"


# this variable should be global so the user can remember the series that he has already added


def get_fav_object():
    with open('static/fav', 'rb') as fav:
        my_unpickler = pickle.Unpickler(fav)
        fav_list = my_unpickler.load()
        return fav_list


def save_fav_object(fav_series):
    with open('static/fav', 'wb') as fav:
        my_pickler = pickle.Pickler(fav)
        my_pickler.dump(fav_series)


def set_fav_posters(list_of_series):
    """
    takes a list of series (Id) and returns a list of their posters
    """
    posters = []
    for i in range(len(list_of_series)):
        posters.append(POSTER_PATH + our_tmdb.Serie(list_of_series[i]).serie_infos[
            "poster_path"])
    return posters


@app.route("/", methods=['GET', 'POST'])
def home():
    fav_series = get_fav_object()
    search_result_code = 0  # 0 for no search issued, 1 for search with results and -1 for search without results
    id_poster = dict()
    if request.method == "POST":
        # fav_series.insert(0, request.form["search"])  # to add the new series in first position
        search_result = our_tmdb.Search(request.form["search"]).get_page()["results"]
        if len(search_result) == 0:
            search_result_code = -1
        else:
            search_result_code = 1
            for series in search_result:
                try:
                    id_poster[series["id"]] = POSTER_PATH + series["poster_path"]
                except:  # some series might not have posters
                    pass
    if request.method == "GET":
        pass  # TODO

    posters = set_fav_posters(fav_series)
    return render_template("index.html", posters=posters, id_poster=id_poster, search_result_code=search_result_code)


@app.route("/addSeries/<int:series_id>")
def add_series_to_fav(series_id):
    fav_series = get_fav_object()

    if series_id in fav_series:  # if the series is already in the list, remove it from the list
        fav_series.remove(series_id)

    fav_series.insert(0, series_id)
    save_fav_object(fav_series)
    return redirect(url_for("home"))


@app.route("/clear_fav")
def clear_fav():
    save_fav_object([])
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
