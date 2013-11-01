# utils file for Flask app

import pymongo
import config as conf

client = pymongo.MongoClient(conf.db)
db = client.SDJJbloginator

users = db.users
posts = db.posts

def formatPosts():
	# retrieve posts for main page

def posts():
	return posts.find()

def post(post):
	return posts.find({ "id" : post })

def profiles():
	return users.find()

def profile(username):
	return users.find({ "username" : username })

def authenticate(username, passwordj):
	user = users.find_one({ "username" : username})
	if user is not None and password = user["password"]:
		return True
	return False

def login(username):
	session["username"] = username
