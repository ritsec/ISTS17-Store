"""
    Tests for authentication functions
"""
from app.tests.util import ApiTestCases

class AuthTests(ApiTestCases):
    """Collection of unit tests for the auth endpoints"""

    def test_login(self):
        """Test the login functionality of our app"""
        result = self.login(self.TEST_USER, self.TEST_PASS)
        assert result is not None

    def test_expire_session(self):
        """Test if expiring a session functions correctly"""
        token = self.login(self.TEST_USER, self.TEST_PASS)
        data = dict(token=token)
        result = self.app.post('/expire-session', data=data)
        assert result.status_code == 200

        # try to access endpoint after token expired, should fail
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403

    def test_update_token(self):
        """Test if you can update a token"""
        token = self.login(self.TEST_USER, self.TEST_PASS)
        data = dict(old_token=token, new_token='heythere')
        result = self.app.post('/update-session', data=data)
        assert result.status_code == 200

        # try to access endpoint with old token, should fail
        data['token'] = data['old_token']
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 403

        # try to access endpoint with new token, should succeed
        data['token'] = data['new_token']
        result = self.app.post('/get-balance', data=data)
        assert result.status_code == 200
