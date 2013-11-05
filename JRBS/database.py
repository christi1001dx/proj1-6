# JRBS - Interface with the SQLite database

from datetime import datetime
import hashlib
import re
import sqlite3

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

class User(object):
    def __init__(self, userid, name, display_name, password_hash=None):
        self.userid = userid
        self.name = name
        self.display_name = display_name
        self.password_hash = password_hash


class Post(object):
    def __init__(self, postid, title, author, date, slug, text=None,
                 summary=None, comments=None):
        self.postid = postid
        self.title = title
        self.author = author
        self.date = date
        self.slug = slug

        self.text = text
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


class Database(object):
    """Represents a single database."""
    def __init__(self, filename):
        self.filename = filename

    def _create(self, conn):
        """Creates a fresh database, assuming one doesn't exist."""
        with open(SCHEMA_FILE) as fp:
            script = fp.read()
        conn.executescript(script % {"version": SCHEMA_VERSION})

    def _execute(self, query, *args):
        """Execute a query, creating/updating the database if necessary."""
        with sqlite3.connect(self.filename) as conn:
            try:
                result = conn.execute("SELECT version FROM version")
                if result.fetchone()[0] < SCHEMA_VERSION:
                    self._create(conn)
            except sqlite3.OperationalError:
                self._create(conn)
            return conn.execute(query, args).fetchall()

    def _get_next_userid(self):
        """Return the next user ID in sequence."""
        r = self._execute("SELECT MAX(user_id) FROM users")
        return r[0][0] + 1 if r[0][0] else 1

    def _get_next_postid(self):
        """Return the next post ID in sequence."""
        r = self._execute("SELECT MAX(post_id) FROM posts")
        return r[0][0] + 1 if r[0][0] else 1

    def _get_comments_for_post(self, postid):
        """Get all the comments corresponding to a certain post."""
        query = "SELECT * FROM comments JOIN posts ON comment_post = post_id JOIN users ON comment_user = user_id WHERE post_id = ?"
        data = self._execute(query, postid)
        comments = []
        for comment in data:
            comments.append(Comment(comment[0], comment[15], comment[3],
                                    comment[4], comment[5], comment[6]))
        return comments

    def login(self, username, password):
        """Returns one of "no user", "bad password", "ok"."""
        r = self._execute("SELECT * FROM users WHERE user_name = ?", username)
        if not r:
            return "no user"
        user = User(*r[0])
        if user.password_hash != hashlib.sha256(password).hexdigest():
            return "bad password"
        return "ok"

    def register(self, username, display_name, password):
        """Returns one of "exists", "ok"."""
        r = self._execute("SELECT * FROM users WHERE user_name = ?", username)
        if r:
            return "exists"
        user_id = self._get_next_userid()
        pwhash = hashlib.sha256(password).hexdigest()
        self._execute("INSERT INTO users VALUES (?, ?, ?, ?)", user_id,
                      username, display_name, pwhash)
        return "ok"

    def get_posts(self, user=None, page=1):
        """Return a list of posts meeting the given conditions."""
        if user:
            query = "SELECT * FROM posts JOIN users ON post_user = user_id WHERE user_id = ?"
            results = self._execute(query, user)
        else:
            query = "SELECT * FROM posts JOIN users ON post_user = user_id"
            results = self._execute(query)
        posts = []
        for result in results:
            comments = self._get_comments_for_post(result[0])
            posts.append(Post(result[0], result[1], result[9], result[3],
                              result[6], result[4], result[5], comments))
        return posts

    def get_post(self, postid):
        """Return an individual post."""
        query = "SELECT * FROM posts JOIN users ON post_user = user_id WHERE post_id = ?"
        results = self._execute(query, postid)
        if not results:
            return None
        result = results[0]
        comments = self._get_comments_for_post(result[0])
        return Post(result[0], result[1], result[9], result[3],
                          result[6], result[4], result[5], comments)

    def create_post(self, title, content, author):
        """Creates a post. Returns one of "ok"."""
        postid = self._get_next_postid()
        user_query = "SELECT user_id FROM users WHERE user_name = ?"
        user = self._execute(user_query, author)[0][0]
        date = datetime.now()
        summary = content.split("\n\n")[0]
        slug = re.sub(r"[\W_]", "-", title.lower(), flags=re.UNICODE)[:50]
        self._execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)", postid,
                      title, user, date, content, summary, slug)
        return "ok"
