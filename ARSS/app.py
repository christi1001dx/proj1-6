#!/usr/bin/python

from flask import Flask
from flask import request, render_template, redirect, session, url_for
import utils
import helpers

app = Flask(__name__)
env = app.jinja_env
env.globals.update(helpers=helpers)
app.secret_key = "abcd"
app.debug = True

def get_form_value(key):
    return request.form[key].encode("ascii", "ignore")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/story')
def story():
    pass
    
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
