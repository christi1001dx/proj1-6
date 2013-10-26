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
	if button == 'Login':
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
	else:
	    print "didn't og in "
	    return redirect("/register")
        
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
                print "Account Created"
                return redirect("/login")
            else:
                print "Username Taken, Try Again"
                return render_template("template.register.html")

@app.route("/blog/<name>")
def blog(name):
    return render_template("template.blogposts.html",posts = utils.getPosts(name,db.posts))

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
