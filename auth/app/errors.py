"""
    Errors our API can raise
"""
from flask import jsonify, request
from . import APP, logger


class APIErrors(Exception):
    """
    Custom class for our API errors

    :param message: the message to send back to the user
    :param status_code: the specific status code to display
    """
    def __init__(self, message=None, status_code=403):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """Converts our error into a dict to send back"""
        rv = dict()
        rv['error'] = self.message
        return rv


class AuthError(APIErrors):
    """Errors with invalid credentials/sessions"""
    def __init__(self, message=None, status_code=403):
        APIErrors.__init__(self, message, status_code)

class TeamError(APIErrors):
    """IErrors with team accounts"""
    def __init__(self, message=None, status_code=200):
        APIErrors.__init__(self, message, status_code)

class RequestError(APIErrors):
    """Errros with missing or malformed request parameters"""
    def __init__(self, message=None, status_code=400):
        APIErrors.__init__(self, message, status_code)


@APP.errorhandler(APIErrors)
def handle_api_error(error):
    """flask error handler for our custom errors"""
    logger.error("[%s] - %s", request.remote_addr, error.to_dict()['error'])

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
