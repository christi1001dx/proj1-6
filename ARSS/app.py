#!/usr/bin/python

from flask import Flask, request, render_template, redirect, session, url_for, flash
from bson import json_util
import utils, json

app = Flask(__name__)
app.secret_key = 'abcd'
app.debug = True

env = app.jinja_env
env.line_statement_prefix = 'yolo'
env.globals.update(utils=utils)

def get_form_value(key):
	return request.form[key].encode('ascii', 'ignore')

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
	if not 'username' in session:
		return 'login'
	author = session['username']
	title = get_form_value('title')
	line = get_form_value('line')
	if utils.add_line(line, title, author):
		return 'success'
	else:
		return 'error'

@app.route('/makestory', methods=['POST'])
def make_story():
	if utils.logged_in():
		author = session['username']
		title = get_form_value('title')
		value = str(utils.make_story(title, author))
	return redirect(url_for('index'))

@app.route('/login', methods = ['POST'])
def login():
	username = get_form_value('username')
	password = get_form_value('password')
	flash(utils.login_user(username, password))
	return redirect(url_for('index'))

@app.route('/register', methods = ['POST'])
def register():
	username = get_form_value('username')
	password = get_form_value('password')
	password2 = get_form_value('password2')
	flash(utils.register_user(username, password, password2))
	return redirect(url_for('index'))

@app.route('/logout', methods = ['POST'])
def logout():
	utils.logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
	#utils.make_story('test1', 'me', False)
	#utils.add_line('test line', 'test1', 'me')
	app.debug = True
	app.run(host='0.0.0.0')
