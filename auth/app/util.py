"""
    File to hold utility functions
"""
import datetime
from . import DB
from .models.session import Session
from . import errors


def new_session(uuid, token, src):
    """
    Enters a new session for a user

    :param uuid: the users id
    :param token: the token to attach to their session
    :param src: the source ip of the request
    """
    now = datetime.datetime.utcnow()
    session = Session.query.filter_by(uuid=uuid).first()
    session.token = token
    session.time = now
    session.src = src
    DB.session.commit()


def validate_request(params, data):
    """
    Verifies all the required parameters are in the request

    :param params: an array of the required parameters
    :param data: the json data in the post request
    """
    for p in params:
        if p not in data:
            raise errors.RequestError("Missing {}".format(p), status_code=400)

    return True
