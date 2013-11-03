from flask import Flask
from flask import session,url_for, request, redirect, render_template
from pymongo import MongoClient
import utils
import time

app = Flask(__name__)
app.secret_key = "abcd"

@app.route("/")
def index():
    if 'username' in session:
        return render_template("index.html",username = session["username"],posts = utils.getAllPosts())
    else:
        return render_template("index.html",posts = utils.getAllPosts())

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        if 'username' in session:
            return render_template("login.html",username = session["username"])
        else:
            return render_template("login.html")
    else:
        username = request.form["username"].encode("ascii","ignore")
        password = request.form["password"].encode("ascii","ignore")
        if utils.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("register.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "GET":
        if 'username' in session:
            return render_template("register.html",username = session["username"]) 
        else:
            return render_template("register.html")
    else:
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")
        confirmpassword = request.form["cpassword"].encode("ascii", "ignore")
        if password == confirmpassword:
            if utils.register(username, password):
                return redirect("/login")
            else:
                return redirect("/register")
        else:
            return render_template("register.html")

@app.route("/aboutme")
def aboutme():
    if 'username' in session:
        return render_template("aboutme.html",username = session["username"])
    else:
        return render_template("aboutme.html")

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect("/")
        
@app.route("/createpost")
def createpost():
    if request.method == "GET":
        if 'username' in session:
            return render_template("createpost.html",username = session["username"])
        else:
            return render_template("createpost.html")
    else:
        name = request.form["title"]
        text = request.form["text"]
        utils.newPost(name, text, time.strftime("%d/%m/%Y"))
        return redirect("/", username = session["username"])

'''@app.route("/removepost")
def removepost():
    if request.method == "GET":
        return render_template("removepost.html",username = session["username"])
    else:
        name = request.form["name"]
        mangodb.removepost(name)
        return redirect("/", username = session["username"])
'''
@app.route("/<post_name>")
def posts(post_name):
    text = utils.getPostText(post_name)
    name = post_name
    date = utils.getPostDate(post_name)
    comments = utils.getAllComments(post_name)
    if request.method =="GET":
        if 'username' in session:
            return render_template("indipost.html",username = session["username"],text=text,name=name,date=date,comments=comments)
        else:
            return render_template("indipost.html",text=text,name=name,date=date,comments=comments)
    else:
        comment = request.form["comment"]
        utils.newComment(username, comment, time.strftime("%d/%m/%Y"), post_name)
        return redirect("/post_name")
        
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5001)
