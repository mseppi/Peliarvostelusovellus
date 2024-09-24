"""
Contains moderator tools
"""
from app import app
from flask import redirect, render_template, request, session
from db_mods import get_users, delete_user, delete_comment
from db_account import check_csrf

@app.route("/users", methods=["GET", "POST"])
def users_route():
    """Handles showing users and deleting users"""
    if "username" not in session:
        return render_template("error.html", message="Log in first")
    if session["admin_rights"] == False:
        return render_template("error.html", message="You do not have permission to view this page")
    if request.method == "GET":
        return render_template("users.html", users=get_users())
    if request.method == "POST":
        username = request.form["username"]
        csrf_token = request.form["csrf_token"]
        check_csrf(csrf_token)
        if username == session["username"]:
            return render_template("error.html", message="You cannot delete yourself")
        if delete_user(username):
            return redirect("/users")
        return render_template("error.html", message="Deleting user failed")

@app.route("/comment/delete", methods=["POST"])
def delete_comment_route():
    """Handles deleting comments"""
    comment_id = request.form["comment_id"]
    review_id = request.form["review_id"]
    csrf_token = request.form["csrf_token"]
    check_csrf(csrf_token)
    if delete_comment(comment_id):
        return redirect("/game/" + str(review_id) + "/comments")
    return render_template("error.html", message="Deleting comment failed")
