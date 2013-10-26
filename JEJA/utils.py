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
    #Lazy way: generate IDs until you get a unique one
    id = randrange(000000,999999)
    while db.Posts.find({'ID':id}).count() != 0:
        num = randrange(0000000,999999)
    
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
