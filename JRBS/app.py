from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key="JRBS"

@app.route("/")
def home():
    return redirect(url_for('posts'))

@app.route("/signup")
def signup():
    if request.method=="GET":
        return render_template("register.html")
    else:
        username = request.form["name"].encode("ascii", "ignore")
        password1 = request.form["password1"].encode("ascii", "ignore")
        password2 = request.form["password2"].encode("ascii", "ignore")
        button = request.form["button"]
        box = request.form["acceptTerms"]
        if button == "Login":
            if not box:                
                return render_template("register.html", "you need to check the box first")
            elif auth.auth(username, password) :
                session["name"] = username
                return redirect(url_for('posts'))
            else:
                return render_template("register.html", "wrong username/pw combo")   
        
@app.route("/new")
def new():
    return "<h1>New posts made here</h1>"

@app.route("/archive")
def archive():
    if request.method=="GET":        
        return "<h1>List of all posts here</h1>"

@app.route("/admin")
def admin():

@app.route("/posts")
def posts():

@app.route("/posts/{page_number}")
def posts():
    if request.method=="GET":
        return render_template("")
    else 
    return "<h1> should be able to navigate through posts, comments, etc. </h1>"

@app.route("/posts/user/{user_id}")

@app.route("/posts/user/{user_id}/{page_number}")

