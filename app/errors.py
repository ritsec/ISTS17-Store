"""
    Errors our Ecommerce app can raise
"""
from flask import render_template
from . import APP

class APPErrors(Exception):
    """
    Custom class for our APP Errors

    :param message: the message to display to the user
    :param status_code: the specific status code to display
    """
    def __init__(self, message=None, status_code=500):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

class APIConnectionError(APPErrors):
    """Error connecting to the API"""
    def __init__(self, message=None, status_code=500):
        APPErrors.__init__(self, message, status_code)

class APIBadRequest(APPErrors):
    """Error from sending a bad request to the API"""
    def __init__(self, message=None, status_code=400):
        APPErrors.__init__(self, message, status_code)

class AuthError(APPErrors):
    """Error from not having an authorized token"""
    def __init__(self, message=None, status_code=403):
        APPErrors.__init__(self, message, status_code)

class BadRequest(APPErrors):
    """Error for when no params are sent to the endpoint"""
    def __init__(self, message=None, status_code=400):
        APPErrors.__init__(self, message, status_code)

@APP.errorhandler(APPErrors)
def handle_app_error(error):
    """Flask error handler for our internal errors"""
    return render_template("error.html", error=error.message)
