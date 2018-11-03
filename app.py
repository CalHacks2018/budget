import flask 
from flask import Flask, request, render_template 
import requests

app = Flask(__name__)

@app.route('/')
def main():
	return flask.render_template("index.html")

if __name__=='__main__':
	app.debug=True
	app.run()

