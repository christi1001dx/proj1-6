from pymongo import MongoClient

#Database structure:
#Database is called JEJA
#Two tables: Posts and Users
#Posts: contains post objects
#    posts have title, author, content, date, and id
#Users: contains users
#    users have ID, Username

#Account Functions:
def createUser(username, password):
    con = MongoClient()
    db = client['JEJA']
    #username is too short
    if len(username) < 4:
        return 1
    #password is too short
    if len(password) < 6:
        return 2
    #check if acc is taken
    if len(list(db.Users.find({'Username':username}))) == 0:
        #generate userID:
        currentIDs = db.Users.find().sort("ID", -1)
        id = currentIDs[0]['ID'] + 1
        db.Users.insert({'Username': username, 'Password': password, 'ID':id})
        return 0
    #username is taken
    return 3


#Post Functions:
def addPost(title, author, content,date):
    #pretend I've sanitized inputs here
    con = MongoClient()
    db = con.Posts
    
    #Create a unique ID for each post
    #sort ids in descending order
    #grab highest ID, add 1
    currentIDs = len(db.find())
    print(currentIDs)
    #id = currentIDs[0]['ID'] + 1
    
    #db.Posts.insert({'Title':title,'Author':author,'Content':content,'Date':date,'ID': id})
    #return id

def getPost(id):
    con = MongoClient()
    db = client['JEJA']
    post = db.Posts.find({'ID':id})
    if post.count() == 0:
        return None
    else:
        return post[0]

#temporary
def getRecent():
    return None
