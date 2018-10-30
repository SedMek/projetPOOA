from flask import Flask, render_template, request, url_for, redirect, session
import our_tmdb, storage_db
import os

app = Flask(__name__)
app.secret_key = "hello".encode()
POSTER_PATH = our_tmdb.POSTER_PATH


@app.route("/notify")
def notify():
    return app.send_static_file("notify.json")


# functions to keep

@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('current_user', None)
    return redirect(url_for('login'))


@app.route("/who")
def who():
    current_user = our_tmdb.User(session["current_user"])
    return current_user.login


@app.route("/mongo")
def mongo():
    return os.environ['MONGODB_URI']


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if len(request.form) == 4:  # sign up case
            try:
                storage_db.ajout_infos_user(request.form["first_name"], request.form["last_name"],
                                            request.form["email"], request.form["password"])
            except storage_db.LoginAlreadyUsedException as e:
                return render_template("error.html", error_msg=str(e))
        # trying to login, works for both new created account or already created account
        try:
            user_object = storage_db.authent(request.form["email"], request.form["password"])
            current_user = our_tmdb.User(user_object)
            session["current_user"] = current_user.__dict__
        except Exception as e:
            return render_template("error.html", error_msg=str(e))
    try:
        current_user = our_tmdb.User(session["current_user"])
    except:  # if no one is logged in, redirect to login page
        return redirect(url_for("login"))
    fav_series = [our_tmdb.Series(i) for i in current_user.favourite_series]
    return render_template("index.html", fav_series=fav_series)


@app.route("/searchResult", methods=['GET', 'POST'])
def search():
    current_user = our_tmdb.User(session["current_user"])
    fav_series = [our_tmdb.Series(i) for i in current_user.favourite_series]
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

                        id_poster[serie.id] = POSTER_PATH + serie.poster_path

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
    current_user = our_tmdb.User(session["current_user"])
    current_user.add_series_to_fav(series_id)
    session["current_user"] = current_user.__dict__
    return redirect(url_for("home"))


@app.route("/removeSeries/<int:series_id>")
def remove_series_from_fav(series_id):
    current_user = our_tmdb.User(session["current_user"])
    current_user.remove_series_from_fav(series_id)
    session["current_user"] = current_user.__dict__
    return redirect(url_for("home"))


@app.route("/clear_fav")
def clear_fav():
    current_user = our_tmdb.User(session["current_user"])
    current_user.clear_fav()
    session["current_user"] = current_user.__dict__
    return redirect(url_for("home"))


# filters
@app.template_filter('join_networks')
def join_networks(series):
    network_names = []

    for i in range(len(series.networks)):
        network_names.append(series.networks[i]["name"])

    return " &".join(network_names)


@app.template_filter('jsonify')
def fav_series_to_json(fav_series):
    keys = [series.id for series in fav_series]
    values = [series.__dict__ for series in fav_series]
    dic = dict(zip(keys, values))
    return dic


@app.template_filter('duration')
def time_counter(list_of_series):
    counter = 0
    duration = ""
    for element in list_of_series:
        counter += element.number_of_episodes * element.episode_run_time[0]
    days = counter // (24*60)
    hours = (counter % (24*60)) // 60
    mins = counter % 60
    if days:
        duration = str(days) + " days "
    if hours:
        duration = duration + str(hours) + " hours "
    if mins:
        duration = duration + str(mins) + " minutes"

    return duration


if __name__ == "__main__":
    app.run(debug=True)
