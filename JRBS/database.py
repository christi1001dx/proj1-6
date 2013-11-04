# JRBS - Interface with the SQLite database

import hashlib
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
        self.postid
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
            return conn.execute(query, *args).fetchall()

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
        pass

    def get_posts(self, user=None, page=1):
        pass

    def get_post(self, postid):
        pass
