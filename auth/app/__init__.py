"""
    Initialize our database and flask app
"""
import logging.config
import sys
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import SQLALCHEMY_DATABASE_URI

APP = Flask(__name__)
logger = APP.logger
CORS(APP)

try:
    APP.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB = SQLAlchemy(APP)

except Exception as e:
    print(e)
    print("ERROR: Could not connect to database")
    sys.exit()

from .views import *
