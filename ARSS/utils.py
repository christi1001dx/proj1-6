from pymongo import MongoClient
from flask import session

client = MongoClient()
db = client.ARSS

##### STORY FUNCTIONS ######

def _find_story(title):
	return db.stories.find_one({'title': title})

def _get_field(title, key):
	return _find_story(title)[key]


def story_exists(title):
	return db.stories.find({'title': title}).limit(1).count(True) > 0

def story_author(title):
	return _get_field(title, 'author')

def story_anonymous(title):
	return story_author(title) == None

def story_lines(title):
	return _get_field(title, 'lines')


def make_story(title, author=None):
	if not story_exists(title):
		story = {
		'title': title,
		'author': author,
		'lines': 0
		}
		db.stories.insert(story)
		return True
	return False

def delete_story(title):
	return db.stories.remove({'title': title}, safe=True)['n'] > 0

def increment_lines(title):
	db.stories.update({'title': title}, {'$inc': {'lines': 1}})

def list_of_stories():
	stories = list(db.stories.find())
	storieslist = []
	for story in stories:
		storieslist.append(story['title'])
	return storieslist

###### LINE FUNCTIONS ######

def add_line(line, title, user):
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
	lineslist = list(db.lines.find({'story':title}))
	return lineslist

def return_all_stories():
	storynames = list_of_stories()
	stories = []
	for story in storynames:
		entry={}
		entry['author'] = str(story_author(story))
		entry['numLines'] = str(story_lines(story))
		entry['title'] = str(story)
		entry['lines'] = ""
		lines = return_all_lines(story)
		for line in lines:
			entry['lines'] += line['line'].decode('utf-8') + " "
		stories.append(entry)
	return stories

##### LOGIN FUNCTIONS ######

# used for register
# user must type password 2 times to make account
def add_user(username, password, password2):
	if (db.users.find_one({'username': username}, fields = {'_id': False})):
		return "User Already Exists."
	elif (password.__len__() < 4):
		return "Password too short."
	elif (password != password2):
		return "Passwords do not match."
	else:
		db.users.insert({'username': username, 'password': password})
		return "good job"

def user_exists(username):
	for x in db.users.find({'username': username}):
		return True
	else:
		return False

# used to validate login
def account_exists(username, password):
	for x in db.users.find({'username': username, 'password': password}):
		return True
	else:
		return False

# used to change password
# type in new password two times
def change_password(username, password, password2):
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
	if (username.__len__() < 5):
		return False
	elif (username != username2):
		return False
	else:
		db.users.update({'username': username}, {'$set':{'password': password}})
		return True

def logged_in():
	if 'username' in session and not user_exists(session['username']):
		session.pop('username', None)
	return 'username' in session and session['username'] != None

if __name__ == '__main__':
	make_story('test1')
	print "Story exists? " + str(story_exists('test1'))
	print "Is story anonymous? " + str(story_anonymous('test1'))
	print "Story exists, Delete story: " + str(delete_story('test1'))
	print "Story just deleted, Delete story: " + str(delete_story('test1'))

	make_story('test1')
	print "Lines: " + str(story_lines('test1'))
	increment_lines('test1')
	increment_lines('test1')
	print "After 2 increments, Lines: " + str(story_lines('test1'))
