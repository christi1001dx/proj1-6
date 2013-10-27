#!/usr/bin/python

from flask import Flask
from flask import request, render_template, redirect, session, url_for
import utils
import helpers

app = Flask(__name__)
app.secret_key = "abcd"
app.debug = True

env = app.jinja_env
env.globals.update(helpers=helpers)
env.line_statement_prefix = '='

def get_form_value(key):
    return request.form[key].encode("ascii", "ignore")

@app.route('/')
<<<<<<< HEAD
def home():
    if (username = session["username"]):      
        return render_template("index.html")
    else:
        return redirect('/login')

@app.route('/story')
def story():
=======
def index():
    return render_template("index.html")

@app.route('/story')
def story():
    pass
>>>>>>> d3f80253968d8ee691921ada844138bd2a63d6d9
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == "GET"):
        return render_template("login.html")
    else:
<<<<<<< HEAD
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")
        
@app.route('/register', methods = ['GET', 'POST'])
def register('/register'):
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")

=======
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
        
>>>>>>> d3f80253968d8ee691921ada844138bd2a63d6d9
@app.route("/logout")
def logout():
    if "username" in sesson:
        session.pop("username")
        return render_template("logout.html")
    else:
        return redirect("/")
        
if __name__ == '__main__':
<<<<<<< HEAD
	app.debug = True
=======
>>>>>>> d3f80253968d8ee691921ada844138bd2a63d6d9
	app.run(host='0.0.0.0')
