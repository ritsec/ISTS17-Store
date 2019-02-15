"""
    Document to represent a users session
"""
import datetime
from app import DB

class Session(DB.Model):
    """
    Represents a users session

    :param uuid: the id of the user (the team number)
    :param token: there unique session id
    :param time: the timestamp this session was created
    :param src: the src ip that initiated this session
    """

    __tablename__ = 'session'
    uuid = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(128))
    time = DB.Column(DB.DateTime, default=datetime.datetime.utcnow)
    src = DB.Column(DB.String(16))

    def __init__(self, time=None, uuid=None, token=None, src=None):
        self.time = time
        self.uuid = uuid
        self.token = token
        self.src = src

    def __repr__(self):
        return '<Session uudid={} token={} time={} ip={}>'.format(
            self.uuid, self.token, self.time, self.src)
