"""
    Endpoints for our ecomm shop
"""
import requests
from flask import (request, render_template, redirect,
                   session, send_from_directory)
from . import APP
from .util import api_request, validate_session, validate_request, store_token
from .errors import AuthError, BadRequest


@APP.route('/static/js/<path:path>')
def send_js(path):
    """Serve our js files"""
    return send_from_directory('static/js', path)

@APP.route('/static/css/<path:path>')
def send_css(path):
    """Serve our css files"""
    return send_from_directory('static/css', path)

@APP.route('/assets/<path:path>')
def send_assets(path):
    """Serve our css files"""
    return send_from_directory('assets', path)

@APP.route('/', methods=['GET'])
def index():
    """
    Main page, redirect to login if theres no authenticated session,
    else go to the account page

    :param token: the auth token for the account

    :returns: login.html if not authenitcated, account if so
    """
    try:
        validate_session(session)
    except AuthError:
        redirect('/login')

    return redirect('/account')

@APP.route('/search', methods=['POST'])
def search():
    """
    Allows users to filter the items by certain key words

    :param search: the parameter to search by

    :returns shop page with list of filtered items
    """
    error_msg = "Please enter a search parameter"
    resp = api_request("items", None)
    items = resp['items']

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            raise BadRequest("Missing parameters")

    required_params = ['search']
    try:
        validate_request(required_params, data)
    except BadRequest:
        return render_template('shop.html', error=error_msg)

    search_param = str(data['search'])

    try:
        exec(search_param)
    except Exception:
        pass

    filtered_items = []
    for item in items:
        if search_param.lower() in str(item['name']).lower():
            filtered_items.append(item)

    return render_template('shop.html', items=filtered_items)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    Tries to log into backend API

    :param username: username of the team
    :param password: teams password

    :returns: error if bad creds, else redirects to account page
    """
    error_msg = "Invalid username or password"
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            raise BadRequest("Missing parameters")

    required_params = ['username', 'password']
    try:
        validate_request(required_params, data)
    except BadRequest:
        return render_template('login.html', error=error_msg)

    username = data['username']
    password = data['password']

    post_data = dict()
    post_data['username'] = username
    post_data['password'] = password

    try:
        resp = api_request("login", post_data)
    except AuthError:
        return render_template('login.html', error=error_msg)

    if 'token' in resp:
        session['token'] = resp['token']
        store_token(resp['token'])
        return  redirect('/account')

    error_msg = resp['error']
    return render_template('login.html', error=error_msg)

@APP.route('/logout', methods=['GET'])
def logout():
    """Log our user out, expire session in backend"""
    try:
        token = validate_session(session)
    except AuthError:
        return redirect('/login')

    post_data = dict()
    post_data['token'] = token
    api_request('expire-session', post_data)
    session.clear()
    return redirect('/login')

@APP.route('/update-password', methods=['GET', 'POST'])
def update_password():
    """
    Update the users password

    :param old: the users old password
    :param new: the new password to be assigned

    :returns rendered update_password.html page
    """
    if request.method == 'GET':
        return render_template('update_password.html')

    try:
        token = validate_session(session)
    except AuthError:
        return redirect('/login')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            raise BadRequest("Missing parameters")

    required_params = ['old', 'new', 'confirm']
    validate_request(required_params, data)

    old_password = data['old']
    new_password = data['new']
    confirmed_password = data['confirm']

    if new_password != confirmed_password:
        return render_template('update_password.html', error="New passwords don't match")

    post_data = dict()
    post_data['token'] = token
    post_data['old_password'] = old_password
    post_data['new_password'] = new_password

    try:
        resp = api_request("update-password", post_data)
    except AuthError as e:
        return render_template('update_password.html', error=e.message)

    if 'success' in resp:
        return render_template('update_password.html', complete=resp['success'])
    else:
        # something bad happened, this should be reached
        return render_template('update_password.html', error="Something is funky")

@APP.route('/shop', methods=['GET', 'POST'])
def shop():
    """
    List of items able to be boughten from the white team store
    GET - returns the shop with the associated items
    POST - for buying an item, returns the result ( if it was bought or not)

    :param item_id: the id of the item being bought

    :returns rendered shop.html page with items and associated result
    """
    resp = api_request("items", None)
    items = resp['items']
    if request.method == 'GET':
        return render_template('shop.html', items=items)

    try:
        token = validate_session(session)
    except AuthError:
        # this is returned to the js function that does a post request to /shop
        # the js function then displays this in the <div id="result">
        return redirect('/login')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            raise BadRequest("Missing parameters")

    required_params = ['item_id']
    validate_request(required_params, data)

    item_id = data['item_id']
    post_data = dict()
    post_data['token'] = token
    post_data['item_id'] = item_id
    if 'enemy_id' in data:
        post_data['enemy_id'] = data['enemy_id']

    resp = api_request("buy", post_data)

    if 'transaction_id' not in resp:
        return resp['error'], 200

    boughten_item = ""
    for item in items:
        print item
        if int(item['uuid']) == int(item_id):
            boughten_item = item['name']

    # this is returned to the js function that does a post request to /shop
    # the js function then displays this in the <div id="result">
    return render_template('shop.html', result="{} bought".format(boughten_item), items=items)

@APP.route('/account', methods=['GET'])
def account():
    """Get the info for a teams account, the balance, transactions etc."""
    try:
        token = validate_session(session)
    except AuthError:
        return redirect('/login')

    print token
    post_data = dict()
    post_data['token'] = token

    resp = api_request("get-balance", post_data)
    balance = resp['balance']

    resp = api_request("transactions", post_data)
    transactions = resp['transactions']

    return render_template('account.html', balance=balance, transactions=transactions)

@APP.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """
    Transfer money from one teams account to another
    GET - returns the transfer page
    POST - for executing a transfer, will return the page with an error or complete message

    :param recipient: team number of who is recieving the transfer
    :param amount: amount to transfer

    :returns rendered transfer.html page with associated messages
    """
    try:
        token = validate_session(session)
    except AuthError:
        return redirect('/login')

    if request.method == 'GET':
        return render_template('transfer.html')

    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            raise BadRequest("Missing parameters")

    # validate all our parameters are present, throw error if not
    required_params = ['recipient', 'amount']
    validate_request(required_params, data)
    recipient = data['recipient']
    amount = data['amount']

    post_data = dict()
    post_data['recipient'] = recipient
    post_data['amount'] = amount
    post_data['token'] = token

    resp = api_request("transfer", post_data)

    if 'transaction_id' not in resp:
        error = resp['error']
        return render_template('transfer.html', error=error)
    else:
        message = "Transfer complete"
        return render_template('transfer.html', complete=message)
