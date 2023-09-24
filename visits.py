from db import db
from flask import session
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash


def login(name, password):
    sql = "SELECT password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if check_password_hash(user[0], password):
        if not user:
            return False
        session["user_id"] = user[0]
        return True
    else:
        return False

