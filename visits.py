from db import db
from flask import session
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text


def login(username, password):
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
    del session["username"]
    del session["csrf_token"]
    del session["admin_rights"]

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

def update_profile(username, bio, fav_games):
    try:
        sql = text("UPDATE profile SET bio=:bio, fav_games=:fav_games WHERE username=:username")
        db.session.execute(sql, {"bio":bio, "fav_games":fav_games, "username":username})
        db.session.commit()
        return True
    except:
        return False
    
def add_game(title, genre, release_year):
    try:
        sql = text("INSERT INTO games (title, genre, release_year) VALUES (:title, :genre, :release_year)")
        db.session.execute(sql, {"title":title, "genre":genre, "release_year":release_year})
        db.session.commit()
        return True
    except:
        return False
    
def get_games():
    try:
        sql = text("SELECT * FROM games")
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

def get_game(id):
    try:
        sql = text("SELECT * FROM games WHERE id=:id")
        result = db.session.execute(sql, {"id":id})
        return result.fetchone()
    except:
        return False    
    
def add_review(title, username, game_id, review, rating):
    try:
        sql = text("INSERT INTO reviews (title, username, game_id, review, rating) VALUES (:title, :username, :game_id, :review, :rating)")
        print(sql)
        db.session.execute(sql, {"title":title, "username":username, "game_id":game_id, "review":review, "rating":rating})
        db.session.commit()
        return True
    except:
        return False
    
def get_reviews(game_id):
    try:
        sql = text("SELECT * FROM reviews WHERE game_id=:game_id")
        result = db.session.execute(sql, {"game_id":game_id})
        return result.fetchall()
    except:
        return False
    
def add_comment(username, review_id, comment):
    try:
        sql = text("INSERT INTO comments (username, review_id, comment) VALUES (:username, :review_id, :comment)")
        db.session.execute(sql, {"username":username, "review_id":review_id, "comment":comment})
        db.session.commit()
        return True
    except:
        return False

def get_comments(review_id):
    try:
        sql = text("SELECT * FROM comments WHERE review_id=:review_id")
        result = db.session.execute(sql, {"review_id":review_id})
        return result.fetchall()
    except:
        return False
    
def get_users():
    try:
        sql = text("SELECT * FROM users")
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

def delete_user(username):
    try:
        sql = text("DELETE FROM users WHERE username=:username")
        db.session.execute(sql, {"username":username})
        sql2 = text("DELETE FROM profile WHERE username=:username")
        db.session.execute(sql2, {"username":username})
        sql3 = text("DELETE FROM reviews WHERE username=:username")
        db.session.execute(sql3, {"username":username})
        sql4 = text("DELETE FROM comments WHERE username=:username")
        db.session.execute(sql4, {"username":username})
        db.session.commit()
        return True
    except:
        return False

def delete_comment(id):
    try:
        sql = text("DELETE FROM comments WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False
    
def delete_review(id):
    try:
        sql = text("DELETE FROM reviews WHERE id=:id")
        db.session.execute(sql, {"id":id})
        sql2 = text("DELETE FROM comments WHERE review_id=:id")
        db.session.execute(sql2, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def delete_game(id):
    try:
        sql = text("DELETE FROM games WHERE id=:id")
        db.session.execute(sql, {"id":id})
        sql2 = text("DELETE FROM reviews WHERE game_id=:id")
        db.session.execute(sql2, {"id":id})
        sql3 = text("DELETE FROM comments WHERE review_id IN (SELECT id FROM reviews WHERE game_id=:id)")
        db.session.execute(sql3, {"id":id})
        db.session.commit()
        return True
    except:
        return False
