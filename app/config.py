"""
    Config parameters for our web app
"""

BANK_API_URL = "http://atlas.whiteteam.ritsec:5000"
AUTH_API_URL = "http://atlas.whiteteam.ritsec:9000"
SECRET_KEY = 'thenotsosecretkey'

AUTH_ENDPOINTS = ['validate-session', 'login', 'update-password',
                  'expire-session', 'update-session', 'pub-key']
