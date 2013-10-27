from pymongo import MongoClient
from datetime import date

def auth (user, passwd, coll):
    return [x for x in coll.find({'username': user, 'password': passwd})] != []

def addUser (user, passwd, coll):
    coll.insert({'username': user, 'password': passwd})

def addPost (user, title, text, coll):
    coll.insert({'username': user, 'date': str(date.today()), 'title': title, 'text': text})

def getPosts (user, coll):
    return [x for x in coll.find({'username':'jasper'}).sort([('date',-1)])]

