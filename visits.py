from db import db
from flask import session
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash


def login(name, password, role):
    sql = "SELECT password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["name"] = name
            session["csrf_token"] = urandom(16).hex()
            session["role"] = role
            return True
        else:
            return False