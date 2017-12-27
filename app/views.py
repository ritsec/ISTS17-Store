"""
    Endpoints for our ecomm shop
"""
import requests
from flask import request, render_template, redirect, session
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
    return render_template('shop.html')

@APP.route('/buy', methods=['POST'])
def buy():
    """Buys a item from the white team store"""
    pass

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