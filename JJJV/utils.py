import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.users
collection = db.info

def adduser(user, pword):
    if((db.info.find( {"username":user}, fields={"_id":False} ))).count() > 0:
        return False
    else:
        db.info.insert( {"username":user, "password":pword, "admin":0} )
        return True
    
def authenticate(user, pword):
    if ((db.info.find( {"username":user}, {"password":pword} ))).count() > 0:
        return True
    else:
        return False

def checkAdmin(user):
    if((db.info.find( {"username":user},  "admin":1}))).count() > 0:
        return True
    else:
        return False

def post(user, post):
    if(checkAdmin(user)):
        (db.posts.insert( {"post":post} ))
        return True
    else:
        return False


def comment(user, comment):
