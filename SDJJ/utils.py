import pymongo
from bson.objectid import ObjectId
import config as conf

client = pymongo.MongoClient(conf.db)
db = client.SDJJbloginator

users = db.users
posts = db.posts
comments = db.comments

def submitPost(title, body, author):
	posts.insert({ "title" : title, "body" : body, "author" : author })

def submitComment(postTitle, body, author):
	comments.insert({ "postTitle" : postTitle, "body" : body, "author" : author })

def getPosts():
	return posts.find()

def getPost(postTitle):
	post = posts.find_one({ "title" : postTitle })
	if post is not None:
		post["comments"] = comments.find({ "postTitle" : post["title"] })
	return post

def getUsers():
	return users.find()

def getUser(username):
	user = users.find_one({ "username" : username })
	if user is not None:
		user["posts"] = posts.find({ "author" : username })
		user["comments"] = comments.find({ "author" : username })
	return user

def authenticate(username, password):
	user = users.find_one({ "username" : username })
	return user is not None and user["password"] == password

def register(username, password):
	if users.find_one({"username" : username}) is None:
		users.insert({ "username" : username, "password" : password })
		return True
	else:
		return False
