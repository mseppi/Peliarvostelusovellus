from app import app
from flask import render_template, request, session
from os import urandom
from visits import login

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["post"])
def login():
    name = request.form["name"]
    password = request.form["password"]
    role = request.form["role"]
    if login(name, password, role):
        return render_template("index.html")
    else:
        return render_template("error.html", message="Väärä salasana tai käyttäjätunnus")

