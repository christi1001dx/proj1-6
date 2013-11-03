from flask import Flask
from flask import render_template, redirect, url_for
from flask import session, request

import config as conf
import utils
import datetime

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
	return error()

@app.route("/users")
def users():
	return render_template("users.html", users = utils.getUsers())
	
@app.route("/user/<username>")
def user(username):
	user = utils.getUser(username)
	if user is not None:
		return render_template("user.html", user = user) 
	return error()
	
@app.route("/submit_post", methods = ["GET", "POST"])
def submitPost():
	if request.method == "GET":
		return render_template("submit_post.html")

	title = request.form["title"]
	if utils.loggedIn() and utils.titleAvailable(title):
			body = request.form["body"]
			author = session["username"]
			utils.submitPost(title, body, author, datetime.datetime.now())
			return redirect(url_for("home"))
	else:
		return error()


@app.route("/post/<postTitle>/submit_comment", methods = ["GET", "POST"])
def submitComment(postTitle):
	body = request.form["body"]
	if utils.loggedIn():
		author = session["username"]
	else:
		author = None
	utils.submitComment(postTitle, body, author, datetime.datetime.now())
	return redirect(url_for("post", postTitle = postTitle))

@app.route("/login", methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	elif not utils.loggedIn():
		username = request.form["username"]
		password = request.form["password"]
		if utils.authenticate(username, password):
			session["username"] = username
		else:
			return error()
	return redirect(url_for("home"))

@app.route("/logout")
def logout():
	session.pop("username")
	return redirect(url_for("home"))

@app.route("/register", methods = ["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	elif not utils.loggedIn():
		username = request.form["username"]
		password = request.form["password"]
		passRetype = request.form["passRetype"]
		security = request.form["security"]
        #answer = request.form["answer"]

		if utils.register(username, password, passRetype, security, answer):
			return redirect(url_for("home"))
		else:
			return error()
	else:
		return redirect(url_for("home"))

@app.route("/recover", methods=["GET", "POST"])
def recover():
    if request.method == "GET" :
        return render_template("recover.html")
    else:
        username = request.form['username']
        security = request.form['security']
        answer = request.form['answer']
        button = request.form['button']
        if button == "Submit":
            if (username == '' or answer == ''):
                return render_template("recover.html", message = "Please fill empty fields")
            else:   
                return render_template("recover.html", message = utils.recover(username,security,answer))
        elif button == "Cancel":
            return render_template("recover.html")


def error():
	error = session["error"]
	return render_template("error.html", error = error)

@app.errorhandler(404)
def error400(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def error500(error):
	return render_template("errors/500.html"), 500

if __name__ == "__main__":
	app.run(debug = True)
