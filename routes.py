from app import app
from flask import render_template, request, session
from os import urandom
from visits import login

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
    return render_template("login.html")

    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=[])
def register():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    if register(username, password, role):
        return "Rekisteröinti onnistui"
    else:
        return render_template("error.html", message="Rekisteröinti epäonnistui")