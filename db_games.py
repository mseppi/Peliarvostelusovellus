"""
Contains functions to handle games in database
"""
from db import db
from sqlalchemy import text

def add_game(title, genre, release_year):
    """Add a game to the database."""
    try:
        sql = text(
            "INSERT INTO games (title, genre, release_year) VALUES (:title, :genre, :release_year)")
        db.session.execute(sql, {"title":title, "genre":genre, "release_year":release_year})
        db.session.commit()
        return True
    except:
        return False

def get_games():
    """Get all games from the database."""
    try:
        sql = text("SELECT * FROM games ORDER BY title ASC")
        result = db.session.execute(sql)
        return result.fetchall()
    except:
        return False

def get_game(id):
    """Get a game from the database."""
    try:
        sql = text("SELECT * FROM games WHERE id=:id")
        result = db.session.execute(sql, {"id":id})
        return result.fetchone()
    except:
        return False
