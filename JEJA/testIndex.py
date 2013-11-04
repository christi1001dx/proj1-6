from flask import Flask, render_template
#from index import formatPost
from index import *

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():

    comments = [
        {
            "username":"Jeffrey",
            "content":"Test comment"
            },{
            "username":"Jared",
            "content":"Another test comment"
            }
        ]

    post = {
                "title":"Test Title",
                "author":"Andrew",
                "content":"This is a test post, I wonder how it works",
                "comments":formatComments(comments),
                "authorHTML":""
                }

    print(post["comments"])

    r = formatPost(post)

    return render_template("index.html",data=r)


if __name__ == "__main__":
    app.run()
