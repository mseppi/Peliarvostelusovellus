"""
Handles all mod-tool related functions
"""
from db import db
from sqlalchemy import text

def delete_user(username):
    """Delete a user from the database."""
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
    """Delete a comment from the database."""
    try:
        sql = text("DELETE FROM comments WHERE id=:id")
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def delete_review(id):
    """Delete a review from the database."""
    try:
        sql = text("DELETE FROM reviews WHERE id=:id")
        db.session.execute(sql, {"id":id})
        sql2 = text("DELETE FROM comments WHERE review_id=:id")
        db.session.execute(sql2, {"id":id})
        sql3 = text("DELETE FROM likes WHERE review_id=:id")
        db.session.execute(sql3, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def delete_game(id):
    """Delete a game from the database."""
    try:
        sql = text("DELETE FROM games WHERE id=:id")
        db.session.execute(sql, {"id":id})
        sql2 = text("DELETE FROM reviews WHERE game_id=:id")
        db.session.execute(sql2, {"id":id})
        sql3 = text(
            "DELETE FROM comments WHERE review_id IN (SELECT id FROM reviews WHERE game_id=:id)")
        db.session.execute(sql3, {"id":id})
        sql4 = text(
            "DELETE FROM likes WHERE review_id IN (SELECT id FROM reviews WHERE game_id=:id)")
        db.session.execute(sql4, {"id":id})
        db.session.commit()
        return True
    except:
        return False

def get_users():
    """Get all users from the database."""
    try:
        sql = text("SELECT * FROM users")
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False
