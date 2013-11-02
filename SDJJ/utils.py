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

def userpost(username, post):
    temp = [x for x in users.find({'username':username},fields={'_id':False})]
    temp =  temp[0]['posts']
    postsize = posts.count()
    temp.extend([postsize])
    user.update({'username':username},{'$set':{'posts':temp}})
    posts.insert({'postid':postsize + 1,'user':username,'post':post,'comments':[]})

def usercomment(username, post, comment):
    temp = [x for x in users.find({'post':post},fields={'_id':False})]
    postnum = temp[0][postid]
    temp = temp[0]['comments']
    temp.extend[comment]
    commentid = temp.len() + 1
    posts.update({'post':post},{'$set':{'comments':temp}})
    temp = [x for x in user.find({'username':username},fields={'_id':False})]
    temp = temp[0]['comments']
    temp.extend([postnum*31415 + commentid*27182])
    user.update({'username':username},{'$set':{'comments':temp}})



def profiles():
	return users.find()

# profile should contain username, date joined, comments
def profile(username):
	return users.find({ "username" : username })

def authenticate(username, passwordj):
	user = users.find_one({ "username" : username})
	if user is not None and password == user["password"]:
		return True
	return False

def login(username):
	session["username"] = username

def register(username,password):
    db = work()
    chk = db.user.find_one({'username':username})
    if(chk == None):
       db.accounts.insert({'username':username,'password':password,'posts':[],'comments':[]})
       return True
    else:
        return False