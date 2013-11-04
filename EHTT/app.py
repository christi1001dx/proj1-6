from flask import Flask
from flask import session,url_for, request, redirect, render_template
from pymongo import MongoClient
import mangodb

app = Flask(__name__)
app.secret_key = "abcd"

@app.route("/")
def index():
    d = mangodb.getallposts();
    if 'username' in session:
        return render_template("index.html",username = session["username"],d=d)
    else:
        return render_template("index.html",d=d)

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
        if mangodb.dlogin(username, password):
            session["username"] = username
            b = 1;
            return redirect("/")
        else:
            return redirect("/register")

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
            mangodb.dregister(username, password, 0)
            return redirect("/login")
        else:
            if 'username' in session:
                return render_template("register.html",username = session["username"]) 
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


#@app.route("/makepost")
#def makepost():
 #   if request.method == "GET"
    
        
@app.route("/createpost")
def createpost():
    if request.method == "GET":
        return render_template("createpost.html",username = session["username"])
    else:
        name = request.form["title"]
        text = request.form["post"]
       #date = request.form["date"]
        mangodb.newpost(name, text, 0)
        return redirect("/", username = session["username"])

@app.route("/removepost")
def removepost():
    if request.method == "GET":
        return render_template("removepost.html",username = session["username"])
    else:
        name = request.form["name"]
        mangodb.removepost(name)
        return redirect("/", username = session["username"])

@app.route("/posts/<post_name>")
def posts(post_name):
    ap = mangodb.getpost(post_name)
    if ap:
        d = {'text' : ap['txt'],
             'name' : post_name,
             'comments' : getpostcom(post_name),
             'date': ap['date']}
    
        if 'username' in session:
            return render_template("indipost.html",username = session["username"],d = d)
        else:
            return render_template("indipost.html",d = d)
    else:
        return redirect("/")

@app.route("/posts/<post_name>/comment")   
def comment(post_name):
    if request.method == "GET":
        if 'username' in session:
            return render_template("comment.html",username = session["username"]) 
        else:
            return render_template("comment.html")
    else: 
        if 'username' in session:
            text = request.form["text"]
            date = request.form["date"]
            mangodb.newcomment(mangodb.getpostid(post_name), text, session["username"], date)
            return redirect("/posts/<post_name>")
        else:
            text = request.form["text"]
            date = request.form["date"]
            mangodb.newcomment(mangodb.getpostid(post_name), text, "Anonymous", date)
            return redirect("/posts/<post_name>")

if __name__ == "__main__":
    #mangodb.connect()
    app.debug = True
    app.run(host = "0.0.0.0", port = 5001)
    
