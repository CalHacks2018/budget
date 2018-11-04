import json
import urllib.request
import datetime

# Databases / Accessing Data 

with urllib.request.urlopen("https://budget-data-d6bdc.firebaseio.com/budget-node/-LQSVMNBHr7yDM7RK0e3.json") as jsonout:
    user_data = json.loads(jsonout.read())

# Response Messages

welcome = "Welcome to Nudist Buddhist!"
help_response = "Try asking Nudist Buddhist what your most recent transaction was \
                or how much of your budget you have been through."
name_response = "Your name is {}"
budget_response = "{}, your budget is currently {} dollars per week."
MET_response = "{}, your most expensive transaction was {} dollars and {} cents, on {} {}."
MRT_response = "{}, your most recent transaction was on {} {}."
all_transactions_response = "Your total sum of all your transactions is {} dollars and {} cents."
remaining = "Your remaining budget is {} dollars and {} cents."
transaction_count = "You have logged {} transactions."
frequent = "Your transactions have been related to {} the most frequently."

summary = "Hello {}, your budget is {} dollars per week and you have made {} transactions totalling {} dollars and {} cents."


# Basic voice response
def response(message, session_end=True):
    return {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': message
                    },
                    'shouldEndSession': session_end
                }
            }

# Helper methods
def total_to_dc(value):
    dollars = str(round(value // 1))
    cents = str(round((value % 1) * 100))
    return dollars, cents

def occurances():
    transactions = user_data['transactions']
    counts = {}
    for i in transactions:
        index = transactions.get(i)['category']
        if counts.get(index):
            counts.update({index: counts.get(index) + 1})
        else:
            counts.update({index: 1})
    
    max_occurance = 0
    key = ''

    for i in counts.keys():
        if counts.get(i) > max_occurance:
            max_occurance = counts.get(i)
            key = i

    return key


# Getter methods
def get_name():
    name = user_data['name']
    return name

def get_budget():
    budget = int(user_data['budget'])
    return budget

def get_MRT():
    transactions = user_data['transactions']
    keys = list(transactions.keys())
    last_transaction = transactions.get(keys[len(keys) - 1])

    try:
        date = last_transaction['transaction-date']
    except Exception:
        date = datetime.datetime.today().strftime("%Y-%m-%d")

    date = date[0:10]
    day = int(date[8:10])
    month = datetime.date(1900, int(date[5:7]), 1).strftime("%B")

    return month, day
    

def get_MET():
    transactions = user_data['transactions']
    keys = transactions.keys()
    largest_transaction = transactions.get(list(transactions.keys())[0])

    for i in keys:
        if float(transactions.get(i)['amount']) > float(largest_transaction['amount']):
            largest_transaction = transactions.get(i)

    try:
        date = largest_transaction['transaction-date']
    except Exception:
        date = datetime.datetime.today().strftime("%Y-%m-%d")

    date = date[0:10]
    day = int(date[8:10])
    month = datetime.date(1900, int(date[5:7]), 1).strftime("%B")

    lt_dollars, lt_cents = total_to_dc(float(largest_transaction['amount']))

    return lt_dollars, lt_cents, month, day

def get_sum():
    transactions = user_data['transactions']
    keys = transactions.keys()
    total = 0.0
    
    for i in keys:
        total += float(transactions.get(i)['amount'])

    sum_dollars, sum_cents = total_to_dc(total)

    return sum_dollars, sum_cents

def get_remaining():
    gotten_sum = get_sum()
    total_sum = float(gotten_sum[0]) + float(gotten_sum[1]) / 100
    remaining = get_budget() - total_sum
    rem_dollars, rem_cents = total_to_dc(remaining)
    return rem_dollars, rem_cents

def num_transactions():
    transactions = user_data['transactions']
    keys = list(transactions.keys())
    return len(keys)

# Intent handler
def intent_handler(event):
    intent = event['request']['intent']['name']
    
    if intent == 'Name':
        return response(name_response.format(get_name()))
    elif intent == 'Budget':
        return response(budget_response.format(get_name(), get_budget()))
    elif intent == 'MostRecentTransaction':
        dollars, cents = get_MRT()
        return response(MRT_response.format(get_name(), dollars, cents))
    elif intent == 'MostExpensiveTransaction':
        dollars, cents, month, day = get_MET()
        return response(MET_response.format(get_name(), dollars, cents, month, day))
    elif intent == 'TotalTransactions':
        dollars, cents = get_sum()
        return response(all_transactions_response.format(dollars, cents))
    elif intent == 'MoneyRemaining':
        dollars, cents = get_remaining()
        return response(remaining.format(dollars, cents))
    elif intent == 'NumTransactions':
        return response(transaction_count.format(num_transactions()))
    elif intent == 'Frequency':
        return response(frequent.format(occurances()))
    elif intent == 'Summary':
        dollars, cents = get_sum()
        return response(summary.format(get_name(), get_budget(), num_transactions(), dollars, cents))
    elif intent == 'AMAZON.HelpIntent':
        return response(help_response)
    elif intent == 'AMAZON.StopIntent' or intent == 'AMAZON.CancelIntent':
        return response("Goodbye.")
    else:
        return response("I don't know that one. Try asking Health Tips for help.")


# Default handler
def lambda_handler(event, context):
    event_kind = event['request']['type']
    
    if event_kind == 'LaunchRequest':
        return response(welcome, False)
    elif event_kind == 'IntentRequest':
        return intent_handler(event)
    elif event_kind == 'SessionEndedRequest':
        return response("Goodbye.")
    else:
        return response("Uh oh! I didn't get that.")