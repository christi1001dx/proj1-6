from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3

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
        if button == "Register":
            if not box:                
                return render_template("register.html", message = "you need to check the box first")
            elif stuff.check(username) :
                session["name"] = username
                return redirect(url_for('posts'))
            else:
                return render_template("register.html", message = "wrong username/pw combo")   
        
@app.route("/new")
def new():
    button = request.form["cancel"]
    if request.method=="GET":
        return render_template("new.html")
    elif button:
        return redirect(url_for('posts'))
    else:
        title = request.form["title"]
        post = request.form["post"]
        stuff.add(title, post)
        return redirect(url_for('posts'))

#@app.route("/archive")
#def archive():                     ****don't really see the difference b/w this and /posts, so will
#    if request.method=="GET":        comment this out for now******
#        return render_template

#@app.route("/admin") ******leaving this blank for now. saving for later.*****
#def admin(): *****admin should be able to delete posts and stuff here****

@app.route("/posts")
def posts():
    button = request.form["users"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts.html")
    elif button:
        if 'username' in session:
            user_id = stuff.getUser()
            return redirect(url_for('posts/user/{user_id}'))
        else
            page_number = page #don't think this works, but putting it here anyway
            return redirect(url_for('posts/{page_number}')

@app.route("/posts/{page_number}")
def posts():
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts") #dunno what to do here, maybe use databse to create the page?
    elif button == "home"
        return redirect(url_for('posts')
    else
        page_number = page
        return redirect(url_for('posts/{page_number}')
    
@app.route("/posts/user/{user_id}")
def posts():
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts") #same as above
    elif button == "home"
        return redirect(url_for('posts')
    else 
        page_number = page
        return redirect(url_for('posts/user/{user_id}/{page_number}'))

@app.route("/posts/user/{user_id}/{page_number}")
def posts():
    button = request.form["home"]
    page = request.form["pagenumber"]
    if request.method=="GET":
        return render_template("posts") # same as above
    elif button == "home"
        return redirect(url_for('posts')
    else
        page_number = page
        return redirect(url_for('posts/user/{user_id}/{page_number}'))
