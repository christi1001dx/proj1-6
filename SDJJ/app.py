from flask import Flask
from flask import render_template, redirect, url_for
from flask import session, request

import config as conf
import utils

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY

@app.route("/")
def home():
	return render_template("home.html", posts = utils.getPosts())

@app.route("/post/<postTitle>")
def post(postTitle):
	post = utils.getPost(postTitle)
	if post is not None:
		return render_template("post.html", post = post)
	return error("noPost")

@app.route("/users")
def users():
	return render_template("users.html", users = utils.getUsers())
	
@app.route("/user/<username>")
def user(username):
	user = utils.getUser(username)
	if user is not None:
		return render_template("user.html", user = user) 
	return error("noUser")
	
@app.route("/submit_post", methods = ["GET", "POST"])
def submitPost():
	if request.method == "GET":
		return render_template("submit_post.html")

	title = request.form["title"]
	if "username" in session:
		if utils.getPost(title) == None:
			body = request.form["body"]
			author = session["username"]
			utils.submitPost(title, body, author)
			return redirect(url_for("home"))
		else: 
			return error("mustLogin")

	else:
		return error("postFail")


@app.route("/post/<postTitle>/submit_comment", methods = ["GET", "POST"])
def submitComment(postTitle):
	body = request.form["body"]
	if "username" in session:
		author = session["username"]
	else:
		author = None
	utils.submitComment(postTitle, body, author)
	return redirect(url_for("post", postTitle = postTitle))

@app.route("/login", methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	elif "username" not in session:
		username = request.form["username"]
		password = request.form["password"]
		if utils.authenticate(username, password):
			session["username"] = username
		else:
			return error("loginFail")
	return redirect(url_for("home"))

@app.route("/logout")
def logout():
	session.pop("username")
	return redirect(url_for("home"))

@app.route("/register", methods = ["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	elif "username" not in session:
		username = request.form["username"]
		password = request.form["password"]
		passRetype = request.form["passRetype"]

		if password == passRetype:
			if utils.register(username, password):
				return redirect(url_for("home"))
			else: 
				return error("registerFail")
		else:
			return error("passMismatch")
	else:
		return redirect(url_for("home"))
	
def error(msg):
	return render_template("error.html", msg = msg)

if __name__ == "__main__":
	app.run(debug = True)
