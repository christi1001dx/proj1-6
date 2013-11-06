# JRBS - Interface with the SQLite database

from datetime import datetime
import hashlib
import math
import re
import sqlite3

from objects import User, Post, Comment

PAGE_SIZE = 5

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

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
        result = self._execute("SELECT MAX(user_id) FROM users")
        return result[0][0] + 1 if result[0][0] else 1

    def _get_next_postid(self):
        """Return the next post ID in sequence."""
        result = self._execute("SELECT MAX(post_id) FROM posts")
        return result[0][0] + 1 if result[0][0] else 1

    def _get_next_commentid(self):
        """Return the next comment ID in sequence."""
        result = self._execute("SELECT MAX(comment_id) FROM comments")
        return result[0][0] + 1 if result[0][0] else 1

    def _get_comments_for_post(self, postid):
        """Get all the comments corresponding to a certain post."""
        query = "SELECT * FROM comments JOIN posts ON comment_post = post_id WHERE post_id = ?"
        data = self._execute(query, postid)
        comments = []
        for comment in data:
            user = self.get_user(comment[2]) if comment[2] else None
            date = datetime.strptime(comment[3].split(".")[0], "%Y-%m-%d %H:%M:%S")
            comments.append(Comment(comment[0], user, date, comment[4],
                                    comment[5], comment[6]))
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

    def get_user(self, userid):
        """Return the user with the given user ID."""
        query = "SELECT * FROM users WHERE user_id = ?"
        results = self._execute(query, userid)
        if not results:
            return None
        result = results[0]
        return User(*result)

    def register(self, username, display_name, password):
        """Returns one of "exists", "ok"."""
        q = "SELECT * FROM users WHERE user_name = ? OR user_display_name = ?"
        result = self._execute(q, username, display_name)
        if result:
            return "exists"
        user_id = self._get_next_userid()
        pwhash = hashlib.sha256(password).hexdigest()
        self._execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", user_id,
                      username, display_name, pwhash, user_id == 1)
        return "ok"

    def get_posts(self, user=None, page=1):
        """Return a list of posts meeting the given conditions."""
        if user:
            query = "SELECT * FROM posts WHERE post_user = ? ORDER BY post_date DESC"
            results = self._execute(query, user.userid)
        else:
            query = "SELECT * FROM posts ORDER BY post_date DESC"
            results = self._execute(query)

        posts = []
        pages = int(math.ceil(len(results) / float(PAGE_SIZE)))
        if page:
            results = results[PAGE_SIZE * (page - 1):PAGE_SIZE * page]
        for result in results:
            user = self.get_user(result[2])
            d = datetime.strptime(result[3].split(".")[0], "%Y-%m-%d %H:%M:%S")
            comments = self._get_comments_for_post(result[0])
            posts.append(Post(result[0], result[1], user, d, result[6],
                              result[4], result[5], comments))
        return posts, pages

    def get_post(self, postid):
        """Return an individual post."""
        query = "SELECT * FROM posts WHERE post_id = ?"
        results = self._execute(query, postid)
        if not results:
            return None
        result = results[0]
        user = self.get_user(result[2])
        date = datetime.strptime(result[3].split(".")[0], "%Y-%m-%d %H:%M:%S")
        comments = self._get_comments_for_post(result[0])
        return Post(result[0], result[1], user, date, result[6], result[4],
                    result[5], comments)

    def create_post(self, title, content, author):
        """Creates a post. Returns one of "ok"."""
        postid = self._get_next_postid()
        user_query = "SELECT user_id FROM users WHERE user_name = ?"
        user = self._execute(user_query, author)[0][0]
        date = datetime.now()
        content = content.replace("\r\n", "\n")
        summary = "\n\n".join(content.split("\n\n")[:2])
        slug = re.sub(r"[\W_]", "-", title.lower(), flags=re.UNICODE)[:50]
        slug = slug.rstrip("-")
        if not slug:
            return "bad title"
        self._execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?)", postid,
                      title, user, date, content, summary, slug)
        return "ok"

    def add_comment(self, postid, author, text, anon_name, anon_email):
        """Add a comment to a post."""
        cid = self._get_next_commentid()
        if author:
            user_query = "SELECT user_id FROM users WHERE user_name = ?"
            user = self._execute(user_query, author)[0][0]
        else:
            user = None
        text = text.replace("\r\n", "\n")
        date = datetime.now()
        self._execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?)", cid,
                      postid, user, date, text, anon_name, anon_email)
        return "ok"

    def validate_email(self, email):
        """Return whether an email address is valid."""
        # Ideally, this would send a confirmation email to the user.
        return re.match(r"[^@]+@[^@]+\.[^@]+$", email)

    def get_top_posters(self, posts):
        """Return a list of top posters as (User, count) tuples."""
        counts = {}
        for post in posts:
            if post.author.userid in counts:
                counts[post.author.userid][1] += 1
            else:
                counts[post.author.userid] = [post.author, 1]
        return sorted(counts.values(), key=lambda x: x[1], reverse=True)[:5]

    def is_admin(self, username):
        """Return whether the given user is an admin."""
        user_query = "SELECT user_id FROM users WHERE user_name = ?"
        userid = self._execute(user_query, username)[0][0]
        user = self.get_user(userid)
        return user.is_admin

    def get_users(self):
        """Return a list of all users in the database."""
        results = self._execute("SELECT * FROM users ORDER BY user_id ASC")
        users = []
        for result in results:
            users.append(User(*result))
        return users

    def delete_post(self, postid):
        """Delete a post in the database."""
        query = "SELECT 1 FROM posts WHERE post_id = ?"
        if not self._execute(query, postid):
            return "no post"
        query1 = "DELETE FROM posts WHERE post_id = ?"
        query2 = "DELETE FROM comments WHERE comment_post = ?"
        self._execute(query1, postid)
        self._execute(query2, postid)
        return "ok"

    def delete_user(self, userid):
        """Delete a user in the database."""
        query = "SELECT 1 FROM users WHERE user_id = ?"
        if not self._execute(query, userid):
            return "no user"
        query1 = "DELETE FROM users WHERE user_id = ?"
        query2 = "DELETE FROM posts WHERE post_user = ?"
        query3 = "DELETE FROM comments WHERE comment_user = ?"
        self._execute(query1, userid)
        self._execute(query2, userid)
        self._execute(query3, userid)
        return "ok"

    def promote_user(self, userid):
        """Promote a user to admin in the database."""
        query = "SELECT 1 FROM users WHERE user_id = ?"
        if not self._execute(query, userid):
            return "no user"
        query = "UPDATE users SET user_is_admin = 1 WHERE user_id = ?"
        self._execute(query, userid)
        return "ok"

    def demote_user(self, userid):
        """Demote a user from admin in the database."""
        query = "SELECT 1 FROM users WHERE user_id = ?"
        if not self._execute(query, userid):
            return "no user"
        query = "UPDATE users SET user_is_admin = 0 WHERE user_id = ?"
        self._execute(query, userid)
        return "ok"
