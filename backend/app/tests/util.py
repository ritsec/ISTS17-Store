"""
    Util functions and class for each test to use
"""
import json
import unittest
from app import APP, DB
from app.models.teams import Team
from app.config import DEFAULT_BALANCE, DEFAULT_PASSWORD

class ApiTestCases(unittest.TestCase):
    """Collection of unit tests for the different API endpoints"""

    TEST_USER = "team1"
    TEST_PASS = "Changeme-2018"

    def setUp(self):
        """
        Set up our testing client
        """
        APP.testing = True
        self.app = APP.test_client()

    def tearDown(self):
        # reset everyones balance and password back the default
        teams = Team.query.all()
        for t in teams:
            t.balance = DEFAULT_BALANCE
            t.passsword = DEFAULT_PASSWORD

        DB.session.commit()

    def login(self, username, password):
        """
        Helper function to log in

        :param username: username of the team
        :param password: passsword of the team

        :return result: the result of the login post request
        """
        token = username + password
        data = dict(username=username, password=password, token=token)

        result = self.app.post('/login', data=data)
        assert result.status_code == 200

        return token

    def get_balance(self, token):
        """
        Helper function to get account balance

        :param token: auth token for the account

        :returns balance: balance of the account
        """
        data = dict(token=token)
        result = self.app.post('/get-balance', data=data)
        result = json.loads(result.data)
        return result['balance']
