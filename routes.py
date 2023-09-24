from app import app
from flask import render_template, request, session, redirect
from os import urandom
from visits import login, register, logout

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