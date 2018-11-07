from flask import Flask, render_template, request, url_for, redirect, session
import our_tmdb, storage_db, methods
import os

app = Flask(__name__)
app.secret_key = "hello".encode()
POSTER_PATH = our_tmdb.POSTER_PATH


@app.route("/notify")
def notify():
    return app.send_static_file("data/notifications_data/notify.json")


# functions to keep

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    user_email = None
    if request.method == "POST":
        if request.form["email"]:
            user_email = request.form["email"]
            new_password = methods.generate_password()
            methods.send_password_mail(user_email, new_password)
            storage_db.update_password_in_db(user_email, new_password)
        else:  # should never happen
            pass
    return render_template("forgot_password.html", email=user_email)


@app.route('/settings')
def settings():
    current_user = our_tmdb.User(session["current_user"])
    return render_template("settings.html", email_notifications=current_user.email_notifications,
                           browser_notifications=current_user.browser_notifications, email=current_user.login)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('current_user', None)
    return redirect(url_for('login'))


@app.route("/who")
def who():
    current_user = our_tmdb.User(session["current_user"])
    return str(current_user.__dict__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'email' in request.form.keys():  # login or sign up case
            if "first_name" in request.form.keys():  # sign up case
                try:
                    storage_db.ajout_infos_user(request.form["first_name"], request.form["last_name"],
                                                request.form["email"], request.form["password"])
                except storage_db.LoginAlreadyUsedException as e:
                    return render_template("error.html", error_msg=str(e), login_error=True)
            # trying to login, works for both new created account or already created account
            try:
                user_object = storage_db.authent(request.form["email"], request.form["password"])
                current_user = our_tmdb.User(user_object)
                session["current_user"] = current_user.__dict__
            except Exception as e:
                return render_template("error.html", error_msg=str(e), login_error=True)
        else:  # settings update case
            current_user = our_tmdb.User(session["current_user"])
            current_user.update_settings(**request.form.to_dict())
            session["current_user"] = current_user.__dict__
    try:
        current_user = our_tmdb.User(session["current_user"])
    except:  # if no one is logged in, redirect to login page
        return redirect(url_for("login"))
    try:
        fav_series = [our_tmdb.Series(i) for i in current_user.favourite_series]
    except our_tmdb.tmdbException as e:
        return render_template("error.html", error_msg=str(e), login_error=False)
    return render_template("index.html", fav_series=fav_series)


@app.route("/searchResult", methods=['GET', 'POST'])
def search():
    current_user = our_tmdb.User(session["current_user"])
    try:
        fav_series = [our_tmdb.Series(i) for i in current_user.favourite_series]
    except our_tmdb.tmdbException as e:
        return render_template("error.html", error_msg=str(e), login_error=False)
    # search_result_code 0 for no search issued, 1 for search with results and -1 for search without results -2 for empty search
    id_poster = dict()
    if request.method == "POST":
        if request.form["search"]:  # if the search query is not empty
            search_result = our_tmdb.Search(request.form["search"]).series
            if len(search_result) == 0:
                search_result_code = -1
            else:
                search_result_code = 1
                for series in search_result:
                    try:
                        id_poster[series.id] = POSTER_PATH + series.poster_path
                    except:  # some series might not have posters
                        pass
        else:
            search_result_code = -2
        return render_template("search_result.html", id_poster=id_poster, search_result_code=search_result_code,
                               fav_series=fav_series)
    elif request.method == "GET":
        if request.args["search"]:  # if the search query is not empty
            try:
                search_result = our_tmdb.Search(request.args["search"]).series
            except our_tmdb.tmdbException as e:
                return render_template("error.html", error_msg=str(e), login_error=False)
            if len(search_result) == 0:
                search_result_code = -1
            else:
                search_result_code = 1
                for series in search_result:
                    try:
                        id_poster[series.id] = POSTER_PATH + series.poster_path
                    except:  # some series might not have posters
                        pass
        else:
            search_result_code = -2
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
    return methods.join_networks(series)


@app.template_filter('jsonify')
def fav_series_to_json(fav_series):
    keys = [series.id for series in fav_series]
    values = [series.__dict__ for series in fav_series]
    dic = dict(zip(keys, values))
    return dic


@app.template_filter('duration')
def time_counter(list_of_series):
    return methods.time_counter(list_of_series)


if __name__ == "__main__":
    app.run(debug=True)
