#!/usr/bin/python

from flask import Flask, request, render_template, redirect, session, url_for, flash
from bson import json_util
import utils, json

app = Flask(__name__)
app.secret_key = "abcd"
app.debug = True

env = app.jinja_env
env.line_statement_prefix = 'yolo'

def get_form_value(key):
	return request.form[key].encode("ascii", "ignore")

@app.route('/story')
def story_test():
	return render_template('story_test.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/story/<name>', methods = ['GET'])
def get_story(name):
	return json.dumps((utils.return_all_lines(name)), default=json_util.default)

@app.route('/allstories', methods = ['GET'])
def get_all_story():
    return json.dumps((utils.return_all_stories()))

@app.route('/addline', methods=['POST'])
def add_line():
	if not "username" in session:
		return "login"
	author = session["username"]
	title = get_form_value('title')
	line = get_form_value('line')
	if utils.add_line(line, title, author):
		return "success"
	else:
		return "error"

@app.route('/makestory', methods=['POST'])
def make_story():
	if not "username" in session:
		return "login"
	author = session["username"]
	title = get_form_value('title')
	return str(utils.make_story(title, author, False))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if (request.method == "GET"):
		return render_template("login.html")
	else:
		username = get_form_value('username')
		password = get_form_value('password')
		if (utils.account_exists(username, password)):
			session["username"] = username
			flash("Success!")
		else:
			flash("Incorrect username or password.")
		return redirect(url_for("index"))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if (request.method == "GET"):
		return render_template("register.html")
	else:
		username = get_form_value('username')
		password = get_form_value('password')
		password2 = get_form_value('password2')
		registertry = utils.add_user(username, password, password2)
		if (registertry == "good job"):
			flash("Success, "+username.decode("utf-8"))
		else:
			flash(registertry)
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username")
		return "success"
	else:
		return "ok"

if __name__ == '__main__':
	#utils.make_story('test1', 'me', False)
	#utils.add_line("test line", 'test1', 'me')
	app.debug = True
	app.run(host='0.0.0.0')
