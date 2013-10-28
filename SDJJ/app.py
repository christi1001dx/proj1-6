from flask import Flask
import config

app = Flask(__name__)

@app.route("/")
def home():
	return "<h1>Hello world.</h1>"

if __name__ == "__main__":
	app.run(debug = True)
