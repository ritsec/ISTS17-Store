"""
    Endpoints for our ecomm shop
"""
from flask import request
from . import APP


@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    Tries to log into backend API

    :param username: username of the team
    :param password: teams password
    :param token: the auth token to be attached to this account

    :returns result: json dict containing either a success or and error
    """
    pass

@APP.route('/shop', methods=['GET'])
def shop():
    """List of items able to be boughten from the white team store"""
    pass

@APP.route('/buy', methods=['POST'])
def buy():
    """Buys a item from the white team store"""
    pass

@APP.route('/account', methods=['GET'])
def expire_session():
    """Get the info for a teams account, the balance, transactions etc."""
    pass

@APP.route('/transfer', methods=['POST'])
def transfers():
    """Transfer money from one teams account to another"""
    pass