"""
Handles all pages that are related to account management.
"""
from app import app
from flask import redirect, render_template, request
from db_account import login, logout, register


@app.route("/")
def index():
    """Displays index page"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    """Handles logging in"""
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout_route():
    """Handles logging out"""
    logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register_route():
    """Handles registering"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        elif len(username) < 3 or len(password) < 3:
            return render_template(
                "error.html",
                  message="Käyttäjätunnuksen ja salasanan tulee olla vähintään 3 merkkiä pitkiä")
        elif register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä")
