import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.blog

def register(user, pword):
    collection = db.users
    if((db.users.find( {"username":user}, fields={"_id":False} ))).count() > 0:
        return False
    else:
        db.info.insert( {"username":user, "password":pword, "admin":0} )
        return True

def addAdmin(user,pword):
    collection = db.users
    if ( (db.users.find({username:user}) ) ).count() > 0:
        return False
    else:
        db.info.insert( {"username":user, "password":pword, "admin":1} )
        return True

def unregister(user, pword):
    collection = db.users
    db.users.remove( {"user":user, "pword":pword} )
    return True

def authenticate(user, pword):
    collection = db.users
    if ((db.users.find( {"username":user}, {"password":pword} ))).count() > 0:
        return True
    else:
        return False

def checkAdmin(user):
    collection = db.users
    if((db.users.find( {"username":user},  "admin":1}))).count() > 0:
        return True
    else:
        return False

def post(user, post):
    collection = db.posts
    if(checkAdmin(user)):
#checkAdmin should actually happen earlier - when someone tries to post, not when they write a post and then attempt to upload it
        (db.posts.insert( {"name":"admin", "post":post} ))
        return True
    else:
        return False


def comment(user, comment,post):
    collection = db.comments
    db.comments.insert( {"name":user, "comment":comment, "post"=post} )
    return True

