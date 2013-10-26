from flask import Flask
from flask import  render_template, url_for, redirect, session, request
import urllib
import utils
import datetime
#Inputs:
#posts(title, content, time, ID)
app = Flask(__name__)
app.secret_key="wheeee"

@app.route("/")
def home():
    recentposts = str(utils.getRecent())
    return render_template("index.html", recentposts = recentposts)


@app.route("/newpost", methods = ['GET', 'POST'])
def newPost():
    if request.method == "GET":
        return render_template("newpost.html")
    elif request.form['button'] == "Cancel":
        return redirect("/")
    else:
        title = request.form["title"]
        content = request.form["content"]
        #utils.addPost will add the post to the database, and generate
        #and return an ID
        id = utils.addPost(title, session['username'], content, datetime.datetime.now())
        return redirect("/getpost?id="+id)

@app.route("/getpost")
def getPost():
    id = request.args.get("id")
    if utils.auth(id, session["username"]):
        post = utils.getPost(id)
        if post == None:
            return render_template("error.html")
        return render_template("post.html",post = post)
    

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)


