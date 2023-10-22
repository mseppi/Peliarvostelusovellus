from db import db
from sqlalchemy.sql import text


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
        sql = text("SELECT * FROM reviews WHERE game_id=:game_id ORDER BY id DESC")
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
        sql = text("SELECT * FROM comments WHERE review_id=:review_id ORDER BY id DESC")
        result = db.session.execute(sql, {"review_id":review_id})
        return result.fetchall()
    except:
        return False
    
def like(username, id):
    try:
        sql = text("INSERT INTO likes (username, review_id) VALUES (:username, :id)")   
        db.session.execute(sql, {"username":username, "id":id})
        sql2 = text("UPDATE reviews SET likes=likes+1 WHERE id=:id")
        db.session.execute(sql2, {"id":id})
        db.session.commit()
        return True
    except:
        return False
    
