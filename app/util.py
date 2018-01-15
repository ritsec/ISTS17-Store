"""
    Utility functions for the ecomm app
"""
import requests
from .config import API_URL
from .errors import APIConnectionError, APIBadRequest, AuthError, BadRequest


def api_request(endpoint, data):
    """
    Makes a request to our api and returns the response

    :param endpoint: the api endpoint to hit
    :param data: the data to send in dictionary format

    :returns resp: the api response
    """
    print data
    url = "{}/{}".format(API_URL, endpoint)
    resp = requests.post(url, data=data)
    if resp.status_code == 400:
        raise APIBadRequest("Bad request sent to API")

    if resp.status_code == 403:
        raise AuthError("Unauthorized for this endpoint")

    elif resp.status_code != 200:
        raise APIConnectionError("API returned {} for /{}".format(
            resp.status_code, endpoint))

    resp_data = resp.json()
    return resp_data

def validate_session(session):
    """
    Checks with the backend that our session is authenticated

    :param session: the session to check if its valid

    :returns token: the token stored in the session
    """

    if 'token' not in session:
        raise AuthError("No session token")

    token = session['token']
    post_data = dict()
    post_data['token'] = token

    resp = api_request("validate-session", post_data)
    if 'success' not in resp:
        raise AuthError(resp['error'])

    return token

def validate_request(params, data):
    """
    Verifies all the required parameters are in the request

    :param params: an array of the required parameters
    :param data: the json data in the post request
    """
    for p in params:
        if p not in data:
            raise BadRequest("Missing {}".format(p), status_code=400)

    return True