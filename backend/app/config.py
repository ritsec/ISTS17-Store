"""
Configuration settings.
"""
import os
import logging
import sys

class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.INFO

class ErrorFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno == logging.ERROR

AUTH_API_URL = "http://lilbite.org:9000"
SHIP_API_URL = "http://lilbite.org:6000"


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.environ.get("MYSQL_USER", "root"),
    os.environ.get("MYSQL_PASS", "youwontguess23$"),
    os.environ.get("MYSQL_SERVER", "0.0.0.0"),
    os.environ.get("MYSQL_PATH", "ists"))



#SQLALCHEMY_DATABASE_URI = 'mysql://root:youwontguess23$@localhost/ists'

#WHITETEAM_SLACK_URI = "https://hooks.slack.com/services/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"
#REDTEAM_SLACK_URI ="https://hooks.slack.com/services/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"
#CHANNEL = "#white-team-tool"
#SLACK_USERNAME = "White Team Store"
#ICON_EMOJI = ":money_with_wings:"

#SHIP_API_ALERT_ITEMS = ['x1 Strikers', 'Health +50%', 'Damage +50%',
#                        'Speed +50%', 'Enemy Health -25%', 'Enemy Damage -25%',
#                        'Enemy Speed -25%', 'Destroy an enemy ship']

#RED_TEAM_ALERT_ITEMS = ['Snapshot Revert', 'Revert Raspberry Pi']

'''
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'info_filter': {
            '()': InfoFilter,
        },
        'error_filter': {
            '()': ErrorFilter,
        }
    },
    'handlers': {
        'info': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  '/var/log/flask/info.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['info_filter']
        },
        'error': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename':  '/var/log/flask/error.log',
            'mode': 'a',
            'backupCount': '16',
            'filters': ['error_filter']
        },
    },
    'loggers': {
        'api_log': {'handlers': ['info', 'error'], 'level': 'DEBUG', 'propagate': False},
    }
}
'''