"""
    Tests for transfer functions
"""
import json
from app.tests.util import ApiTestCases

class TransferTests(ApiTestCases):
    """Collection of unit tests for the transfer endpoints"""

    def test_transactions(self):
        """Test if we can get a list of transactions for a user"""
        token = self.login(self.TEST_USER, self.TEST_PASS)
        data = dict(token=token)
        result = self.app.post('/transactions', data=data)
        assert result.status_code == 200

        result_data = json.loads(result.data)
        assert 'transactions' in result_data
