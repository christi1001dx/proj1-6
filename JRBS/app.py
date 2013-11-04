from flask import Flask, request, render_template, redirect, session, url_for
from database import User, Post, Comment, Database
import sqlite3

import database

app = Flask(__name__)
app.secret_key="JRBS"
database = Database("database.db")

@app.route("/")
def home():
    return redirect("/posts")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["name"]
    password = request.form["password"]
    if not username or not password:
        return render_template("login.html", error="missing")
    answer = database.login(username, password)
    if answer == "ok":
        session["username"] = username
        return redirect("/posts")
    return render_template("login.html", error=answer)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form["name"]
    password = request.form["password"]
    password_confirm = request.form["passwordConfirm"]
    display_name = request.form["displayName"]
    box = request.form["acceptTerms"]
    if not username or not password or not password_confirm or not display_name:
        return render_template("register.html", error="missing")
    if not box:
        return render_template("register.html", error="accept terms")
    if password != password_confirm:
        return render_template("register.html", error="password mismatch")
    answer = database.register(username, display_name, password)
    if answer == "ok":
        session["username"] = username
        return redirect("/posts")
    return render_template("register.html", error=answer)

@app.route("/posts")
def posts():
    posts = database.get_posts()
    return render_template("posts.html", posts=posts)

@app.route("/posts/<page>")
def posts_page(page=1):
    posts = database.get_posts(page=page)
    return render_template("posts.html", posts=posts)

@app.route("/posts/user/<user>")
def posts_user(user):
    posts = database.get_posts(user=user)
    return render_template("posts.html", posts=posts)

@app.route("/posts/user/<user>/<page>")
def posts_user_page(user, page=1):
    posts = database.get_posts(user=user, page=page)
    return render_template("posts.html", posts=posts)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/posts")

# @app.route("/new")
# def new():
#     button1 = request.form["cancel"]
#     button2 = request.form["submit"]
#     title = request.form["title"]
#     post = request.form["post"]
#     if request.method=="GET":
#         return render_template("new.html")
#     elif button1:
#         return redirect(url_for('posts'))
#     elif button2:
#         stuff.add(title, post)
#         return redirect(url_for('posts'))

# @app.route("/admin")
# def admin():
#     pass

if __name__=="__main__":
    app.run(debug=True)
