"""
    Tests the app login functionality
"""
from app.tests.util import AppTestCases

class LoginTests(AppTestCases):
    """Collection of tests for the login functionality"""


    def test_successful_login(self):
        '''This login should execute successfully'''
        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "account"))
        assert str(self.client.title) == "Account"

    def test_bad_creds(self):
        """This login should fail from bad creds"""
        self.login("baduser", "badpass")
        self.client.get("{}/{}".format(self.APP_URL, "account"))
        assert str(self.client.title) == "Error"
