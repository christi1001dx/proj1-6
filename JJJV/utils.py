from pymongo import MongoClient

client = MongoClient(host='localhost',port=27017)
db = client.JJJV

users= db.users
posts= db.posts
comments= db.comments

def register(user, pword):
    if((users.find( {"username":user}, fields={"_id":False} ))).count() > 0:
        return False
    else:
        users.insert( {"username":user, "password":pword, "admin":0} )
        return True

def checkUser(user):
    if ( ( users.find( {"username":user} )).count() >0):
        return False
    else:
        return True
    
def addAdmin(user,pword):
    if ( (users.find({username:user}) ) ).count() > 0:
        return False
    else:
        users.insert( {"username":user, "password":pword, "admin":1} )
        return True

def unregister(user, pword):
    users.remove( {"user":user, "pword":pword} )
    return True

def authenticate(user, pword):
    if ((users.find( {"username":user}, {"password":pword} ))).count() == 1:
        return True
    else:
        return False

def checkAdmin(user):
    if( (users.find({"username":user}, {"admin":1})) ).count() == 1:
        return True
    else:
        return False

def post(user, title, post):
    #make sure only admins have option to post
    posts.insert( {"name":"admin", "title":title, "post":post} )
    return True


def comment(user, comment,post):
    dcomments.insert( {"name":user, "comment":comment, "post":post} )
    return True

    

