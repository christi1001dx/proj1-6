from pymongo import MongoClient
from datetime import datetime
from erutil import errorch
from erutil import errorlook


#def connect():
mango = MongoClient()
mangodb = mango.levenpoka 
logcol = mangodb.flynn #login collection
postcol = mangodb.tron #post collection
comcol = mangodb.clu #comment collection

def dlogin(username, password):
    if not username or not password:
        errorch(0)
    found = logcol.find_one({"username":username, "password":password}, fields = {'_id':0})
    if not found:
        errorch(1)
    elif password != found["password"]:
        errorch(2)
    else:
        return found

def dregister(username, password, stat):
    if not username or not password:
        errorch(0)
        print(errorlook())
        return 0
    found = logcol.find_one({"username":username})
    if found:
        errorch(3)
    else:
        logcol.insert({"username":username, "password":password, "type": stat})
        return 1

def dchangepw(username, password, newpw):
    if not username or not password or not newpw:
        errorch(0)
        return 0
    found = logcol.find_one({"username":username})
    if not found:
        errorch(1)
    elif password != found["password"]:
        errorch(2)
    else:
        logcol.update({"username":username}, {"password":newpw})
        return 1

#####################################################################################
def getpost(name):
    if not name:
        errorch(0)
    else:
        found = postcol.find_one({"name":name})
        if not found:
            errorch(4)
        else:
            return found["txt"]

def getpostid(name): 
    found = postcol.find_one({"name":name})
    if not found:
        errorch(4)
    else:
        return name["id"]

def getcom(clu):
    found = comcol.find_one({"id":clu})
    if not found:
        errorch(4)
    else:
        return found["coms"]

def getpostcom(tron):
    if not tron:
        errorch(0)
    else:
        return getcom(getpostid(tron))

def getallposts():
    l = [];
    for x in postcol.find({"f":"toe"}):
        l.insert(x)
    return l

###################################################################################
def newpost(mcp, sark):
    if not mcp or not sark:
        errorch(0)
    else:
        found = postcol.find_one({"name": mcp})
        if found:
            errorch(5)
        else:
            found = find_one({"num"})
            postcol.insert({"name":mcp,"txt":sark, "id":found["num"]})
            postcol.update({"num":found["num"]}, {"$set": {"num":found["num"]+1}})
            comcol.insert({"id" : found["num"], "coms":[]})
            return 1;

def newcomment(clu, comet, usr):
    if not usr or not comet:
        errorch(0)
    else:
        found = comcol.find_one({"id":clu})
        if not found:
            errorch(4)
        else:
            comcol.update({"id":clu}, {'$push':{"coms":{"comment":comet,
                                                        "user":usr,
                                                        "date":datetime.utcnow}}})
            return 1

#####################################################################################
def removepost(name):
    if not name:
        errorch(0)
    else:
        found = postcol.find_one({"name": mcp})
        if not found:
            errorch(4)
        else:
            comcol.remove({"id":found["id"]}, True)
            postcol.remove({"id":found["id"]}, True)
            return 1

def removecomment(clu, usr, comet):
    if not usr or not comet or not clu:
        errorch(0)
    else:
        found = comcol.find_one({"id":clu})
        if not found:
            errorch(4)
        else:
            x = found["coms"]
            for y in x:
                if (y["comment"] == comet) and (y["user"] == usr):
                    x.remove(y)
                    comcol.update({'id':clu}, {'$pull':{'coms':y}})
                    return 1

    
def reset():
    mangodb.drop("levanpolka")
    mangodb = mango.levenpoka
    mangodb = mango.levenpoka
    logcol = mangodb.flynn
    postcol = mangodb.tron
    comcol = mangodb.clu
    postcol.insert({"no":1})

######################################################################################

