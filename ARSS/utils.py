from pymongo import MongoClient
from flask import session

client = MongoClient()
db = client.ARSS
#db.stories.drop_index('title_1')
db.stories.ensure_index('title', unique=True)

def record_exists(collection, query, limit=1):
	return collection.find(query, limit=1).count(True) > 0

##### STORY FUNCTIONS ######

def _get_next_seq(key):
	query = {'_id': key}
	# create if does not exist
	db.counters.update(query, {'$setOnInsert': {'seq': 0}}, upsert=True)
	return db.counters.find_and_modify(
		query=query,
		update={'$inc': {'seq': 1}},
		upsert=True
	)['seq']

def _find_story(title):
	return db.stories.find_one({'title': title})

def _get_field(title, key):
	return _find_story(title)[key]

def story_exists(title):
	return record_exists(db.stories, {'title': title})

def story_author(title):
	return _get_field(title, 'author')

def story_anonymous(title):
	return story_author(title) == None

def story_lines(title):
	return _get_field(title, 'lines')

def make_story(title, author=None):
	if not story_exists(title):
		story = {
			'_id': _get_next_seq('story_id'),
			'title': title,
			'author': author,
			'lines': 0
		}
		db.stories.insert(story)
		return True
	return False

def delete_story(title):
	return db.stories.remove({'title': title})['n'] > 0

def increment_lines(title):
	# returns the new value after increment
	return db.stories.find_and_modify(
		query={'title': title},
		update={'$inc': {'lines': 1}},
		new=True
	)['lines']

def list_of_stories():
	return [story['title'] for story in db.stories.find()]

###### LINE FUNCTIONS ######

def add_line(line, title, user):
	entry = {
	'line': line,
	'number': increment_lines(title),
	'story': title,
	'user': user
	}
	db.lines.insert(entry)
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
		entry['lines'] = ''
		lines = return_all_lines(story)
		for line in lines:
			entry['lines'] += line['line'].decode('utf-8') + ' '
		stories.append(entry)
	return stories

##### LOGIN FUNCTIONS ######

def user_exists(username):
	return record_exists(db.users, {'username': username})

# used to validate login
def account_exists(username, password):
	return record_exists(db.users, {'username': username, 'password': password})

def upsert_user(username, password):
	db.users.update(
		{'username': username},
		{'password': password},
		upsert=True
	)

# used for register
# user must type password 2 times to make account
def register_user(username, password, confirm_password):
	if (user_exists(username)):
		return 'User Already Exists.'
	elif (len(password) < 4):
		return 'Password too short.'
	elif (password != confirm_password):
		return 'Password does not match confirmation.'
	else:
		upsert_user(username, password)
		return 'Success!'

# used to change password
# type in new password two times
def change_password(username, password, confirm_password):
	if (len(password) < 4):
		return 'Password too short.'
	elif (password != confirm_password):
		return 'Password does not match confirmation.'
	else:
		upsert_user(username, password)
		return 'Success!'

# used to change username
def change_username(username, new_username):
	db.users.update({'username': username}, {'username': new_username})

def logged_in():
	if 'username' in session and not user_exists(session['username']):
		session.pop('username', None)
	return 'username' in session and session['username'] != None

if __name__ == '__main__':
	db = client.test
	db.counters.remove()
	db.stories.remove()

	print('Testing story')
	print('\tMaking story: ' + str(make_story('test1')))
	print('\tMaking existing story: ' + str(make_story('test1')))
	print('\tStory: ' + str(_find_story('test1')))
	print('\tStory exists? ' + str(story_exists('test1')))
	print('\tIs story anonymous? ' + str(story_anonymous('test1')))
	db.stories.update({'title': 'test1'}, {'$set': {'author': 'AuthorName'}})
	print('\tAdded author, is story anonymous? ' + str(story_anonymous('test1')))
	print('\tStory lines: ' + str(story_lines('test1')))
	increment_lines('test1')
	increment_lines('test1')
	print('\tAfter 2 increments: ' + str(_find_story('test1')))
	print('\tStory exists, Delete story: ' + str(delete_story('test1')))
	print('\tStory just deleted, Delete again: ' + str(delete_story('test1')))
	print('\tDelete unexisting story: ' + str(delete_story('tasdasd')))

	print('Testing _get_next_seq')
	make_story('test1')
	make_story('test2')
	for x in db.stories.find():
		print('\t' + str(x))
	print('\t' + str(db.counters.find_one({'_id': 'story_id'})))

	print('Stories: ' + str(list_of_stories()))
