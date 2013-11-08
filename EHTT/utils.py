from pymongo import MongoClient

def login(username,password):
    c = MongoClient()
    data = c['blogdb']
    x = data.users.find({'username':username, 'password':password})
    if x:
        return True
    else:
        return False

def register(username,password):
    c = MongoClient()
    data = c['blogdb']
    x = data.users.find({'username':username})
    if x:
        return False
    else:
        data.users.insert({'username':username, 'password':password})
        return True

def getAllPosts():
    c = MongoClient()
    data = c['blogdb']
    l = []
    for post in data.posts.find():
        l.append(post['title'])
    return l

def newPost(title,text,date):
    c = MongoClient()
    data = c['blogdb']
    data.posts.insert({'title':title, 'text':text, 'date':date})

def newComment(username,text,date,post):
    c = MongoClient()
    data = c['blogdb']
    data.comments.insert({'username':username, 'text':text, 'date':date, 'post':post})

def getAllComments(post):
    c = MongoClient()
    data = c['blogdb']
    username = []
    text = []
    date = []
    for comment in data.comments.find({'post':post}):
        username.append(comment['username'])
        text.append(comment['text'])
        date.append(comment['date'])
    comments = [username,text,date]
    return comments
    
def getPostText(title):
    c = MongoClient()
    data = c['blogdb']
    post = data.posts.find_one({'title':title}, fields = {'_id': False, 'text' : True})
    return post

def getPostDate(title):
    c = MongoClient()
    data = c['blogdb']
    post = data.posts.find({'title':title}).date
    return post

