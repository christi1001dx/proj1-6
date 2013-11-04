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

    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1

    r = ""
    posts = utils2.getRecent(page)
    nav = utils2.nav([["Home"]])
    for x in posts:
        r += str(index.formatData(uid,x))


    return render_template("index.html", data=r,head=h,type=request.args.get("type"),uid=uid,nav=nav,pages=utils2.pagination(page,utils2.indexMaxPages()))

@app.route("/register",methods=['GET','POST'])
def register():
    nav = utils2.nav([["/","Home"],["Register"]])
    if request.method == "POST":
        if request.form["password"] == request.form["password2"]:
            if auth.createUser(str(request.form["username"]),str(request.form["password"])):
                return redirect("/login?type=2")
            else:
                return render_template("register.html",type=1,nav=nav)
        else:
            return render_template("register.html",type=2,nav=nav)
    else:
        return render_template("register.html",nav=nav)
@app.route("/logout")
def logout():
    session.pop("uid",None)
    session.pop("username",None)
    return redirect("/?type=3")
@app.route("/login", methods=['GET','POST'])
def login():
    nav = utils2.nav([["/","Home"],["Login"]])
    if request.method == "POST":
        uu = auth.authorize(str(request.form["username"]), str(request.form["password"]))
        if uu:
            session["uid"] = uu
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            return redirect("/?type=2")
        else:
            return render_template("login.html",type='1',nav=nav)
    else:
        return render_template("login.html",type=request.args.get("type"),nav=nav)


@app.route("/new-post", methods = ['GET', 'POST'])
def newPost():
    nav = utils2.nav([["/","Home"],["Create New Post"]])
    uid = getUID()
    h = index.getHeader(uid)
    if request.method == "GET":
        return render_template("newPost.html",head=h,nav=nav)
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
    postString = str(index.formatData(uid,post))

    nav = utils2.nav([["/","Home"],[post["title"]]])
    
    return render_template("index.html",data=postString,head=h,type=request.args.get("type"),uid=uid,nav=nav)

@app.route("/edit",methods=['GET','POST'])
def editPost():
    nav = utils2.nav([["/","Home"],["Edit Post"]])
    uid = getUID()
    h = index.getHeader(uid)

    if request.method == "GET":
        pid = int(request.args.get("id"))
    
        post = utils2.getPost(pid)
        if uid == post["uid"]:
            return render_template("editPost.html",post=post,head=h,nav=nav)
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


