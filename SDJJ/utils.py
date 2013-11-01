# database/authentication utils for Flask app

import pymongo
import config as conf

client = pymongo.MongoClient(conf.db)
db = client.SDJJbloginator

users = db.users
posts = db.posts

def posts():
	return posts.find()

def query(query):
	# returns dictionary with keys {"posts", "profiles", "comments"}
	# values are arrays containing query results for each
	# querying should be conducted with a regex match on the query string

# post should contain author, title, data, subjet line, body, comments
def post(post):
	return posts.find({ "id" : post })

def profiles():
	return users.find()

# profile should contain username, date joined, comments
def profile(username):
	return users.find({ "username" : username })

def authenticate(username, passwordj):
	user = users.find_one({ "username" : username})
	if user is not None and password = user["password"]:
		return True
	return False

def login(username):
	session["username"] = username

def register(username, password):
	# insert username, password pair into db
