"""
    Initialize our flask app
"""
import sys
from flask import Flask

APP = Flask(__name__)

from .views import *
