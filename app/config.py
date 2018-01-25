"""
    Config parameters for our web app
"""

BANK_API_URL = "http://lilbite.org:5000"
AUTH_API_URL = "http://lilbite.org:9000"
SECRET_KEY = 'thenotsosecretkey'

AUTH_ENDPOINTS = ['validate-session', 'login', 'update-password',
                  'expire-session', 'update-session', 'pub-key']
