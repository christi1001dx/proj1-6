from flask import Flask
from flask import session,url_for,request,redirect,render_template
from pymongo import MongoClient

import utils

db = MongoClient().db

app = Flask(__name__)
app.secret_key = 'maroon5'

@app.route("/")
def home():
    return redirect("/login")
#    return render_template("template.blogposts.html",posts=utils.getPosts('jasper',db.posts))

@app.route("/login",methods=['GET','POST'])
def login():
    print "yolo"
    if request.method=="GET":
	return render_template("template.login.html")
    else:
	button = request.form['button']
	print "yo"
	if button == 'Submit':
	    print "hiiiii"
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
    return render_template("template.post.html", post = utils.getPost(_id, db.posts))

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

@app.poute("/blogPost")
def individualPostPage (title, comment, author, comments):
    if request.method=="GET":
	return render_template("post.htm"l, title = title, author = author, comments = comments)
    else:
        newcomment = request.form['comment'].encode ('ascii',"ignore")
        finalComments = comments.append (newcomment)
        name = session['username']
        utils.addComments (name, comments)
        

        

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
