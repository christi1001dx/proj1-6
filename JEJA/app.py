from flask import Flask, render_template, url_for, redirect, session, request
import auth
import index
import urllib
import utils
import utils2
import datetime
#Inputs:
#posts(title, content, time, ID)

app = Flask(__name__)
app.secret_key = 'sdfsdgwg'


def getUID():
    if "uid" in session:
        return session["uid"]
    else:
        return -1

@app.route("/")
def home():
    uid = getUID()
    h = index.getHeader(uid)
    print(h)
    r = ""
    posts = utils2.getRecent()
    for x in posts:
        r += str(index.formatData(uid,x))
    
    return render_template("index.html", data=r,head=h,type=request.args.get("type"),uid=uid)

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":
        if request.form["password"] == request.form["password2"]:
            if auth.createUser(str(request.form["username"]),str(request.form["password"])):
                return redirect("/login?type=2")
            else:
                return render_template("register.html",type=1)
        else:
            return render_template("register.html",type=2)
    else:
        return render_template("register.html")
@app.route("/logout")
def logout():
    session.pop("uid",None)
    session.pop("username",None)
    return redirect("/?type=3")
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        uu = auth.authorize(str(request.form["username"]), str(request.form["password"]))
        if uu:
            session["uid"] = uu
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            return redirect("/?type=2")
        else:
            return render_template("login.html",type='1')
    else:
        return render_template("login.html",type=request.args.get("type"))


@app.route("/new-post", methods = ['GET', 'POST'])
def newPost():
    uid = getUID()
    h = index.getHeader(uid)
    if request.method == "GET":
        return render_template("newPost.html",head=h)
    elif request.form["submit"] == "Cancel":
        return redirect("/")
    elif request.form["submit"] == "Create Post":
        title = request.form["title"]
        content = request.form["content"]
        #utils.addPost will add the post to the database, and generate
        #and return an ID
        post = utils2.addPost(title, uid, content, datetime.datetime.now())
        return redirect("/post?id="+str(post))

@app.route("/comment", methods=['POST'])
def addComment():
    uid = getUID()
    pid = request.form["pid"]
    comment = request.form["comment"]
    utils2.addComment(uid,pid,comment,datetime.datetime.now())
    return redirect("/post?id="+pid)

@app.route("/post")
def getPost():
    uid = getUID()
    h = index.getHeader(uid)
    pid = int(request.args.get("id"))
    post = utils2.getPost(pid)
    post = str(index.formatData(uid,post))
    return render_template("index.html",data=post,head=h,type=request.args.get("type"),uid=uid)

@app.route("/edit",methods=['GET','POST'])
def editPost():
    uid = getUID()
    h = index.getHeader(uid)

    if request.method == "GET":
        pid = int(request.args.get("id"))
    
        post = utils2.getPost(pid)
        if uid == post["uid"]:
            return render_template("editPost.html",post=post,head=h)
    else:
        pid = int(request.form["pid"])
        post = utils2.getPost(pid)
        if uid == post["uid"]:
            utils2.editPost(pid,request.form["title"],request.form["content"])
            return redirect("/post?id="+str(pid)+"&type=1")

@app.route("/delete",methods=['GET','POST'])
def delPost():
    uid = getUID()
    h = index.getHeader(uid)
    
    if request.method == "GET":
        pid = int(request.args.get("id"))
        post = utils2.getPost(pid)
        if uid == post["uid"]:
            return render_template("confirmDelete.html",post=post,head=index.getHeader(uid))
    else:
        pid = int(request.form["pid"])
        post = utils2.getPost(pid)
        if uid == post["uid"]:
            utils2.delPost(pid)
            return redirect("/?type=4")

@app.route("/like")
def likePost():
    uid = getUID()
    pid = int(request.args.get("id"))
    post = utils2.getPost(pid)

    # Of course you like your own post!
    if uid != -1 and uid != post["uid"]:
        utils2.likePost(uid,pid)
    return redirect("post?id="+str(pid))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)


