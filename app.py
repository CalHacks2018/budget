import flask 
from flask import Flask, url_for, request, render_template, jsonify
import requests
import paypalrestsdk 
from paypalrestsdk import Webhook
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, jsonify, abort, url_for, make_response
import requests
# import firebase_admin
from firebase_admin import db, initialize_app


paypalrestsdk.configure({
	'mode': 'sandbox', #sandbox or live
  	'client_id': 'Aa0VFBzKjKzgdI-kZwHEkLv5aOmy9yBJ8tqHSH2ElzKWXFtZ-btg9ADqaw4nFwgPQAEHa88pNe4FeUtI',
  	'client_secret': 'EI-dMlYlcd7Zykf4vJRpizh-a2EnpfVxdFBl4EbzzHYxa9qP8LkwKwOoReBofFWvpSn6w02sBCLFPhPY' 
})

webhook = Webhook({
	"url": "https://budget-track.herokuapp.com/webhhook",
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

app = Flask(__name__)

initialize_app(options={
    'databaseURL': 'https://budget-data-d6bdc.firebaseio.com'
})
USERS = db.reference('budget-node')

@app.route('/index', methods =['POST'])
def create_user():
    req = request.form.to_dict() 
    new_user = USERS.push(req)
    user_id = new_user.key
    print('[INFO] User ID: ', user_id)
    user_details = _ensure_user(user_id)
    print('[INFO] User Info: ', user_details) # read_user(user_id).json)
    return render_template("index.html", user=user_details) 

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

@app.route('/webhook', methods=['POST'])
def webhook():
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
			'category': 'random'
		}

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



@app.route('/')
def main():
    return render_template("user.html")

if __name__=='__main__':
    app.debug=True
    app.run()