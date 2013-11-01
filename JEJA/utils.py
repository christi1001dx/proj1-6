from pymongo import MongoClient
from random import randrange

#Database structure:
#Database is called JEJA
#Two tables: Posts and Users
#Posts: contains post objects
#    posts have title, author, content, date, and id
#Users: contains users
#    users have ID, Username



def addPost(title, author, content,date):
    #pretend I've sanitized inputs here
    con = MongoClient()
    db = client['JEJA']
    
    #Create a unique ID for each post
    #sort ids in descending order
    #grab highest ID, add 1
    currentIDs = db.Posts.find().sort("ID", -1)
    newID = currentIDs[0]['ID'] + 1
    
    db.Posts.insert({'Title':title,'Author':author,'Content':content,'Date':date,'ID': id})
    return id

def getPost(id):
    con = MongoClient()
    db = client['JEJA']
    post = db.Posts.find({'ID':id})
    if post.count() == 0:
        return None
    else:
        return post[0]

#temporary
def getRecent():
    return None
