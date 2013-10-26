from flask import Flask
from flask import request
from flask import render_template

from pymongo import MongoClient

import utils

db = MongoClient().db

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("template.blogposts.html",posts=utils.getPosts('jasper',db.posts))

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)

