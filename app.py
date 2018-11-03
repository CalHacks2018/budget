import flask 
from flask import Flask, url_for, request, render_template, jsonify
import requests
import paypalrestsdk 
from paypalrestsdk import Webhook

paypalrestsdk.configure({
	'mode': 'sandbox', #sandbox or live
  	'client_id': 'ATbI73Ar9lZ6oeQEcjh-KPV9Zbe1q_x8k3A_CoV7liqZgI2lknrW5ZawTZnDhDRwc5L1eQNi0d8NHnCg',
  	'client_secret': 'EM764Y5eYv8WM1dVs-z8lgqN2AQcmq_13BjuHVWhHr80bHxSLtVqBx7h9WWCHE8tIFa0_89DwG9kfWZ5' 
})

webhook = Webhook({
	"url": "https://budget-track.herokuapp.com/",
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

@app.route('/webhook', methods=['POST'])
def webhook():
	if request.method == 'POST':
		req = request.get_json(silent=True, force=True)
		print("Request:")
		print(req)
		print(req['id'])
		sale_id = req['id']
		print(req['create_time'])
		time = req['create_time']
		print(req['resource']['amount']['total'])
		amout = req['resource']['amount']['total']
		print(req['resource']['parent_payment'])
		payment_id = req['resource']['parent_payment']
		print(req['resource']['links'][2]['href'])
		payment_url = req['resource']['links'][2]['href']

		r = requests.get(payment_url)
		print(r.json())
	else:
		abort(400)

	# template_data = {
	# 	'result' : req
	# }
	return flask.render_template("budget.html")

@app.route('/', methods=['POST'])
def form_input():
	if request.method == 'POST':
		name = request.form['name']
		budget = request.form['budget']
		template_data = {
			'name': name,
			'budget': budget
		}
		return flask.render_template("budget.html", **template_data)

@app.route('/')
def main():
	return flask.render_template("index.html")

if __name__=='__main__':
	app.debug=True
	app.run()

