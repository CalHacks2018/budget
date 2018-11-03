from flask import Flask, request, render_template, redirect, jsonify, \
abort, url_for, make_response
import requests
# import firebase_admin
from firebase_admin import db, initialize_app

app = Flask(__name__)

initialize_app(options={
    'databaseURL': 'https://budget-data-d6bdc.firebaseio.com'
})
USERS = db.reference('budget-node')

@app.route('/index', methods =['POST'])
def create_user():
    # print('[INFO]: ', request.form['name'])
    # print('[INFO]: ', request.form['budget'])
    # print('[INFO]: ', request.form.to_dict())
    req = request.form.to_dict() 
    new_user = USERS.push(req)
    user_id = new_user.key
    print('[INFO] User ID: ', user_id)
    user_details = _ensure_user(user_id)
    print('[INFO] User Info: ', user_details) # read_user(user_id).json)
    return render_template("index.html", user=user_details) 
    # redirect(url_for('read_user'))
    # flask.jsonify({'id': hero.key}), 201 

@app.route('/users/<id>')
def read_user(id):
    return jsonify(_ensure_user(id))

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    _ensure_user(id)
    req = request.json
    USERS.child(id).update(req)
    return jsonify({'success': True})

def _ensure_user(id):
    user = USERS.child(id).get()
    if not user:
        abort(404)
    return user

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    _ensure_user(id)
    USERS.child(id).delete()
    return jsonify({'success': True})


@app.route('/users', methods=['POST'])
# def create_user():

@app.route('/')
def main():
    return render_template("user.html")

if __name__=='__main__':
    app.debug=True
    app.run()