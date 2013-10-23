#!/usr/bin/python

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
	#app.jinja_env.line_statement_prefix = '='
	app.debug = True
	app.run(host='0.0.0.0')