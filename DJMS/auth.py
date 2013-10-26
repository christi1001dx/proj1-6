from flask import Flask, url_for, request, redirect, render_template
from pymongo import MongoClient

def work():
    client = MongoClient()
    try:
        db = clients["DJMSStory"]
    except:
        pass
    return db;

def register(username, password):
    db = work()
    chk = db.DJMSStory.find_one({'username' :username})
    if(chk == None):
        db.DJMSStory.insert({'username':username, 'password' :password})
    else:
        return "Account Registered"

def makeStory(name, story):
    db = work()
    chk = db.DJMSStory.find_one({'storyname' :name})
    if(chk == None):
        db.DJMSStory.insert({'storyname':name, 'story' :story})
    else:
        return "There is a story under that name"

def editStory(name, addition):
    db = work()
    data = [x for x in db.DJMSStory.find({'storyname':name},fields={'_id':False})]
    if(len(data)==0):
        return "No Story found"
    data = data[0]
    newStory = data['story'] + addition
    db.DJMSStory.update({'storyname':name},{'$set':{'story':newStory}})
    
def delStory(name):
    db = work()
    db.DJMSStory.remove({'name':{'$gt':name}})
    
def check(username,password):
    db = work()
    user = [x for x in db.DJMSStory.find({'username':username,'password':password},fields={'_id':False})]
    if (len(user) == 0):
        return "User Not Found"
    user =  user[0]
    if username == user['username'] and password == user['password']:
        return True
    else:
        return False 

           
             
            
            
            


