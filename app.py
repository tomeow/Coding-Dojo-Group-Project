import os
from flask import Flask, render_template, request, session, redirect
from mysqlconnection import MySQLConnector

import stripe


stripe_keys = {
    'secret_key': os.environ.get('SECRET_KEY', ""),
    'publishable_key': os.environ.get('PUBLISHABLE_KEY', "")
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.secret_key = "DonationsAreGreatlyAppreciated8282"
mysql = MySQLConnector('mydb')

@app.route('/', methods=['GET'])
def index():
    total = mysql.fetch("SELECT TRUNCATE(SUM(amount)/100, 2) AS sofar FROM donations")
    recent = mysql.fetch("SELECT name FROM donations ORDER BY donations.id DESC LIMIT 3")
    return render_template('index.html', key=stripe_keys['publishable_key'], total=total, recent=recent)

# This is just to see 'charge.html'. Do Not use in presentation
# @app.route('/charge', methods=['POST'])
# def charge():
#     return render_template('charge.html')

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = request.form['amount']+'00'
    session['amount'] = request.form['amount']
    session['name'] = request.form['name']

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    query = "INSERT INTO donations (amount, name) VALUES ('{}', '{}')".format(amount, session['name'])
    mysql.run_mysql_query(query)
    return redirect('/')
    # return redirect('/chage')


if __name__ == '__main__':
    app.run(debug=True)



# import os
# from flask import Flask, render_template, request, session, redirect
# from mysqlconnection import MySQLConnector
# # import stripe



# stripe_keys = {
#     'secret_key': os.environ.get['SECRET_KEY'],
#     'publishable_key': os.environ.get['PUBLISHABLE_KEY']
# }

# stripe.api_key = stripe_keys['secret_key']

# app = Flask(__name__)
# app.secret_key = "DonationsAreGreatlyAppreciated8282"
# mysql = MySQLConnector('mydb')

# @app.route('/', methods=['GET'])
# def index():
#     total = mysql.fetch("SELECT TRUNCATE(SUM(amount)/100, 2) AS sofar FROM donations")
#     recent = mysql.fetch("SELECT name FROM donations ORDER BY donations.id DESC LIMIT 3")
#     return render_template('index.html', key=stripe_keys['publishable_key'], total=total, recent=recent)

# @app.route('/charge', methods=['POST'])
# def charge():
#     # Amount in cents
#     amount = request.form['amount']+'00'
#     session['amount'] = request.form['amount']
#     session['name'] = request.form['name']

#     customer = stripe.Customer.create(
#         email='customer@example.com',
#         card=request.form['stripeToken']
#     )

#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount,
#         currency='usd',
#         description='Flask Charge'
#     )

#     query = "INSERT INTO donations (amount, name) VALUES ('{}', '{}')".format(amount, session['name'])
#     mysql.run_mysql_query(query)
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True)



