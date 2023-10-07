from app import app
from flask import render_template, request, session, redirect
from os import urandom
from visits import login, register, logout, profile, update_profile, add_game, get_games, get_game, add_review, get_reviews

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

    
@app.route("/logout")
def logout_route():
    logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/profile")
def profile_route():
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    
    username = session["username"]
    if profile(username):
        return render_template("profile.html", bio=session.get("bio"), fav_games=session.get("fav_games"))
    else:
        return render_template("error.html", message="Profiilin lataaminen ei onnistunut")
        
        
@app.route("/update_profile", methods=["GET", "POST"])
def update_profile_route():
    if request.method == "GET":
        return render_template("update_profile.html")
    if request.method == "POST":
        username = session["username"]
        bio = request.form["bio"]
        fav_games = request.form["fav_games"]
        if update_profile(username, bio, fav_games):
            return redirect("/profile")
        else:
            return render_template("error.html", message="Profiilin päivittäminen ei onnistunut")

@app.route("/add_game", methods=["GET", "POST"])
def add_game_route():
    if request.method == "GET":
        return render_template("add_game.html")
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        release_year = request.form["release_year"]
        if add_game(title, genre, release_year):
            return redirect("/")
        else:
            return render_template("error.html", message="Pelin lisääminen ei onnistunut")

@app.route("/games")
def games_route():
    games = get_games()
    return render_template("games.html", games=games)

@app.route("/game/<int:id>")
def game_route(id):
    if get_game(id):
        return render_template("game.html", game=get_game(id), reviews=get_reviews(id))
    else:
        return render_template("error.html", message="Peliä ei löydy")
    
@app.route("/game/<int:id>/add_review", methods=["GET", "POST"])
def add_review_route(id):
    if request.method == "GET":
        return render_template("add_review.html", id=id)
    if request.method == "POST":
        username = session["username"]
        review = request.form["review"]
        title = request.form["title"]
        rating = request.form["rating"]
        if add_review(title, username, id, review, rating):
            return redirect("/game/" + str(id))
        else:
            return render_template("error.html", message="Arvostelun lisääminen ei onnistunut")