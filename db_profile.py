"""
Handles all profile related functions
"""
from db import db
from sqlalchemy import text

def profile(username):
    """Get profile data from the database."""
    try:
        sql = text("SELECT username, bio, fav_games FROM profile WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        profile_data = result.fetchone()
        if profile_data:
            return profile_data
    except:
        return False

def update_profile(username, bio, fav_games):
    """Update profile data in the database."""
    try:
        sql = text("UPDATE profile SET bio=:bio, fav_games=:fav_games WHERE username=:username")
        db.session.execute(sql, {"bio":bio, "fav_games":fav_games, "username":username})
        db.session.commit()
        return True
    except:
        return False
