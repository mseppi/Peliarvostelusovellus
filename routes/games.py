"""
Handles pages that are related to games.
"""
from app import app
from flask import redirect, render_template, request, session
from db_account import check_csrf
from db_games import add_game, get_games, get_game
from db_mods import delete_review, delete_game
from db_comments import get_reviews, get_comments

@app.route("/add_game", methods=["GET", "POST"])
def add_game_route():
    """Handles adding games"""
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
            return render_template(
                "error.html", message="Pelin nimi ja genre eivät voi olla tyhjiä")
        elif len(title) > 50 or len(genre) > 50:
            return render_template(
                "error.html", message="Pelin nimi ja genre eivät voi olla yli 50 merkkiä pitkiä")
        elif release_year.isnumeric() == False:
            return render_template("error.html", message="Pelin julkaisuvuosi ei ole numero")
        elif int(release_year) < 1950 or int(release_year) > 2030:
            return render_template("error.html", message="Pelin julkaisuvuosi ei ole kelvollinen")
        elif add_game(title, genre, release_year):
            return redirect("/")
        return render_template("error.html", message="Järjestelmässä on jo tämän niminen peli")

@app.route("/games", methods=["GET", "POST"])
def games_route():
    """Handles showing games and deleting games"""
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
        return render_template("error.html", message="Pelin poistaminen ei onnistunut")

@app.route("/game/<int:id>", methods=["GET", "POST"])
def game_route(id):
    """Handles showing games and deleting reviews"""
    if "username" not in session:
        return render_template("error.html", message="Kirjaudu ensin sisään")
    if request.method == "GET":
        if get_game(id):
            return render_template(
                "game.html", game=get_game(id), reviews=get_reviews(id), len=len(get_comments(id)))
        return render_template("error.html", message="Peliä ei löydy")
    if request.method == "POST":
        review_id = request.form["review_id"]
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if delete_review(review_id):
            return render_template(
                "game.html", game=get_game(id), reviews=get_reviews(id), len=len(get_comments(id)))
        return render_template("error.html", message="Arvostelun poistaminen ei onnistunut")
