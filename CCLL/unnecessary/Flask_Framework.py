from flask import Flask
from flask.ext import shelve
from flask import session,url_for,request,redirect,render_template

from pymongo import MongoClient
#connection = MongoClient('db.stuycs.org')
connection = MongoClient ()
#SQL_Users=connection.admin
#SQL_Users.authenticate('softdev','softdev')
print (connection.database_names())
import utils_Login
import utils

app = Flask(__name__)
app.secret_key="mysecretkey"
app.config['SHELVE_FILENAME'] = 'my_users.db'
shelve.init_app(app)

@app.route("/")
def home():
    if 'count' in session:
        return render_template("index.html")
    else:
        return redirect("/login")

@app.route("/count")
def count():
    try:
        c = session['count']
    except:
        c=0
    c=c+1
    session['count']=c
    page="""
    <h1>The count is: %d</h1>
    <a href="/count">count</a>
    """
    return page%(c)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("template.login.html")
    else:
	button = request.form['button']
	if button == 'Login':
            username = request.form['username'].encode ('ascii',"ignore")
	    password = request.form['password'].encode ('ascii',"ignore")
            if utils_Login.authenticate(username,password) == 1:
                session['username'] = username
                session['count'] = 1
                return redirect("/")
            else:
                return redirect ("/login")
                print 'login attempt failed. Try again.'
	else:
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
            if utils_Login.userNameExist (username) == 0:
                utils_Login.addUser (username, password)
                print "Account Created"
                return redirect("/login")
            else:
                print "Username Taken, Try Again"
                return render_template("template.register.html")

@app.route ("/newPost",methods = ["GET","POST"])
def newPost ():
    if request.method=="GET":
        return render_template("template.submit.html")
    else:
	button = request.form['button']
	if button == 'submit':
            title = request.form['title'].encode ('ascii',"ignore")
	    genre = request.form['genre'].encode ('ascii',"ignore")
	    blog = request.form['blog'].encode ('ascii',"ignore")
            username = session['username']           
            utils. addPost (username, title, blog, genre)
	else:
            return render_template("template.submit.html")

#@app.route ("/myPosts")
#def myPosts ():
 #   username = session['username']
  #  utils.getPosts (username)

@app.route("/logout")
def logout():
    session.pop('count',None)
    return redirect(url_for('home'))

if __name__=="__main__":
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
    
