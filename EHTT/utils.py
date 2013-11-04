from pymongo import MongoClient

def login(username,password):
    c = MongoClient()
    db = c['blogdb']
    x = db.users.find({'username':username, 'password':password})
    if x:
        return True
    else:
        return False

def register(username,password):
    c = MongoClient()
    db = c['blogdb']
    x = db.users.find({'username':username})
    if x:
        return False
    else:
        db.users.insert({'username':username, 'password':password})
        return True

def getAllPosts():
    c = MongoClient()
    db = c['blogdb']
    l = []
    for post in db.posts.find():
        l.insert(post['name'])
    return l

def newPost(name,text,date):
    c = MongoClient()
    db = c['blogdb']
    c.posts.insert({'name':name, 'text':text, 'date':date})

def newComment(username,text,date,post):
    c = MongoClient()
    db = c['blogdb']
    c.comments.insert({'username':username, 'text':text, 'date':date, 'post':post})

def getAllComments(post):
    c = MongoClient()
    db = c['blogdb']
    username = []
    text = []
    date = []
    for comment in db.comments.find({'post':post}):
        username.insert(comment['username'])
        text.insert(comment['text'])
        date.insert(comment['date'])
    comments = [username,text,date]
    return comments
    
def getPostText(name):
    c = MongoClient()
    db = c['blogdb']
    post = db.posts.find({'name':name}).date
    return post

def getPostDate(name):
    c = MongoClient()
    db = c['blogdb']
    post = db.posts.find({'name':name}).date
    return post

