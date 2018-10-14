from flask import Flask, render_template, request, url_for, redirect
import our_tmdb

app = Flask(__name__)
app.secret_key = "hello".encode()

POSTER_PATH = "https://image.tmdb.org/t/p/w200/"
# this variable should be global so the user can remember the series that he has already added
fav_series = ["1399", "1396", "1100", "1668", "71446"]


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
    search_result_code = 0 # 0 for no search issued, 1 for search with results and -1 for search without results
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
                except: #some series might not have posters
                    pass
    if request.method == "GET":
        pass  # TODO
    posters = set_fav_posters(fav_series)
    return render_template("index.html", posters=posters, id_poster=id_poster, search_result_code= search_result_code)


@app.route("/addSeries/<int:series_id>")
def add_series_to_fav(series_id):
    fav_series.insert(0, series_id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
