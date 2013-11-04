from flask import Flask, url_for, request, redirect, render_template
from pymongo import MongoClient

def work():
    client = MongoClient()
    db = client["DJMSStory"]       
    return db

#User Stuf ---------------------------------------------------------------------------
def register(username, password):
    db = work()
    chk = db.DJMSStory.find_one({'username' :username})
    if(chk == None):
        db.DJMSStory.insert({'username':username, 'password' :password})
        return True
    else:
        return False
        
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
        
def checkuser(username):
    db = work()
    user = [x for x in db.DJMSStory.find({'username':username},fields={'_id':False})]
    if (len(user) == 0):
        return True
    else:
        return False


#Story stuff -----------------------------------------------------------------------
def makeStory(name, story, username, summary):
    db = work()
    chk = db.DJMSStory.find_one({'storyname' :name})
    if(chk == None):
        db.DJMSStory.insert({'storyname':name, 'story':story, 'author':username, 'summary': summary})
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

def printAll():
    db = work()
    storylist = list(db.storynames)
    return storylist

def chkStoryName(name):
    db = work()
    data = [x for x in db.DJMSStory.find({'storyname':name},fields={'_id':False})]
    if(len(data)==0):
        return "No Story found"
    else:
        return "Story found"
    
def delStory(name):
    db = work()
    db.DJMSStory.remove({'storyname':name})
    
def returnAuthor(name):
    db = work()
    data = [x for x in db.DJMSStory.find({'storyname':name},fields={'_id':False})]
    return data['author']

def returnAuthor(name):
    db = work()
    data = [x for x in db.DJMSStory.find({'storyname':name},fields={'_id':False})]
    return data['summary']
    
def returnStory(name):
    db = work(name)
    story = db.story.find({'story':story},fields={'_id':False})
    return story


           
             

