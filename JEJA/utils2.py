# uid = user ID
# pid = post ID
# cid = comment ID


from pymongo import MongoClient
import index
import math


c = MongoClient()

# max posts per page
MAX_POSTS = 5

def getRecent(page):
    db = c.posts
    posts = db.Collections.find().sort("date",-1)
    
    r = []
    for x in range(0,min(page*MAX_POSTS,posts.count())):
        if x >= (page-1)*MAX_POSTS:
            r.append(posts[x])

    return r


def addPost(title, uid, content, date):
    db = c.posts
    if db.Collections.count() == 0:
        pid = 1
    else:
        pid = db.Collections.find({}).sort("id",-1).limit(1)[0]["id"]+1


    db.Collections.insert({"id":pid,"title":title,"uid":uid,"content":content,"date":date})
    return pid

def getPost(pid):
    db = c.posts
    post = db.Collections.find_one({"id":pid})
    return post

def editPost(pid,title,content):
    db = c.posts
    db.Collections.update({"id":pid},{"$set":{"title":title,"content":content}})

def delPost(pid):
    db = c.posts
    db.Collections.remove({"id":pid})

def likePost(uid,pid):
    db = c.likes
    if db.Collections.find({"pid":pid,"uid":uid}).count() == 0:
        db.Collections.insert({"pid":pid,"uid":uid})
    else:
        db.Collections.remove({"pid":pid,"uid":uid})


def getLikes(pid):
    db = c.likes
    lik = db.Collections.find({"pid":pid})

    r = ""

    count = lik.count()
    for x in range(0,count):
        if x == 0:
            r += '<span class="glyphicon glyphicon-thumbs-up"></span>'
        r += ' <strong>'+uidToUsername(lik[x]["uid"])+'</strong>'
        if x+1 != count:
            r += ','
    return r

def userLikesPost(uid,pid):
    db = c.likes
    return db.Collections.find({"pid":pid,"uid":uid}).count()

def uidToUsername(uid):
    db = c.users
    user = db.Collections.find_one({"id":uid})
    if user:
        return user["username"]
    else:
        return None

def addComment(uid,pid,comment,date):
    db = c.comments
    cid = db.Collections.count()+1
    db.Collections.insert({"id":cid,"pid":pid,"uid":uid,"content":comment,"date":date})

def getComments(pid):
    db = c.comments
    com = db.Collections.find({"pid":str(pid)})
    com.sort("id",-1)
    return com

def nav(stuff):
    r = '<ol class="breadcrumb">'

    for x in stuff:
        if len(x) == 1:
            r += '<li class="active">%s</li>'%(x[0])
        else:
            r += '<li><a href="%s">%s</a></li>'%(x[0],x[1])
    
    r += '</ol>'
    return r


def indexMaxPages():
    db = c.posts
    return math.floor((db.Collections.count()-1)/MAX_POSTS)+1

def pagination(cur,n):
    # n = max
    r = '<ul class="pagination">'
    
    if cur == 1:
        r += '<li class="disabled"><a href="/">&laquo;</a></li>'
    else:
        r += '<li><a href="/?page=%d">&laquo;</a></li>'%(cur-1)

    for x in range(1,int(n)+1):
        if x == cur:
            r += '<li class="active"><a href="/?page=%d">%d</a></li>'%(x,x)
        else:
            r += '<li><a href="/?page=%d">%d</a></li>'%(x,x)

    if cur == n:
        r += '<li class="disabled"><a href="/">&raquo;</a></li>'
    else:
        r += '<li><a href="/?page=%d">&laquo;</a></li>'%(cur+1)

    
    r += '</ul>'

    return r
