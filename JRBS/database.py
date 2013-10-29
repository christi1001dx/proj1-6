# JRBS - Interface with the SQLite database

import sqlite3

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
            return conn.execute(query, *args).fetchall()
