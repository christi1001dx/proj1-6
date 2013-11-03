# uid = user ID
# pid = post ID
# cid = comment ID


from pymongo import MongoClient
import index

c = MongoClient()


def getRecent():
    db = c.posts
    posts = db.Collections.find()
    posts.sort("date",-1)
    
    return posts


def addPost(title, uid, content, date):
    db = c.posts
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
