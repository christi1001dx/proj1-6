# Flask engine for bloginator

from flask import Flask
from flask import render_template, redirect, url_for
from flask import session, request

import config as conf
import utils

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY

# all posts; for each, display anchor title (hyperlink to real post) and metadata
@app.route("/")
def home():
	posts = utils.posts()
	return render_template("home.html")

# all profiles; should only contain anchor usernames (links to respective profile)
@app.route("/profiles")
def profiles():
	return render_template("profiles.html", profiles = utils.profiles())

# profile by username
@app.route("/profiles/<username>")
def profile(username):
	profile = utils.profile(username)
	return render_template("profile.html", profile = profile)

# post by ID number
@app.route("/posts/<post>")
def post(post):
	post = utils.post(post)
	return render_template("post.html", post = post)

# action URL for login form
@app.route("/login", methods = ["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"] 

	if utils.authenticate(username, password):
		utils.login(username)
		return redirect(url_for("home"))
	return error("LoginFail")
	
# action URL for register form
@app.route("/register", methods = ["POST"])
def register():
	username = request.form["username"]	
	password = request.form["password"]	
	passRetype = request.form["passRetype"]	
	
	if password == passRetype:
		utils.register(username, password)
	else:
		return error("RegisterFail")

@app.route("/search", method = ["POST"])
def search():
	results = utils.query(request.form["query"])
	return render_template("query.html", results = results)

# error handling
def error(message):
	return render_template("error.html", message = message)

if __name__ == "__main__":
	app.run(debug = True)
