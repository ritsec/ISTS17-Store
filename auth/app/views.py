"""
    Entry point for API calls
"""
import json
import random
import string
from flask import request, jsonify, abort, make_response
from . import APP, DB, logger
from .models.session import Session
from .models.teams import Team
from . import errors
from .util import new_session, validate_request

@APP.route('/validate-key', methods=['POST'])
def validate_key():
    """
    Validates if the session is valid and returns the team_id

    :param key: the private key for the user

    :returns: json dict containing the token and team_id
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['key']
    validate_request(params, data)
    key = data['key']
    user = Team.query.filter_by(private_key=key).first()

    if user is None:
        raise errors.AuthError('Invalid key')

    result['team'] = user.uuid

    return jsonify(result)


@APP.route('/validate-session', methods=['POST'])
def validate_session():
    """
    Validates if the session is valid and returns the team_id

    :param token: the token for the users session

    :returns: json dict containing either success or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    token = token.replace("token=", "")

    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    result['success'] = session.uuid

    return jsonify(result)

@APP.route('/login', methods=['POST'])
def login():
    """
    Verifies if a the submitted credentials are correct

    :param username: username of the team
    :param password: teams password
    :param key(optional): this is for when white team is logging in through their card
    :returns result: json dict containing either a success or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    if 'key' in data:
        key = data['key']
        key = key[5:-1]
        user = Team.query.filter_by(private_key=key).first()
        if user is None:
            raise errors.AuthError('Invalid key')
    else:
        params = ['username', 'password']
        validate_request(params, data)

        username = data['username']
        password = data['password']
        user = Team.query.filter_by(username=username, password=password).first()
        if user is None:
            raise errors.AuthError('Invalid username or password')

    # IF TOKEN ALREADY EXISTS THEN SEND THAT ONE BACK
    sesh = Session.query.filter_by(uuid=user.uuid).first()
    if sesh.token is not None:
        token = sesh.token
    else:
        token = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        new_session(user.uuid, token, request.remote_addr)

    result['token'] = token
    result['team_id'] = user.uuid
    resp = make_response(json.dumps(result), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    return resp

@APP.route('/update-password', methods=['POST'])
def update_password():
    """
    Updates a teams password

    :param old_password: old team password
    :param new_password: new team password
    :param token: the auth token for the account

    :returns result: json dict containing either a success or and error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['old_password', 'token', 'new_password']
    validate_request(params, data)

    old_password = data['old_password']
    new_password = data['new_password']
    token = data['token']

    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    user = Team.query.filter_by(uuid=session.uuid).first()
    if user.password != old_password:
        raise errors.AuthError("Old password does not match")

    user.password = new_password
    DB.session.commit()
    result['success'] = "Successfully updated password"

    return jsonify(result)

@APP.route('/expire-session', methods=['POST'])
def expire_session():
    """
    Set a teams auth token to NULL, essentially expiring their session

    :param token: the authentication token to expire, must be valid
    :param team_id: the id of the team
    :return result: json dict containing either a success or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    session = Session.query.filter_by(token=token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    session.token = None
    DB.session.commit()
    result['success'] = 'Token expired'

    return jsonify(result)

@APP.route('/update-session', methods=['POST'])
def update_session():
    """
    Updates a teams auth token from an old one to a new one.

    :param old_token: the old auth token, must be valid
    :param new_token: the new token to be set

    :returns result: json dict containg either a success or a error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['old_token', 'new_token']
    validate_request(params, data)

    old_token = data['old_token']
    new_token = data['new_token']
    session = Session.query.filter_by(token=old_token).first()
    if session is None:
        raise errors.AuthError('Invalid session')

    session.token = new_token
    DB.session.commit()
    result['success'] = 'Token updated'

    return jsonify(result)

@APP.route('/pub-key', methods=['POST'])
def get_pub_key():
    """
        Returns the public key for the given team

        :param team_id: the id of the team

        :returns result: json dict containing either the public key or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['team_id']
    validate_request(params, data)

    team_id = data['team_id']

    user = Team.query.filter_by(uuid=team_id).first()
    if user is None:
        raise errors.TeamError("Team not found")

    pub_key = user.pub_key
    result['pub_key'] = pub_key

    return jsonify(result)
