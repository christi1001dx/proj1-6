from flask import Flask
from flask import request, render_template, redirect, session, url_for
import auth


app = Flask(__name__)
app.secret_key = "shhhh"

@app.route("/")
def home():
    return redirect("/home")

@app.route("/home")
def homepage():
    return  render_template("login.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username = request.form["username"].encode("ascii","ignore")
        password = request.form["password"].encode("ascii","ignore")
        button = request.form['button']
        if button == "Login":
            if auth.check(username,password):
                session["name"] = username
                return redirect("/storylist")
            else:
                return redirect("/register")
        elif button == "Cancel":
                return render_template("login.html")
                
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET" :
        return render_template("register.html",message = "Please register")
    else:
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if (username == '' or password == '' or confirmpassword == ''):
            return render_template("register.html", message = "Please fill empty fields")
        elif password != confirmpassword:
            return render_template("register.html", message = "Please enter the same passwords.")
        elif (checkuser(username) == True):
            return render_template("register.html", message = "Username already taken. Please choose another username.")
        else:
            if(auth.register(username,password)):
                session["name"] = username    
                return redirect("/storylist")
            else:
                return render_template("register.html", message = "There is already an account under your name.")
        


@app.route("/<storytitle>", methods = ["GET", "POST"])
def story(title = None):
    if request.method == "GET" :
        return render_template("story.html")
    else:
        Addition = request.form['addition'].encode("ascii","ignore")
        button = request.form['button']
        if button == "Delete":
            delStory(title)
            return redirect("/storylist")
        if button == "Submit":
                editStory(title, addition)
                return render_template("story.html")
                
@app.route("/storylist", methods = ["GET", "POST"])
def storylist():
    if request.method == "GET":
        return render_template("home.html")
    else:
        return for i in len(printall()):
                printall.pop()

    
@app.route("/createstory", methods = ["GET", "POST"])
def make():
    if request.method == "GET" :
        return render_template("createstory.html")
    else:
        author =  request.form['password'].encode("ascii","ignore")
        password = request.form['password'].encode("ascii","ignore")
        title = request.form['title'].encode("ascii","ignore")
        summary = request.form['summary'].encode("ascii","ignore")
        story = request.form['story'].encode("ascii","ignore")
        button = request.form['button']
        if button == "Submit":
            if (author == '' or password == '' or story == ''):
                return render_template("createstory.html", message = "Please fill empty fields")
            elif (auth.check(author,password) == False):
                return render_template("createstory.html", message = "Username and Password do not match. Please try again")
            else:
                makeStory(title, story, author)
                return redirect("/<title>")
        elif button == "Cancel":
            return render_template("createstory.html")
            

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")
    
    
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
