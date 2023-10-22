"""
Handles pahes that are related to comments and reviews.
"""
from app import app
from flask import render_template, request, session, redirect
from db_comments import add_comment, get_comments, like
from db_account import check_csrf
from db_comments import add_review

@app.route("/game/<int:id>/add_review", methods=["GET", "POST"])
def add_review_route(id):
    """Handles adding reviews"""
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
            return render_template(
                "error.html", message="Arvostelun otsikko ja sisältö eivät voi olla tyhjiä")
        elif add_review(title, username, id, review, rating):
            return redirect("/game/" + str(id))
        else:
            return render_template(
                "error.html", message="Voit lisätä vain yhden arvostelun peliä kohden")

@app.route("/game/<int:id>/comments", methods=["GET", "POST"])
def comments_route(id):
    """Handles showing comments and adding comments"""
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

@app.route("/like", methods=["POST"])
def like_route():
    """Handles liking reviews"""
    review_id = request.form["review_id"]
    game_id = request.form["game_id"]
    username = session["username"]
    csrf_token = request.form["csrf_token"]
    check_csrf(csrf_token)
    if like(username, review_id):
        return redirect("/game/" + str(game_id))
    else:
        return redirect("/game/" + str(game_id))
