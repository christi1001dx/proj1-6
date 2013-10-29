from flask import Flask
from flask import request, render_template

class post():
    author = "";
    title = "";
    preview = ""
    link = "";
    def __init__(self):
        pass
app = Flask(__name__)

@app.route('/')
def home():
    h1 = post()
    h1.author = "aaron"
    h1.title = "First"
    h1.link = "first.html"
    h1.preview = "Here we can see that Aaron came first, by his alphabetical name blah blah vlaa as aerg a g"
    h2 = post()
    h2.author = "jim"
    h2.title = "Second"
    h2.link = "second.html"
    return render_template("index.html", featured=h1)
@app.route("/a")
def a():
    print("AGA")
    return render_template("index.html")
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
