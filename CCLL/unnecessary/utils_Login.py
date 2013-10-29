from pymongo import MongoClient
connection = MongoClient('db.stuycs.org')
SQL_Users = connection.admin
SQL_Users.authenticate('softdev','softdev')
#SQL_Users.createcollection("login_info")

def userNameExist (username):
    ans = 0
    if SQL_Users.login_info.find_one ({'username' : username}):
        print 'user exists'
        ans = 1
    else:
        print 'user does not exist'
    return ans

def authenticate (username, password):
    ans = 0
    if (userNameExist (username)== 1):
        db = SQL_Users.login_info
    try: 
        db.find ({'username' : username}, {'password' : password})
        print 'sucess!' 
        ans = 1
    except:
        print 'Failed Attempt!'
    print 'authentication compelete'
    return ans

def addUser (username, password):
    SQL_Users.login_info.insert ({'username' : username},{ 'password' : password})
    print 'user added'




    
