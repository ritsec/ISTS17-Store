"""
    Endpoints for our ecomm shop
"""
import ast
import requests
from flask import request, render_template, redirect, session, abort
from . import APP
from .config import API_URL


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

    data = request.form

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

    # move this to a function
    resp = requests.post("{}/{}".format(API_URL, "login"), data=post_data)
    print resp.json()

    if 'success' in resp.json():
        session['token'] = token
        return  redirect('/account')

    return render_template('login.html')

@APP.route('/shop', methods=['GET'])
def shop():
    """List of items able to be boughten from the white team store"""
    # move this to a function
    resp = requests.get("{}/{}".format(API_URL, "items"))
    items = resp.json()['items']
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

    # move this to a function
    resp = requests.post("{}/{}".format(API_URL, "buy"), data=post_data)
    print resp.json()
    # add return variable that says item was bought
    return redirect('/shop')


@APP.route('/account', methods=['GET'])
def expire_session():
    """Get the info for a teams account, the balance, transactions etc."""
    if 'token' not in session:
        return render_template('403.html')
    print session['token']
    return render_template('account.html')

@APP.route('/transfer', methods=['POST'])
def transfers():
    """Transfer money from one teams account to another"""
    pass