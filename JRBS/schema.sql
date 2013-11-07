-- Database schema
-- version 1

DROP TABLE IF EXISTS version;
CREATE TABLE version (
    version INTEGER
);
INSERT INTO version VALUES (%(version)s);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT,
    user_display_name TEXT,
    user_password_hash BLOB,
    user_is_admin INTEGER
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    post_id INTEGER PRIMARY KEY,
    post_title TEXT,
    post_user INTEGER,
    post_date DATETIME,
    post_text TEXT,
    post_summary TEXT,
    post_slug TEXT
);

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    comment_post INTEGER,
    comment_user INTEGER,
    comment_date DATETIME,
    comment_text TEXT,
    comment_anon_name TEXT DEFAULT NULL,
    comment_anon_email TEXT DEFAULT NULL
);
