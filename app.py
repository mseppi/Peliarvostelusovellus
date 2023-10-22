"""
This file is the main file that is used to run the application.
"""
from dotenv import load_dotenv
from flask import Flask
from os import getenv


app = Flask(__name__)
load_dotenv()
app.secret_key = getenv("SECRET_KEY")

from routes import account
from routes import mods
from routes import profile
from routes import games
from routes import comments
