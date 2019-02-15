"""
    Initialize our flask app
"""
import sys
from flask import Flask
from .config import SECRET_KEY

APP = Flask(__name__)
APP.secret_key = SECRET_KEY

from .views import *
