from app import app
from flask import render_template, request, session, redirect
from os import urandom
from visits import login, register, logout, profile, update_profile, add_game, get_games, get_game, add_review, get_reviews, get_comments, add_comment

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
        elif len(username) < 3 or len(password) < 3:
            return render_template("error.html", message="Käyttäjätunnuksen ja salasanan tulee olla vähintään 3 merkkiä pitkiä")
        elif register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä")

@app.route("/profile")
def profile_route():
    username = session["username"]
    if profile(username):
        return render_template("profile.html", bio=session.get("bio"), fav_games=session.get("fav_games"))
    else:
        return render_template("error.html", message="Kirjaudu ensin sisään") 
        
        
@app.route("/update_profile", methods=["GET", "POST"])
def update_profile_route():
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
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
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        return render_template("add_game.html")
    if request.method == "POST":
        title = request.form["title"]
        genre = request.form["genre"]
        release_year = request.form["release_year"]
        if len(title) < 1 or len(genre) < 1:
            return render_template("error.html", message="Pelin nimi ja genre eivät voi olla tyhjiä")
        elif len(title) > 50 or len(genre) > 50:
            return render_template("error.html", message="Pelin nimi ja genre eivät voi olla yli 50 merkkiä pitkiä")
        elif release_year < 1950 or release_year > 2030:
            return render_template("error.html", message="Pelin julkaisuvuosi ei ole kelvollinen")
        elif add_game(title, genre, release_year):
            return redirect("/")
        else:
            return render_template("error.html", message="Pelin lisääminen ei onnistunut")

@app.route("/games")
def games_route():
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    games = get_games()
    return render_template("games.html", games=games)

@app.route("/game/<int:id>")
def game_route(id):
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if get_game(id):
        return render_template("game.html", game=get_game(id), reviews=get_reviews(id), len=len(get_comments(id)))
    else:
        return render_template("error.html", message="Peliä ei löydy")
    
@app.route("/game/<int:id>/add_review", methods=["GET", "POST"])
def add_review_route(id):
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        return render_template("add_review.html", id=id)
    if request.method == "POST":
        username = session["username"]
        review = request.form["review"]
        title = request.form["title"]
        rating = request.form["rating"]
        if rating < 1 or rating > 10:
            return render_template("error.html", message="Arvostelun tulee olla 1-10 väliltä")
        elif len(review) < 1 or len(title) < 1:
            return render_template("error.html", message="Arvostelun otsikko ja sisältö eivät voi olla tyhjiä")
        elif add_review(title, username, id, review, rating):
            return redirect("/game/" + str(id))
        else:
            return render_template("error.html", message="Arvostelun lisääminen ei onnistunut")
        
@app.route("/game/<int:id>/comments", methods=["GET", "POST"])
def comments_route(id):
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        if get_comments(id):
            return render_template("comments.html", comments=get_comments(id), id=id)
        elif get_comments(id) == []:
            return render_template("comments.html", comments=[], id=id)
        else:
            return render_template("error.html", message="Kommenttien lataaminen ei onnistunut")
    if request.method == "POST":
        username = session["username"]
        comment = request.form["comment"]
        if add_comment(username, id, comment):
            return redirect("/game/" + str(id) + "/comments")
        else:
            return render_template("error.html", message="Kommentin lisääminen ei onnistunut")