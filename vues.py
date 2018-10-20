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


@app.route("/")
def home():
    fav_series_ids = get_fav_object()
    fav_series = [our_tmdb.Serie(i) for i in fav_series_ids]
    return render_template("index.html", fav_series=fav_series)


@app.route("/searchResult", methods=['GET', 'POST'])
def search():
    fav_series_ids = get_fav_object()
    fav_series = [our_tmdb.Serie(i) for i in fav_series_ids]
    # search_result_code 0 for no search issued, 1 for search with results and -1 for search without results -2 for empty search
    id_poster = dict()
    if request.method == "POST":
        if request.form["search"]:  # if the search query is not empty
            search_result = our_tmdb.Search(request.form["search"]).series
            if len(search_result) == 0:
                search_result_code = -1
            else:
                search_result_code = 1
                for serie in search_result:
                    try:
                        id_poster[serie.serie_infos["id"]] = POSTER_PATH + serie.serie_infos["poster_path"]
                    except:  # some series might not have posters
                        pass
        else:
            search_result_code = -2
    if request.method == "GET":
        pass  # TODO

    return render_template("search_result.html", id_poster=id_poster, search_result_code=search_result_code,
                           fav_series=fav_series)


@app.route("/addSeries/<int:series_id>")
def add_series_to_fav(series_id):
    fav_series_ids = get_fav_object()

    if series_id in fav_series_ids:  # if the series is already in the list, remove it from the list
        fav_series_ids.remove(series_id)

    fav_series_ids.insert(0, series_id)
    save_fav_object(fav_series_ids)
    return redirect(url_for("home"))


@app.route("/removeSeries/<int:series_id>")
def remove_series_from_fav(series_id):
    fav_series_ids = get_fav_object()

    if series_id in fav_series_ids:  # if the series is already in the list, remove it from the list
        fav_series_ids.remove(series_id)

    save_fav_object(fav_series_ids)
    return redirect(url_for("home"))


@app.route("/clear_fav")
def clear_fav():
    save_fav_object([])
    return redirect(url_for("home"))


@app.route("/seriesInfo/<int:series_id>")
def series_info(series_id):
    series = our_tmdb.Serie(series_id)
    fav_series_ids = get_fav_object()
    fav_series = [our_tmdb.Serie(i) for i in fav_series_ids]
    return render_template("series_info.html", series=series, fav_series=fav_series)


# filters
@app.template_filter('join_networks')
def join_networks(series):
    network_names = []
    for i in range(len(series.serie_infos["networks"])):
        network_names.append(series.serie_infos["networks"][i]["name"])
    return " &".join(network_names)


if __name__ == "__main__":
    app.run(debug=True)
