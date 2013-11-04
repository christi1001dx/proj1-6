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

def list_of_stories():
    db = mongo_init()
    stories = list(db.stories.find())
    storieslist = []
    for story in stories:
        storieslist.append(story['title'])
    return storieslist

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
    return True

def return_all_lines(title):
    db = mongo_init()
    lineslist = list(db.lines.find({'story':title}))
    return lineslist

def return_all_stories():
    storynames = list_of_stories()
    stories = []
    for story in storynames:
        entry={}
        entry['author'] = story_author(story)
        entry['numLines'] = story_lines(story)
        entry['title'] = story
        entry['lines'] = ""
        lines = return_all_lines(story)
        for line in lines:
            entry['lines'] += line['line'] + " "
        stories.append(entry)
    return stories

#####LOGIN FUNCTIONS######

# used for register
# user must type password 2 times to make account
def add_user(username, password, password2):
    db = mongo_init()
    if (db.users.find_one({'username': username}, fields = {'_id': False})):
        return "User Already Exists."
    elif (password.__len__() < 4):
        return "Password too short."
    elif (password != password2):
        return "Passwords do not match."
    else:
        db.users.insert({'username': username, 'password': password})
        return "good job"

# used to validate login
def account_exists(username, password):
    db = mongo_init()
    for x in db.users.find({'username': username, 'password': password}):
        return True
    else:
        return False

# used to change password 
# type in new password two times
def change_password(username, password, password2):
    db = mongo_init()
    if (password.__len__() < 5):
        return False
    elif (password != password2):
        return False
    else:
        db.users.update({'username': username}, {'$set':{'password': password}})
        return True

# used to change username 
# type in new username two times
def change_username(username, username2, password):
    db = mongo_init()
    if (username.__len__() < 5):
        return False
    elif (username != username2):
        return False
    else:
        db.users.update({'username': username}, {'$set':{'password': password}})
        return True
