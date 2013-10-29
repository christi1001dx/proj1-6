# Flask engine for bloginator

from flask import Flask
import config

app = Flask(__name__)

@app.route("/")
def home():
	posts = utils.getPosts()
	return render_template("home.html")

# profile by username
@app.route("/profiles/<username>")
def profile(username):
	user = utils.getUser(username)
	return render_template("profile.html", user = user)

# post by number
@app.route("/posts/<post>")
def post(post):
	post = utils.getPost(post)
	return render_template("post.html", post = post)

if __name__ == "__main__":
	app.run(debug = True)
