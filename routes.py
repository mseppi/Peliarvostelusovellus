from app import app
from flask import render_template, request, session, redirect, flash
from os import urandom
from visits import login, register, logout, profile, update_profile, add_game, get_games, get_game, add_review, get_reviews, get_comments, add_comment, get_users
from visits import delete_user, delete_game, delete_review, delete_comment, like, check_csrf
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "GET":
        return render_template("index.html")
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

@app.route("/profile/<username>")
def profile_route(username):
    if profile(username):
        return render_template("profile.html", bio=profile(username)[1], fav_games=profile(username)[2], username=username)
    else:
        return render_template("error.html", message="Profiilia ei löydy") 
        
        
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
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if update_profile(username, bio, fav_games):
            return redirect("/profile/" + username + "")
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
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if len(title) < 1 or len(genre) < 1:
            return render_template("error.html", message="Pelin nimi ja genre eivät voi olla tyhjiä")
        elif len(title) > 50 or len(genre) > 50:
            return render_template("error.html", message="Pelin nimi ja genre eivät voi olla yli 50 merkkiä pitkiä")
        elif release_year.isnumeric() == False:
            return render_template("error.html", message="Pelin julkaisuvuosi ei ole numero")
        elif int(release_year) < 1950 or int(release_year) > 2030:
            return render_template("error.html", message="Pelin julkaisuvuosi ei ole kelvollinen")
        elif add_game(title, genre, release_year):
            return redirect("/")
        else:
            return render_template("error.html", message="Järjestelmässä on jo tämän niminen peli")

@app.route("/games", methods=["GET", "POST"])
def games_route():
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        games = get_games()
        return render_template("games.html", games=games)
    if request.method == "POST":
        id = request.form["game_id"]
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if delete_game(id):
            return redirect("/games")
        else:
            return render_template("error.html", message="Pelin poistaminen ei onnistunut")



@app.route("/game/<int:id>", methods=["GET", "POST"])
def game_route(id):
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        if get_game(id):
            return render_template("game.html", game=get_game(id), reviews=get_reviews(id), len=len(get_comments(id)))
        else:
            return render_template("error.html", message="Peliä ei löydy")
    if request.method == "POST":
        review_id = request.form["review_id"]
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if delete_review(review_id):
            return render_template("game.html", game=get_game(id), reviews=get_reviews(id), len=len(get_comments(id)))
        else:
            return render_template("error.html", message="Arvostelun poistaminen ei onnistunut")


    
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
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if int(rating) < 1 or int(rating) > 10:
            return render_template("error.html", message="Arvostelun tulee olla 1-10 väliltä")
        elif len(review) < 1 or len(title) < 1:
            return render_template("error.html", message="Arvostelun otsikko ja sisältö eivät voi olla tyhjiä")
        elif add_review(title, username, id, review, rating):
            return redirect("/game/" + str(id))
        else:
            return render_template("error.html", message="Voit lisätä vain yhden arvostelun peliä kohden")
        
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
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if add_comment(username, id, comment):
            return redirect("/game/" + str(id) + "/comments")
        else:
            return render_template("error.html", message="Kommentin lisääminen ei onnistunut")

@app.route("/users", methods=["GET", "POST"])
def users_route():
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if session["admin_rights"] == False:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tälle sivulle")
    if request.method == "GET":
        return render_template("users.html", users=get_users())
    if request.method == "POST":
        username = request.form["username"]
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if username == session["username"]:
            return render_template("error.html", message="Et voi poistaa itseäsi")
        elif delete_user(username):
            return redirect("/users")
        else:
            return render_template("error.html", message="Käyttäjän poistaminen ei onnistunut")

@app.route("/comment/delete", methods=["POST"])
def delete_comment_route():
    comment_id = request.form["comment_id"]
    review_id = request.form["review_id"]
    csrf_token = request.form["csrf_token"]
    check_csrf(csrf_token)
    if delete_comment(comment_id):
        return redirect("/game/" + str(review_id) + "/comments")
    else:
        return render_template("error.html", message="Kommentin poistaminen ei onnistunut")

@app.route("/like", methods=["POST"])
def like_route():
    review_id = request.form["review_id"]
    game_id = request.form["game_id"]
    username = session["username"]
    csrf_token = request.form["csrf_token"]
    check_csrf(csrf_token)
    if like(username, review_id):
        return redirect("/game/" + str(game_id))
    else:
        return redirect("/game/" + str(game_id))
    