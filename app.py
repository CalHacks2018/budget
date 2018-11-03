import flask 
from flask import Flask, request, render_template 
import requests
import firebase_admin
from firebase_admin import db

app = flask.Flask(__name__)

firebase_admin.initialize_app(options={
    'databaseURL': 'https://budget-data-d6bdc.firebaseio.com'
})
USERS = db.reference('superheroes')

@app.route('/login', methods =['POST'])
def create_hero():
    # print('[INFO]: ', request.form)
    print('[INFO]: ', request.form['name'])
    print('[INFO]: ', request.form['budget'])
    # print('[INFO]: ', request.form.to_dict())
    req = request.form.to_dict() # flask.request.json
    hero = USERS.push(req)
    return flask.jsonify({'id': hero.key}), 201 

@app.route('/heroes', methods=['POST'])
# def create_hero():
#     # print('[INFO]: ', request.form)
#     print('[INFO]: ', request.form['amount'])
#     print('[INFO]: ', request.form['type'])
#     print('[INFO]: ', request.form.to_dict())
#     req = request.form.to_dict() # flask.request.json
#     hero = USERS.push(req)
#     return flask.jsonify({'id': hero.key}), 201

@app.route('/heroes/<id>')
def read_hero(id):
    return flask.jsonify(_ensure_hero(id))

@app.route('/heroes/<id>', methods=['PUT'])
def update_hero(id):
    _ensure_hero(id)
    req = flask.request.json


    USERS.child(id).update(req)
    return flask.jsonify({'success': True})

@app.route('/heroes/<id>', methods=['DELETE'])
def delete_hero(id):
    _ensure_hero(id)
    USERS.child(id).delete()
    return flask.jsonify({'success': True})

def _ensure_hero(id):
    hero = USERS.child(id).get()
    if not hero:
        flask.abort(404)
    return hero

@app.route('/')
def main():
    return flask.render_template("login.html")

if __name__=='__main__':
    app.debug=True
    app.run()