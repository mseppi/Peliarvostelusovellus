"""
Contains functions to handle user accounts in database
"""
from os import urandom
from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

def login(username, password):
    """Check if username and password match"""
    sql = text("SELECT pword, id, admin_rights FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    print("User:")
    if user is not None:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["csrf_token"] = urandom(16).hex()
            session["admin_rights"] = user[2]
            return True
    return False

def register(username, password):
    """Register a new user"""
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

def check_csrf(csrf_token):
    """Check if the CSRF token is valid"""
    if session["csrf_token"] != csrf_token:
        abort(403)

def logout():
    """Logout the current user"""
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    del session["admin_rights"]
