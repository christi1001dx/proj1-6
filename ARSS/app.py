#!/usr/bin/python

from flask import Flask
from flask import request, render_template, redirect, session, url_for
import utils
import helpers
import json

app = Flask(__name__)
app.secret_key = "abcd"
app.debug = True

env = app.jinja_env
env.line_statement_prefix = '='
env.globals.update(helpers=helpers)

def get_form_value(key):
    return request.form[key].encode("ascii", "ignore")

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/story/<name>', methods = ['GET'])
def story(name):
    return json.dumps(utils.return_all_lines(name))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "GET"):
        return render_template("login.html")
    else:
        username = get_form_value('username')
        password = get_form_value('password')
        #check if username is valid

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        username = get_form_value('username')
        password = get_form_value('password')
        #check if passwords match

@app.route("/logout")
def logout():
    if "username" in sesson:
        session.pop("username")
        return render_template("logout.html")
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
