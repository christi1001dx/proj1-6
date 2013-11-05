#! /usr/bin/env python

from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3

from database import Database

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
    box = request.form.get("acceptTerms")
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
@app.route("/posts/<page>")
@app.route("/posts/user/<user>")
@app.route("/posts/user/<user>/<page>")
def posts(user=None, page=1):
    posts = database.get_posts(user=user, page=page)
    return render_template("posts.html", posts=posts)

@app.route("/post/<post_id>")
@app.route("/post/<post_id>/<post_title>")
def post(post_id=None, post_title=None):
    if not post_id:
        return redirect("/posts")
    return render_template("post.html", post=database.get_post(post_id))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/posts")

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

# @app.route("/admin")
# def admin():
#     pass

if __name__=="__main__":
    app.run(debug=True)
