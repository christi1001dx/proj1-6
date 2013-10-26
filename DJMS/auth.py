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


