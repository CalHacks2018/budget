import flask 
from flask import Flask, request, render_template, jsonify
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
	"name": "PAYMENT.SALE.CREATED"
	},{
	"name": "PAYMENT.SALE.DENIED"
 	},{
 	"name": "PAYMENT.AUTHORIZATION.CREATED"
 	},{
 	"name": "PAYMENT.AUTHORIZATION.VOIDED"
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
	else:
		abort(400)


@app.route('/')
def main():
	return flask.render_template("index.html")

if __name__=='__main__':
	app.debug=True
	app.run()

