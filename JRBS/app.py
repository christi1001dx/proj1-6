#! /usr/bin/env python

import sqlite3

from flask import Flask, request, render_template, redirect, session
from jinja2 import Environment

from database import Database
from objects import User, Post, Comment

app = Flask(__name__)
app.secret_key = "JRBS"

database = Database("database.db")

# For pluralization code
app.jinja_options["extensions"].append("jinja2.ext.i18n")
app.create_jinja_environment()
app.jinja_env.install_null_translations()

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
        return render_template("signup.html")
    username = request.form["name"]
    password = request.form["password"]
    confirm = request.form["passwordConfirm"]
    display_name = request.form["displayName"]
    box = request.form.get("acceptTerms")
    if not username or not password or not confirm or not display_name:
        return render_template("signup.html", error="missing")
    if not box:
        return render_template("signup.html", error="accept terms")
    if password != confirm:
        return render_template("signup.html", error="password mismatch")
    answer = database.register(username, display_name, password)
    if answer == "ok":
        session["username"] = username
        return redirect("/posts")
    return render_template("signup.html", error=answer)

@app.route("/register")
def register():
    return redirect("/signup")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/posts")

@app.route("/posts")
@app.route("/posts/<page>")
@app.route("/posts/user/<user>")
@app.route("/posts/user/<user>/<page>")
def posts(user=None, page=1):
    try:
        page = int(page)
    except ValueError:
        return redirect("/posts")
    if page < 1:
        return redirect("/posts")
    if user:
        try:
            user = int(user)
        except ValueError:
            return redirect("/posts")
        user = database.get_user(user)
        if not user:
            return redirect("/posts")
    posts, pages = database.get_posts(user=user, page=page)
    if not pages:
        pages = 1
    if page > pages:
        return redirect("/posts")
    return render_template("posts.html", user=user, page=page, pages=pages,
                           posts=posts)

@app.route("/post/<postid>", methods=["GET", "POST"])
@app.route("/post/<postid>/<title>", methods=["GET", "POST"])
def post(postid=None, title=None):
    if not postid:
        return redirect("/posts")
    post = database.get_post(postid)
    if not post:
        return render_template("post.html", error1="missing")
    if request.method == "POST":
        text = request.form["text"]
        required = [text]
        if "username" in session:
            username = session["username"]
            anon_name = email = None
        else:
            username = None
            anon_name = request.form["anonName"]
            email = request.form["anonEmail"]
            required.extend([anon_name, email])
        if not all(required):
            return render_template("post.html", post=post, error2="incomplete")
        if email and not database.validate_email(email):
            return render_template("post.html", post=post, error2="bad email")
        answer = database.add_comment(postid, username, text, anon_name, email)
        if answer != "ok":
            return render_template("post.html", post=post, error2=answer)
        post = database.get_post(postid)
    return render_template("post.html", post=post)

@app.route("/new", methods=["GET", "POST"])
def new():
    if "username" not in session:
        return redirect("/login")
    if request.method == "GET":
        return render_template("new.html")
    title = request.form["title"]
    content = request.form["content"]
    if not title or not content:
        return render_template("new.html", error="incomplete")
    answer = database.create_post(title, content, session["username"])
    if answer == "ok":
        return redirect("/posts")
    return render_template("new.html", error=answer)

@app.route("/archive")
def archive():
    posts, pages = database.get_posts(page=None)
    return render_template("archive.html", posts=posts)

# @app.route("/admin")
# def admin():
#     pass

if __name__ == "__main__":
    app.run(debug=True)
