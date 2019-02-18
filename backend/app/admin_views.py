from flask import request, jsonify, abort
from . import APP, DB, logger, errors
from .models.teams import Team
from .models.transaction import Transaction
from .models.item import Item
from .util import validate_request, validate_session

"""
WHITETEAM admin routes
"""
@APP.route('/admin-get-balance', methods=['POST'])
def admin_get_balance():
    """
    Route for white team APIs to get balance of other teams

    :param token: should be token for white team
    :param team_id: the team id to get the balance for

    :returns result: json dict containg either account balance or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'team_id']
    validate_request(params, data)

    token = data['token']
    team_id = data['team_id']
    session_team_id = validate_session(token)
    if session_team_id != 1337:
        raise errors.RequestError("Not white team")

    user = Team.query.filter_by(uuid=team_id).first()
    balance = user.balance
    result['balance'] = balance
    result['team_id'] = team_id
    return jsonify(result)

@APP.route('/admin-add-credits', methods=['POST'])
def admin_add_credits():
    """
    Route for white team to add credits to a specific team

    :param token: should be a token for white team
    :param team_id: the team to add the credits to
    :param amount: the amount of credits to add

    :return result: json dict containg either success or error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'team_id', 'amount']
    validate_request(params, data)

    token = data['token']
    team_id = data['team_id']
    try:
        amount = float(data['amount'])
    except Exception:
        raise errors.RequestError("Please enter a number")

    session_team_id = validate_session(token)
    if session_team_id != 1337 and session_team_id != 47:
        raise errors.RequestError("Not white team")

    user = Team.query.filter_by(uuid=team_id).first()
    if user is None:
        raise errors.TeamError("Team {} doesn't exist".format(team_id), status_code=404)

    user.balance += amount
    DB.session.commit()

    logger.info("White Team added %d credtis for Team %d", amount, user.uuid)

    result['success'] = "Successfully added credits"
    return jsonify(result)

@APP.route('/admin-remove-credits', methods=['POST'])
def admin_remove_credits():
    """
    Route for white team to remove credits to a specific team

    :param token: should be a token for white team
    :param team_id: the team to add the credits to
    :param amount: the amount of credits to add

    :return result: json dict containg either success or error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'team_id', 'amount']
    validate_request(params, data)

    token = data['token']
    team_id = data['team_id']
    try:
        amount = float(data['amount'])
    except Exception:
        raise errors.RequestError("Please enter a number")

    session_team_id = validate_session(token)
    if session_team_id != 1337:
        raise errors.RequestError("Not white team")

    user = Team.query.filter_by(uuid=team_id).first()
    if user is None:
        raise errors.TeamError("Team {} doesn't exist".format(team_id), status_code=404)

    user.balance -= amount
    DB.session.commit()

    logger.info("White Team removed %d credtis for Team %d", amount, user.uuid)

    result['success'] = "Successfully removed credits"
    return jsonify(result)

@APP.route('/admin-set-credits', methods=['POST'])
def admin_set_credits():
    """
    Route for white team to set credits for a team

    :param token: should be a token for white team
    :param team_id: the team to add the credits to
    :param amount: the amount of credits to add

    :return result: json dict containg either success or error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'team_id', 'amount']
    validate_request(params, data)

    token = data['token']
    team_id = data['team_id']
    try:
        amount = float(data['amount'])
    except Exception:
        raise errors.RequestError("Please enter a number")

    session_team_id = validate_session(token)
    if session_team_id != 1337:
        raise errors.RequestError("Not white team")

    user = Team.query.filter_by(uuid=team_id).first()
    if user is None:
        raise errors.TeamError("Team {} doesn't exist".format(team_id), status_code=404)

    user.balance = amount
    DB.session.commit()
    logger.info("White Team set %d credtis for Team %d", amount, user.uuid)

    result['success'] = "Successfully set credits"
    return jsonify(result)
