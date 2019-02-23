"""
    Entry point for API calls
"""
from flask import request, jsonify, abort
from sqlalchemy import or_
from . import APP, DB, logger
from .models.teams import Team
from .models.transaction import Transaction
from .models.item import Item
from . import errors
from .util import validate_request, validate_session, post_slack, ship_api_request
#from .config import SHIP_API_ALERT_ITEMS, RED_TEAM_ALERT_ITEMS

# Import the admin views
from .admin_views import *

"""
    REGULAR ROUTES
"""
@APP.route('/get-balance', methods=['POST'])
def get_balance():
    """
    Gets the balance of a team

    :param token: the auth token for that team

    :returns result: json dict containing either the account balance or an error
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
    team_id = validate_session(token)

    user = Team.query.filter_by(uuid=team_id).first()
    balance = user.balance
    result['balance'] = balance
    result['team_id'] = team_id
    return jsonify(result)

@APP.route('/buy', methods=['POST'])
def buy():
    """
    Buys a item from the white team store

    :param token: the auth token for the team
    :param item_id: the id of the item to buy
    :param enemy_id(optional): if the item bought has a enemy_id
    :return result: json dict containg either the id of the transaction or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token', 'item_id']
    validate_request(params, data)

    enemy_id = None
    token = data['token']
    item_id = data['item_id']
    team_id = validate_session(token)
    user = Team.query.filter_by(uuid=team_id).first()
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise errors.TransactionError('Item not be found', status_code=404)

    balance = user.balance
    if balance < item.price:
        raise errors.TransactionError('Insufficient funds')

    user.balance -= item.price
    description = "{} bought {} from shop".format(user.username, item.name)

    # notify correct parties of the item being bought
    # TODO: Push a github issue of the item being bought

    # create our tranasction
    # dst = 1337 because 1337 is white team
    if enemy_id is not None:
        description = "{} bought {} from shop against Team {}".format(user.username, item.name, enemy_id)

    tx = Transaction(src=user.username, dst="whiteteam",
                     desc=description, amount=item.price)
    DB.session.add(tx)
    DB.session.commit()
    result['transaction_id'] = tx.uuid

    logger.info("Team %d bought item %s - [tx id: %d]", user.uuid, item.name, tx.uuid)
    post_slack(description, team='white')

    return jsonify(result)


@APP.route('/transactions', methods=['POST'])
def transactions():
    """
    Get a list of transactions made by the team

    :param token: the auth token for the team

    :returns result: json dict containing either an array of the transactions or an error.
    """
    result = dict()
    result['transactions'] = []
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['token']
    validate_request(params, data)

    token = data['token']
    team_id = validate_session(token)

    user = Team.query.filter_by(uuid=team_id).first()
    txs = Transaction.query.filter(or_(Transaction.src == user.username, Transaction.dst == user.username))
    for t in txs:
        tx_dict = t.__dict__
        del tx_dict['_sa_instance_state']
        result['transactions'].append(tx_dict)

    # reverse in newest first
    result['transactions'] = result['transactions'][::-1]
    return jsonify(result)

@APP.route('/transfer', methods=['POST'])
def transfers():
    """
    Transfer money from one teams account to another

    :param token: the auth token for the account
    :param recipient: the id of the team to send the funds to
    :param amount: amount to transfer
    :returns result: json dict containing the transaction id or an error
    """
    result = dict()
    data = request.get_json()
    if data is None:
        data = request.form
        if data is None:
            abort(400)

    # make sure we have all the correct parameters
    params = ['recipient', 'token', 'amount']
    validate_request(params, data)

    dst_id = data['recipient']
    try:
        amount = float(data['amount'])
    except Exception:
        raise errors.TransactionError("Please enter a number")

    if amount < 0:
        raise errors.TransactionError("Can't do negative amounts")

    token = data['token']
    team_id = validate_session(token)
    user = Team.query.filter_by(uuid=team_id).first()
    dst_user = Team.query.filter_by(uuid=dst_id).first()
    if dst_user is None:
        raise errors.TeamError("Team id not found", status_code=404)

    if user.balance < amount:
        raise errors.TransactionError('Insufficient funds')

    # transfer the funds
    user.balance -= amount
    dst_user.balance += amount
    # change to team names instead of id
    tx = Transaction(src=user.username, dst=dst_user.username,
                     desc="transfer to team {}".format(dst_id), amount=amount)
    DB.session.add(tx)
    DB.session.commit()

    logger.info("Team %d transfered %f$ to Team %d - [tx id: %d]",
                int(user.uuid), amount, int(dst_id), int(tx.uuid))
    result['transaction_id'] = tx.uuid
    return jsonify(result)


@APP.route('/items', methods=['POST'])
def get_items():
    """
    Items and their price from the white team store

    :return result: json dict containg either the id of the transaction or an error
    """
    result = dict()
    result['items'] = []
    items = Item.query.order_by(Item.price).all()
    for i in items:
        item_dict = dict()
        item_dict['name'] = i.__dict__['name']
        item_dict['description'] = i.__dict__['description']
        item_dict['price'] = i.__dict__['price']
        item_dict['image'] = i.__dict__['image']
        item_dict['uuid'] = i.__dict__['uuid']
        result['items'].append(item_dict)

    return jsonify(result)
