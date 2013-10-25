#!/usr/bin/python

from flask import Flask
from flask import request, render_template, redirect, session, url_for
import utils

app = Flask(__name__)
app.secret_key = "abcd"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/story')
def story():
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "GET"):
        return render_template("login.html")
    else:
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")
        #check if username is valid
    
@app.route('/register', methods = ['GET', 'POST'])
def register('/register'):
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")
        #check if passwords match
        
@app.route("/logout")
def logout():
    if "username" in sesson:
        session.pop("username")
        return render_template("logout.html")
    else:
        return redirect("/")
        
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
