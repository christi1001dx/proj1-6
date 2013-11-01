# utils file for Flask app

import pymongo
import config as conf

client = pymongo.MongoClient(conf.db)
db = client.SDJJbloginator

users = db.users
posts = db.posts

def formatPosts():
	# retrieve posts for main page

def post(post):
	# retrieve post by number

def profile(username):

