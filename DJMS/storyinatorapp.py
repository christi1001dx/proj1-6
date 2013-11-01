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

@app.route("/login", methods = ["GET", "POST"]):
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
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword'].encode("ascii","ignore")
        button = request.form['button']
        if button == "Submit":
            if (username == '' or password == '' or confirmpassword == ''):
                return render_template("register.html", message = "Please fill empty fields")
            elif password != confirmpassword:
                return render_template("register.html", message = "Please enter the same passwords.")
            else:
                if(auth.register(username,password)):
                    session["name"] = username    
                    return redirect("/members")
                else:
                    return render_template("register.html", message = "There is already an account under your name.")
        elif button == "Cancel":
            return render_template("register.html")

#@app.route("/     ", methods =["GET", "POST"])




@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")
    
    
if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
