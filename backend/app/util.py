"""
    File to hold utility functions
"""
import requests
from .config import (AUTH_API_URL, WHITETEAM_SLACK_URI, CHANNEL, SLACK_USERNAME,
                     ICON_EMOJI, REDTEAM_SLACK_URI, SHIP_API_URL)
from .models.item import Item
from .models.session import Session
from .errors import RequestError, AuthError, TransactionError

def validate_session(token):
    """
    Sends token to auth server to validate, should recieve
    associated team number if it is valid

    :param token: the session token to validate

    :return team_id: the id of the team the token is attached to
    """
    post_data = dict()
    post_data['token'] = token
    resp = auth_api_request('validate-session', post_data)
    if 'success' not in resp:
        raise AuthError(resp['error'])

    team_id = resp['success']
    return team_id

def auth_api_request(endpoint, data):
    """
    Makes a request to our api and returns the response

    :param endpoint: the api endpoint to hit
    :param data: the data to send in dictionary format
    :param url: the url of the api

    :returns resp: the api response
    """
    print data
    url = "{}/{}".format(AUTH_API_URL, endpoint)

    resp = requests.post(url, data=data)
    if resp.status_code == 400:
        raise RequestError("Bad request sent to API")

    if resp.status_code == 403:
        raise AuthError(resp.json()['error'])

    elif resp.status_code != 200:
        raise RequestError("API returned {} for /{}".format(
            resp.status_code, endpoint))

    resp_data = resp.json()
    return resp_data

def get_item_price(item_id):
    """
    Returns the price of an item from the database

    :param item_id: id of the item

    :returns price: price of the item
    """
    item = Item.query.filter_by(uuid=item_id).first()
    if item is None:
        raise TransactionError("Item not found", status_code=404)

    return item.price

def validate_request(params, data):
    """
    Verifies all the required parameters are in the request

    :param params: an array of the required parameters
    :param data: the json data in the post request
    """
    for p in params:
        if p not in data:
            raise RequestError("Missing {}".format(p), status_code=400)

    return True

def post_slack(message, team='white'):
    """
    Posts a message to our white team slack

    :param message: the message to post to slack
    :param team: the slack team to post to
    """
    post_data = dict()
    post_data["text"] = message
    post_data["channel"] = CHANNEL
    post_data["link_names"] = 1
    post_data["username"] = SLACK_USERNAME
    post_data["icon_emoji"] = ICON_EMOJI

    if team == 'red':
        post_data['channel'] = "#box-resets"
        slack_uri = REDTEAM_SLACK_URI
    else:
        slack_uri = WHITETEAM_SLACK_URI

    requests.post(slack_uri, json=post_data)

def ship_api_request(token, item, team_id, enemy_id):
    """
    Notifies our ship api that a escort mission item has been bought

    :param token: the auth token for the backend
    :param item: the name of the item
    :param team_id: the id of the team
    :param enemy_id: the id of the enemy team if they bought a powerup against them
    """
    post_data = dict()
    print "Make request for {} by {}".format(item, team_id)
    # for this type of request we need white team token
    if enemy_id is not None:
        sesh = Session.query.filter_by(uuid=1337).first()
        token = sesh.token

    cookies = {'token': str(token)}

    if 'striker' in item.lower():
        post_data['value'] = 1
        requests.post("{}/teams/{}/striker".format(SHIP_API_URL, team_id),
                      json=post_data, cookies=cookies)

        return None

    if 'ship' in item.lower():
        post_data['value'] = -1
        requests.post("{}/teams/{}/striker".format(SHIP_API_URL, enemy_id),
                      json=post_data, cookies=cookies)

        return None

    if 'health' in item.lower():
        post_data['type'] = 'health'
    elif 'damage' in item.lower():
        post_data['type'] = 'damage'
    elif 'speed' in item.lower():
        post_data['type'] = 'speed'

    if 'enemy' in item.lower():
        post_data['change'] = 'decrease'
        post_data['value'] = -25
    else:
        post_data['change'] = 'increase'
        post_data['value'] = 50

    if enemy_id is not None:
        requests.post("{}/teams/{}/boost".format(SHIP_API_URL, enemy_id),
                      json=post_data, cookies=cookies)
    else:
        requests.post("{}/teams/{}/boost".format(SHIP_API_URL, team_id),
                      json=post_data, cookies=cookies)
