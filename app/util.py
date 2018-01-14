"""
    Utility functions for the ecomm app
"""
import requests
from .config import API_URL
from .errors import APIConnectionError, APIBadRequest


def api_request(endpoint, data):
    """
    Makes a request to our api and returns the response

    :param endpoint: the api endpoint to hit
    :param data: the data to send in dictionary format

    :returns resp: the api response
    """
    url = "{}/{}".format(API_URL, endpoint)
    resp = requests.post(url, data=data)
    if resp.status_code == 400:
        raise APIBadRequest("Bad request sent to API")

    elif resp.status_code != 200:
        raise APIConnectionError("API returned {} for /{}".format(
            resp.status_code, endpoint))

    resp_data = resp.json()
    print resp_data
    return resp_data
