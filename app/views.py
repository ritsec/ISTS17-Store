"""
    Endpoints for our ecomm shop
"""
from flask import (request, render_template, redirect,
                   session, abort, flash, send_from_directory)
from . import APP
from .config import TEAM_ID
from .util import api_request
from .errors import AuthError


@APP.route('/js/<path:path>')
def send_js(path):
    """
    Serve our js files
    """
    return send_from_directory('js', path)

@APP.route('/', methods=['GET'])
def index():
    """
    Main page, redirect to login if theres no authenticated session,
    else go to the account page

    :param token: the auth token for the account
    :returns: login.html if not authenitcated, account if so
    """
    if 'token' not in session:
        return redirect('/login')

    token = session['token']
    post_data = dict()
    post_data['token'] = token
    post_data['team_id'] = TEAM_ID

    resp = api_request("validate-session", post_data)

    if 'success' in resp:
        return  redirect('/account')

    return redirect('/login')

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    Tries to log into backend API

    :param username: username of the team
    :param password: teams password

    :returns: error if bad creds, else redirects to account page
    """
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    if 'username' not in data or 'password' not in data:
        # error
        pass

    username = data['username']
    password = data['password']

    # generate token here
    token = 'heythere'

    post_data = dict()
    post_data['username'] = username
    post_data['password'] = password
    post_data['token'] = token

    resp = api_request("login", post_data)

    if 'success' in resp:
        session['token'] = token
        return  redirect('/account')

    # return error here
    return render_template('login.html')

@APP.route('/shop', methods=['GET'])
def shop():
    """List of items able to be boughten from the white team store"""
    resp = api_request("items", None)
    items = resp['items']
    return render_template('shop.html', items=items)

@APP.route('/buy', methods=['POST'])
def buy():
    """Buys a item from the white team store"""
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # add error checking
    item_id = data['item_id']
    token = session['token']
    post_data = dict()
    post_data['token'] = token
    post_data['item_id'] = item_id

    resp = api_request("buy", post_data)

    if 'transaction_id' not in resp:
        return resp['error'], 200
    else:
        return 'Item bought', 200


@APP.route('/account', methods=['GET'])
def expire_session():
    """Get the info for a teams account, the balance, transactions etc."""
    if 'token' not in session:
        raise AuthError("No session token")

    print session['token']
    post_data = dict()
    post_data['token'] = session['token']

    # get balance
    resp = api_request("get-balance", post_data)
    balance = resp['balance']

    # get transactions
    resp = api_request("transactions", post_data)
    transactions = resp['transactions']
    return render_template('account.html', balance=balance, transactions=transactions)

@APP.route('/transfer', methods=['GET', 'POST'])
def transfers():
    """Transfer money from one teams account to another"""
    if 'token' not in session:
        return render_template('403.html')

    if request.method == 'GET':
        return render_template('transfer.html')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    recipient = data['recipient']
    amount = data['amount']
    token = session['token']

    post_data = dict()
    post_data['recipient'] = recipient
    post_data['amount'] = amount
    post_data['token'] = token

    resp = api_request("transfer", post_data)

    if 'transaction_id' not in resp:
        error = resp['error']
        flash(error)
    else:
        flash('Transaction completed')

    return render_template('transfer.html')
