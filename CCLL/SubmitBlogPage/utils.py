from pymongo import MongoClient

def auth (user, passwd, coll):
    return [x for x in coll.find({'username': user, 'password': passwd})] != []

def addUser (user, passwd, coll):
    coll.insert({'username': user, 'password': passwd})

def addPost (user, date, text, coll):
    coll.insert({'username': user, 'date': date, 'text': text})

def getPosts (user, coll):
    return [x for x in coll.find({'username':user}).sort({'date':-1})]
