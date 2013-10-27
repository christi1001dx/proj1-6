from flask import Flask
from flask import request, render_template, redirect, session, url_for
import auth


app = Flask(__name__)
app.secret_key = "shhhh"

@app.route("/")
def home():
    return redirect("/home")

@app.route("/home")
def homepage():
    return  render_template("login.html")

@app.route("/login", methods = ["GET", "POST"]):
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
       username = request.form["username"].encode("ascii","ignore")
        password = request.form["password"].encode("ascii","ignore")

        
