# Flask engine for bloginator

from flask import Flask
import config

app = Flask(__name__)

@app.route("/")
def home():
	posts = utils.posts()
	return render_template("home.html")

@app.route("/profiles")
def profile():
	return render_template("profiles.html", profiles = utils.profiles()

# profile by username
@app.route("/profiles/<username>")
def profile(username):
	profile = utils.profile(username)
	return render_template("profile.html", profile = profile)

# post by number
@app.route("/posts/<post>")
def post(post):
	post = utils.post(post)
	return render_template("post.html", post = post)

@app.route("/login", methods = ["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"] 
	if utils.authenticate(username, password):
		utils.login(username)
		return "Success"
	return "Error."
	
if __name__ == "__main__":
	app.run(debug = True)
