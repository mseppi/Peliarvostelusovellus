from db import db
from flask import session
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text


def login(username, password):
    sql = text("SELECT pword, id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    print("User:")
    if user is not None:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            return True

    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, pword) VALUES (:username, :pword)")
        db.session.execute(sql, {"username":username, "pword":hash_value})
        sql2 = text("INSERT INTO profile (username) VALUES (:username)")
        db.session.execute(sql2, {"username":username})
        db.session.commit()
        return True
    except:
       return False

def logout():
    del session["user_id"]

def profile(username):
    try:
        sql = text("SELECT username, bio, fav_games FROM profile WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        profile_data = result.fetchone()

        if profile_data:
            session["bio"] = profile_data[1]
            session["fav_games"] = profile_data[2]
            return True
        else:
            return False
    except:
        return False
    

    
