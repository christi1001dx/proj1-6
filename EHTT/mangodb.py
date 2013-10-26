from pymongo import MongoClient
from datetime import datetime

def connect():
    mango = MongoClient("db.stuy.cs")
    db = mango.admin
    db.authenticate('softdev', 'softdev')
    mangodb = mango.levenpoka
    logcol = mangodb.flynn
    postcol = mangodb.tron
    comcol = mangodb.clu


def login(username, password):
    if not username or not password:
        error = 'err0'
    found = logcol.find_one({"username":username, "password":password}, fields = {'_id':0})
    if not found:
        error = 'err1'
    elif password != found["password"]:
        error = 'err2'
    else:
        return found

def register(username, password, stat):
    if not username or not password:
        error = 'err0'
    found = logcol.find_one({"username":username})
    if found:
        error = 'err3'
    else:
        logcol.insert({"username":username, "password":password, "type": stat})

def getpost(name):
    if not name:
        error = 'err0'
    else:
        found = postcol.find_one({"name":name})
        if not found:
            error = 'err4'
        else:
            return found["txt"]

def getpostid(name): 
    found = postcol.find_one({"name":name})
    if not found:
        error = err4
    else:
        return name["id"]

def getcom(clu):
    found = comcol.find_one({"id":clu})
    if not found:
        error = 'err4'
    else:
        return found["coms"]

def getpostcom(tron):
    if not tron:
        error = 'err0'
    else:
        return getcom(getpostid(tron))

def newpost(mcp, sark):
    if not mcp or not sark:
        error = 'err0'
    else:
        found = postcol.find_one({"name": mcp})
        if found:
            error = 'err5'
        else:
            found = find_one({"num"})
            postcol.insert({"name":mcp,"txt":sark, "id":found["num"]})
            postcol.update({"num":found["num"]}, {"$set": {"num":found["num"]+1}})
            comcol.insert({"id" : found["num"], "coms":[]})

def newcomment(clu, comet, usr):
    if not usr or not comet:
        error = 'err0'
    else:
        found = comcol.find_one({"id":clu})
        if not found:
            error = 'err4'
        else:
            comcol.update({"id":clu}, {'$push':{"comment":comet,
                                              "user":usr,
                                              "date":datetime.utcnow}})

def removepost(name):
    if not name:
        error = 'err0'
    else:
        found = postcol.find_one({"name": mcp})
        if not found:
            error = 'err4'
        else:
            comcol.remove({"id":found["id"]}, True)
            postcol.remove({"id":found["id"]}, True)

def reset():
    mangodb.drop("levanpolka")
    mangodb = mango.levenpoka
    mangodb = mango.levenpoka
    logcol = mangodb.flynn
    postcol = mangodb.tron
    comcol = mangodb.clu
    postcol.insert({"no":1})


connect()
