from pymongo import MongoClient
from time import strftime

def auth (user, passwd, coll):
    return [x for x in coll.find({'username': user, 'password': passwd})] != []

def addUser (user, passwd, coll):
    coll.insert({'username': user, 'password': passwd})

def addPost (user, title, genre, text, coll):
    coll.insert({'username': user, 'date': strftime("%Y-%M-%d %H:%M:%S"), 'title': title, 'genre': genre, 'text': text})

def getPosts (user, coll):
    return [x for x in coll.find({'username':user}).sort([('date',-1)])]

def getPostsGenre(genre, coll):
    return [x for x in coll.find({'genre':genre}).sort([('date',-1)])]

def getPost(_id, coll):
    return [x for x in coll.find('_id':id)]
