class User(object):
    def __init__(self, userid, name, display_name, password_hash=None):
        self.userid = userid
        self.name = name
        self.display_name = display_name
        self.password_hash = password_hash


class Post(object):
    def __init__(self, postid, title, author, date, slug, content=None,
                 summary=None, comments=None):
        self.postid = postid
        self.title = title
        self.author = author
        self.date = date
        self.slug = slug

        self.content = content
        self.summary = summary
        self.comments = comments


class Comment(object):
    def __init__(self, cid, user, date, text, anon_name=None, anon_email=None):
        self.cid = cid
        self.user = user
        self.date = date
        self.text = text
        self.anon_name = anon_name
        self.anon_email = anon_email
