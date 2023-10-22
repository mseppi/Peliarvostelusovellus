from db import db
from sqlalchemy import text

def profile(username):
    try:
        sql = text("SELECT username, bio, fav_games FROM profile WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        profile_data = result.fetchone()
        if profile_data:
            return profile_data
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