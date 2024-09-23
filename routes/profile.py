"""
Contains routes for profile page and updating profile
"""
from app import app
from flask import redirect, render_template, request, session
from db_account import check_csrf
from db_profile import profile, update_profile

@app.route("/profile/<username>")
def profile_route(username):
    """Handles showing profile"""
    if profile(username):
        return render_template(
            "profile.html", bio=profile(username)[1],
             fav_games=profile(username)[2], username=username)
    return render_template("error.html", message="Profile not found")

@app.route("/update_profile", methods=["GET", "POST"])
def update_profile_route():
    """Handles updating profile"""
    if "username" not in session:
        return render_template("error.html", message="Log in first")
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
        return render_template("error.html", message="Updating profile failed")
