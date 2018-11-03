from flask import Flask, request, render_template, redirect, jsonify, \
abort, url_for, make_response
import requests
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
    req['transactions'] = []
    new_user = USERS.push(req)
    user_id = new_user.key
    print('[INFO] User ID: ', user_id)
    user_details = _ensure_user(user_id)
    user_details['user_id'] = user_id
    print('[INFO] User Info: ', user_details) # read_user(user_id).json)
    return render_template("budget.html", user=user_details) #, 201 
    # redirect(url_for('read_user'))

@app.route('/users/<id>')
def read_user(id):
    return jsonify(_ensure_user(id))

@app.route('/users/<id>', methods=['PUT', 'POST'])
def update_user(id):
	_ensure_user(id)
	req = request.form.to_dict() 
	print('[INFO] Payload: ', req)
	ref = USERS.child(id).child('transactions')
	ref.push(req)
	# ref.update({"transactions": req})
	#  print('[INFO] Payload: ', USERS.child(id).child('transactions').push(req))
	# USERS.child(id).update(req)
	user_details = _ensure_user(id)
	user_details['user_id'] = id
	print('[INFO] User Info: ', user_details) 
	return render_template("budget.html", user=user_details) # jsonify({'success': True})

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
    return render_template("new_user.html")

if __name__=='__main__':
    app.debug=True
    app.run()