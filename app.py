import flask 
from flask import Flask, url_for, request, render_template, jsonify
import requests
import paypalrestsdk 
from paypalrestsdk import Webhook
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, jsonify, abort, url_for, make_response
import requests
from firebase_admin import db, initialize_app
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "budget-data-d6bdc-firebase-adminsdk-bu5t8-383b28eb2d.json"
paypalrestsdk.configure({
	'mode': 'sandbox', #sandbox or live
  	'client_id': 'Aa0VFBzKjKzgdI-kZwHEkLv5aOmy9yBJ8tqHSH2ElzKWXFtZ-btg9ADqaw4nFwgPQAEHa88pNe4FeUtI',
  	'client_secret': 'EI-dMlYlcd7Zykf4vJRpizh-a2EnpfVxdFBl4EbzzHYxa9qP8LkwKwOoReBofFWvpSn6w02sBCLFPhPY' 
})

webhook = Webhook({
	"url": "https://budget-track.herokuapp.com/webhook",
	"event_types": [{
	"name": "PAYMENT.SALE.COMPLETED"
	},{
	"name": "PAYMENT.SALE.DENIED"
 	},{
 	"name": "PAYMENT.SALE.REFUNDED"
 	},{
 	"name": "PAYMENT.SALE.REVERSED"
 	},{
 	"name": "PAYMENT.SALE.PENDING"
 	},{
 	"name": "PAYMENT.AUTHORIZATION.CREATED"
 	},{
 	"name": "PAYMENT.AUTHORIZATION.VOIDED"
 	},{
 	"name": "PAYMENT.ORDER.CANCELLED"
 	},{
 	"name": "PAYMENT.ORDER.CREATED"
 	}]
 })

if webhook.create():
	print("Webhook[%s] created successfully" % (webhook.id))
else:
	print(webhook.error)

ogBudget = 0
totalSpent = 0

app = Flask(__name__)

initialize_app(options={
    'databaseURL': 'https://budget-data-d6bdc.firebaseio.com'
})
USERS = db.reference('budget-node')

@app.route('/index', methods =['POST'])
def create_user():
    req = request.form.to_dict() 
    req['transactions'] = []
    new_user = USERS.push(req)
    user_id = new_user.key
    print('[INFO] User ID: ', user_id)
    user_details = _ensure_user(user_id)
    user_details['user_id'] = user_id
    print('[INFO] User Info: ', user_details) # read_user(user_id).json)
    global ogBudget
    ogBudget = req['budget']
    return render_template("budget.html", user=user_details, ogBudget=ogBudget, spent=totalSpent) #, 201 

@app.route('/users/<id>')
def read_user(id):
	# return jsonify(_ensure_user(id))
	user_details = _ensure_user(id)
	user_details['user_id'] = id
	print('[INFO] User Info: ', user_details) 
	return render_template("budget.html", user=user_details, ogBudget=ogBudget, spent=totalSpent) 

@app.route('/users/<id>', methods=['PUT', 'POST'])
def update_user(id):
	_ensure_user(id)
	update_payload = request.form.to_dict() 
	print('[INFO] Payload from web form: ', update_payload)

	master_ref = USERS.child(id)

	transactions_ref = USERS.child(id).child('transactions')
	transactions_ref.push(update_payload)
	# master_ref.push({'transactions': update_payload})
	# print('[INFO] Total Amount? ', USERS.child(id).child('budget').get())
	curr_budget = float(USERS.child(id).child('budget').get())
	curr_budget -= float(update_payload['amount'])
	global totalSpent 
	totalSpent+=float(update_payload['amount'])
	print("PRINTING TOTAL SPENT!!!!!!!!!!!!!!!!!!!!! {}".format(totalSpent))
	budget_ref = USERS.child(id).child('budget')
	# master_ref.update({'budget': curr_budget})
	budget_ref.set(curr_budget)
	#  print('[INFO] Payload: ', USERS.child(id).child('transactions').push(req))
	# USERS.child(id).update(req)
	# ref.update({"transactions": req})
	return redirect(url_for('read_user', id = id)) 
	# render_template("budget.html", user=user_details) 
	# jsonify({'success': True})

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

# @app.route('/users', methods=['POST'])
# def create_user():

@app.route('/users/webhook/<id>', methods=['POST'])
def webhook(id):
	if request.method == 'POST':
		req = request.get_json(silent=True, force=True)
		sale_id = req['id']
		time = req['create_time']
		amount = req['resource']['amount']['total']
		payment_id = req['resource']['parent_payment']
		payment_url = req['resource']['links'][2]['href']

		transaction = {
			'date': time,
			'amount': amount,
			'category': "Utilities"
		}

		print('[INFO] Transaction: ', transaction)
		ref = USERS.child(id).child('transactions')
		ref.push(transaction)
		# ref.update({"transactions": req})
		#  print('[INFO] Payload: ', USERS.child(id).child('transactions').push(req))
		# USERS.child(id).update(req)
		user_details = _ensure_user(id)
		user_details['user_id'] = id
		print('[INFO] User Info: ', user_details) 	
		# db[id][transaction].append(transaction)
		# db[id][spent]+=transation[amount]
		# N = 1
		# global speant 
		# speant -= float(amount)
		# global budget
		# remaining = budget - speant

		# ind = np.arange(N)    # the x locations for the groups
		# width = 0.15       # the width of the bars: can also be len(x) sequence

		# p1 = plt.bar(ind, remaining, width, color='#d62728')
		# p2 = plt.bar(ind, speant, width,
		#              bottom=remaining)

		# plt.ylabel('Amount')
		# plt.title('Rremaining in budget')
		# plt.xticks(ind, ('Budget'))
		# plt.yticks(np.arange(0, 101, 10))
		# plt.legend((p1[0], p2[0]), ('Remaining', 'Speant'))

		# fig = plt.gcf()
		# plt.show()
		# fig.savefig('img.png')
	else:
		abort(400)
	return render_template("budget.html", user=user_details, ogBudget=ogBudget, spent=totalSpent)


@app.route('/')
def main():
    return render_template("new_user.html")

if __name__=='__main__':
    app.debug=True
    app.run()