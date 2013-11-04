from flask import Flask
from flask import session,url_for,request,redirect,render_template
from pymongo import MongoClient

import utils

db = MongoClient().db

app = Flask(__name__)
app.secret_key = 'maroon5'

if db.posts.count() == 0:
    utils.addPost("admin","WELCOME!","Other","Please make an account and begin blogging!",db.posts)

@app.route("/")
def home():
    if 'username'  in session:
        username = session ['username']
	print utils.getRandPost(db.posts)
        return render_template("template.index.html", featured = utils.getRandPost(db.posts), sports = utils.getPostsGenre("Sports",db.posts), arts = utils.getPostsGenre("Arts",db.posts),opinions= utils.getPostsGenre("Opinion",db.posts),humor = utils.getPostsGenre("Humor",db.posts),academics = utils.getPostsGenre("Academics",db.posts), name = session['username'])
    else:
        return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    print "yolo"
    if request.method=="GET":
	return render_template("template.login.html")
    else:
	button = request.form['button']
	print "yo"
	if button == 'Submit':
            username = request.form['username'].encode ('ascii',"ignore")
	    password = request.form['password'].encode ('ascii',"ignore")
            if utils.auth(username,password,db.login):
		print "logged in!"
                session['username'] = username
                return redirect("/blog/"+username)
            else:
                return redirect ("/login")
                print 'login attempt failed. Try again.'
        
@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method=="GET":
	return render_template("template.register.html")
    else:
	button = request.form['button']
	if button == "Submit":
	    username = request.form['username'].encode ('ascii',"ignore")
	    password = request.form['password'].encode ('ascii',"ignore")
            if not utils.auth(username,password,db.login):
		utils.addUser(username,password,db.login)
                return redirect("/login")
            else:
                return render_template("template.register.html")

@app.route("/blog/<name>")
def blog(name):
    b = 0
    if session['username'] == name:
	b = 1
	return render_template("template.blogposts.html",posts = utils.getPosts(name,db.posts), mypage = b, name = name)

@app.route("/blog/<name>/submit", methods = ["GET","POST"])
def submit(name):
    if request.method=="GET":
	return render_template("template.submit.html")
    else:
	button = request.form['button']
	if button == "Submit":
	    title = request.form['title'].encode('ascii',"ignore")
	    text = request.form['text']
	    genre = request.form['genre']
	    if title and text:
		utils.addPost (session['username'], title, genre, text, db.posts)
		return redirect("/blog/" + session['username'])
	    else:
		return render_template("template.submit.html")
	else:
	    return render_template("template.submit.html")

@app.route("/post/<_id>")
def post(_id):
    name = session['username']
    if request.method=="GET":
	print utils.getPost(_id, db.posts)
        return render_template("template.post.html", post = utils.getPost(_id, db.posts)[0], name = name)
    else:
        newcomment = request.form['comment'].encode ('ascii',"ignore")
        finalComments = comments.append (newcomment)
        utils.addComments (_id,name, finalComments, db.posts)
        return render_template("template.post.html", post = utils.getPost(_id, db.posts)[0])

@app.route("/genre/<genre>")
def genre(genre):
    genre = genre.title()
    print genre
    return render_template("template.genre.html", genre = genre, posts = utils.getPostsGenre(genre, db.posts), name = name)

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=80)
