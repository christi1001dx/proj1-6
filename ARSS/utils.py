from pymongo import MongoClient

def mongo_init():
    client = MongoClient()
    db=client.ARSS
    return db

#####STORY FUNCTIONS######

def story_exists(title):
    db = mongo_init()
    return db.stories.find_one({'title':title})

def make_story(title, author, anonymous):
    db = mongo_init()
    ans = False
    if not story_exists(title):
        story = {}
        story['title'] = title
        story['lines'] = 0
        story['author'] = author
        story['anonymous'] = anonymous #boolean
        db.stories.insert(story)
        ans = True
    return ans

def delete_story(title):
    db = mongo_init()
    ans = False
    if story_exists(title):
        db.stories.remove({'title':title})
        ans = True
    return ans

def story_author(title):
    db = mongo_init()
    return db.stories.find_one({'title':title})['author']

def story_anonymous(title):
    db = mongo_init()
    return db.stories.find_one({'title':title})['anonymous']

def story_lines(title):
    db = mongo_init()
    return db.stories.find_one({'title':title})['lines']

def increment_lines(title):
    db = mongo_init()
    story = db.stories.find_one({'title':title})
    story['lines'] = story['lines'] + 1
    db.stories.save(story)

######LINE FUNCTIONS######

def add_line(line, title, user):
    db = mongo_init()
    storylines = story_lines(title)
    entry = {}
    entry['line'] = line
    entry['number'] = storylines + 1
    entry['story'] = title
    entry['user'] = user
    db.lines.insert(entry)
    increment_lines(title)

def return_all_lines(title):
    db = mongo_init()
    lineslist = list(db.lines.find({'title':title}))
    return lineslist

#####LOGIN FUNCTIONS######

from pymongo import MongoClient

def get_collection():
    connection = MongoClient()
    db = connection.login.users
    return db

# used for register
# user must type password 2 times to make account
def add_user(username, password, password2):
    if (get_collection().find_one({'username': username}, fields = {'_id': False})):
        return "copy"
    elif (password.__len__() < 4):
        return "short password"
    elif (password != password2):
        return "retype: passwords mismatch"
    else:
        get_collection().insert({'username': username, 'password': password})
        return "good job"

# used to validate login
def account_exists(username, password):
    for x in get_collection().find({'username': username, 'password': password}):
        return True
    else:
        return False

# used to change password to password2
def change_password(username, password, password2):
    if (password.__len__() < 4):
        return "too short"
    elif (password != password2):
        return "retype: password mismatch"
    else:
        get_collection().update({'username': username}, {'$set':{'password': password}})
        return "successfully changed password" 
