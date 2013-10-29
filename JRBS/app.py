from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key="JRBS"

@app.route("/")
def home():
    return "<h1>Bloginator Home</h1>"

@app.route("/signup")
def signup():
    return "<h1>Signup</h1>"

@app.route("/newpost")
def newpost():
    return "<h1>New posts made here</h1>"

@app.route("/archive")
def archive():
    return "<h1>List of all posts here</h1>"

@app.route("/posts")
def posts():
    return "<h1> should be able to navigate through posts, comments, etc. </h1>"

# @app.route("/posts/user")
# def user():
#     return """
# <h1> navigation of users should go here </h1>
# <h2> /posts/user/userid should take you to a user's posts </h2>
# """
