"""
    Config parameters for our web app
"""
import os
STORE_API = os.environ.get("STORE_API", "http://0.0.0.0:5000")
#BANK_API_URL
#AUTH_API_URL = "http://10.0.20.21:9000"
SECRET_KEY = 'thenotsosecretkey'

AUTH_ENDPOINTS = ['validate-session', 'login', 'update-password',
                  'expire-session', 'update-session', 'pub-key']

AUTH_API_URL=os.environ.get("AUTH_API", "http://auth:5000")
