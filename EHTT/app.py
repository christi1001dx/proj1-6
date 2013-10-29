from flask import Flask
from flask import session,url_for, request, redirect, render_template
from pymongo import MongoClient
#import mangodb.py

app = Flask(__name__)
app.secret_key = "abcd"

@app.route("/")
def index():
    return render_template("index.html",session["username"])

@app.route("/login", methods = ['GET', 'POST'])
def login()
    if request.method == "GET":
        return render_template("login.html",session["username"])
    else:
        username = request.form["username"].encode("ascii","ignore")
        password = request.form["password"].encode("ascii","ignore")
        if mongodb.dlogin(username, password):
            session["username"] = username
            b = 1;
            return redirect("/")
        else:
            return render_template("register.html",session["username"])

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html",session["username"]) 
    else:
        username = request.form["username"].encode("ascii", "ignore")
        password = request.form["password"].encode("ascii", "ignore")
        confirmpassword = request.form["confirmpassword"].encode("ascii", "ignore")
        if a = mangodb.dregister(username, password, confirmpassword, 0):
            return redirect("/login", error = a)
        else:
            return render_template("register.html",session["username"])

@app.route("/aboutme")
def aboutme():
    return render_template("aboutme",session["username"])

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect("/")

@app.route("/createpost")
def createpost():
     if request.method == "GET":
        return render_template("createpost.html",session["username"])
    else:
        name = request.form["title"]
        text = request.form["post"]
        mongodb.newpost(name, text)
        return redirect("/")

@app.route("/removepost")
def removepost():
     if request.method == "GET":
        return render_template("removepost.html",session["username"])
    else:
        name = request.form["name"]
        mongodb.removepost(name)
        return redirect("/")

@app.route("/posts/<post_name>")
def posts(post_name):
 
    d = {'text' : mongodb.getpost(post_name),
         'name' : post_name,
         'comments' : getpostcom(post_name)}
    return render_template("posts",session["username"],d = d)

@app.route("/posts/<post_name>/comment")   
def comment(post_name):
    if request.method == "GET":
        return render_template("comment.html",session["username"])
    else:
        text = request.form["text"]
        mongodb.newcomment(mongodb.getpostid(post_name), text, session["username"])
        return redirect("/posts/<post_name>")
    

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)

