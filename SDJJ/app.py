from flask import Flask
from flask import render_template, redirect, url_for
from flask import session, request

import config as conf
import utils
import datetime

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY

@app.route("/")
def home():
        return render_template("home.html", posts = utils.getPosts())

@app.route("/post/<postTitle>")
def post(postTitle):
        post = utils.getPost(postTitle)
        if post is not None:
                return render_template("post.html", post = post)
        return error()

@app.route("/users")
def users():
        return render_template("users.html", users = utils.getUsers())
        
@app.route("/user/<username>")
def user(username):
        user = utils.getUser(username)
        if user is not None:
                return render_template("user.html", user = user) 
        return error()
        
@app.route("/submit_post", methods = ["GET", "POST"])
def submitPost():
        if request.method == "GET":
                return render_template("submit_post.html")

        title = request.form["title"]
        if utils.loggedIn() and utils.titleAvailable(title):
                        body = request.form["body"]
                        author = session["username"]
                        date = datetime.datetime.now()
                        utils.submitPost(title, body, author, date.replace(second=0, microsecond=0))
                        return redirect(url_for("home"))
        else:
                return error()


@app.route("/post/<postTitle>/submit_comment", methods = ["GET", "POST"])
def submitComment(postTitle):
        body = request.form["body"]
        if utils.loggedIn():
                author = session["username"]
        else:
                author = None
        date = datetime.datetime.now()
        utils.submitComment(postTitle, body, author, date.replace(second=0, microsecond=0))
        return redirect(url_for("post", postTitle = postTitle))

@app.route("/login", methods = ["GET", "POST"])
def login():
        if request.method == "GET":
                return render_template("login.html")

        elif not utils.loggedIn():
                username = request.form["username"]
                password = request.form["password"]
                if utils.authenticate(username, password):
                        session["username"] = username
                else:
                        return error()
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
        session.pop("username")
        return redirect(url_for("home"))

@app.route("/register", methods = ["GET", "POST"])
def register():
        if request.method == "GET":
                return render_template("register.html")

        elif not utils.loggedIn():
                username = request.form["username"]
                password = request.form["password"]
                passRetype = request.form["passRetype"]
                security = request.form["security"]
                answer = request.form["answer"]

                if utils.register(username, password, passRetype, security, answer):
                        return redirect(url_for("home"))
                else:
                        return error()
        else:
                return redirect(url_for("home"))

@app.route("/recover", methods=["GET", "POST"])
def recover():
    if request.method == "GET" :
        return render_template("recover.html")
    else:
        username = request.form['username']
        security = request.form['security']
        answer = request.form['answer']
        button = request.form['button']
        if button == "Submit":
            if (username == '' or answer == ''):
                return render_template("recover.html", message = "Please fill empty fields")
            else:   
                return render_template("recover.html", message = utils.recover(username,security,answer))
        elif button == "Cancel":
            return render_template("recover.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "GET" :
        return render_template("change.html")
    else:
        password = request.form['oldpassword']
        newpassword = request.form['newpassword']
        confirmnewpassword = request.form['confirmnewpassword']
        security = request.form['security']
        answer = request.form['answer']
        button = request.form['button']
        if button == "Submit":
            if (password == '' or newpassword == '' or confirmnewpassword == '' or answer == ''):
                return render_template("change.html", message = "Please fill empty fields")
            elif newpassword != confirmnewpassword:
                return render_template("change.html", message = "Please enter the same passwords.")
            else:
                if(utils.change(session["name"],newpassword)):   
                    return redirect("/members")
        elif button == "Cancel":
            return render_template("change.html")


def error():
        error = session["error"]
        return render_template("error.html", error = error)

if __name__ == "__main__":
        app.run(debug = True)