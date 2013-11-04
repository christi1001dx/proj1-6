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
    display_name = request.form["displayname"]
    box = request.form["acceptTerms"]
    if not box:
        return render_template("register.html", error="accept terms")
    if password != password_confirm:
        return render_template("register.html", error="password mismatch")
    answer = database.register(username, display_name, password)
    if answer == "ok":
        session["username"] = username
        return redirect("/posts")
    return render_template("register.html", error=answer)

@app.route("/new")
def new():
    button1 = request.form["cancel"]
    button2 = request.form["submit"]
    title = request.form["title"]
    post = request.form["post"]
    if request.method=="GET":
        return render_template("new.html")
    elif button1:
        return redirect(url_for('posts'))
    elif button2:
        stuff.add(title, post)
        #possibly create a Post and add it to db? coming back to this later.
        return redirect(url_for('posts'))

@app.route("/posts")
def posts():
    button = request.form["users"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts.html")
    elif button:
        if 'username' in session:
            user_id = stuff.getUser()
            return redirect(url_for('posts/user/%s' % user_id))
        else:
            page_number = page
            return redirect(url_for('posts/%s' % page)) #don't think this works, but putting it here anyway

@app.route("/posts/<page_number>")
def posts_page(page_number=1):
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":           #don't know how to make the page based on pg # here....
        return render_template("posts") #so I'll just leave what I was trying to do below.
        #pg = Database(None, page)
        #return render_template("posts", posts = pg.get_posts()) ****get_posts() is from database.py******
    elif button == "home":
        return redirect(url_for('posts'))
    else:
        page_number = page
        return redirect(url_for('posts/%s' % page))

@app.route("/posts/user/<user_id>")
def posts_user(user_id):
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts") #same as above
    elif button == "home":
        return redirect(url_for('posts'))
    else:
        page_number = page
        return redirect(url_for('posts/user/%s/%s' % (user, page)))

@app.route("/posts/user/<user_id>/<page_number>")
def posts_user_page(user_id, page_number=1):
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts") # same as above
    elif button == "home":
        return redirect(url_for('posts'))
    else:
        page_number = page
        return redirect(url_for('posts/user/%s/%s' % (user, page)))

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect('posts')

if __name__=="__main__":
    app.debug=True
    app.run()
