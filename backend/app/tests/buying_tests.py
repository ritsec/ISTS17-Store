"""
    Tests for buying and get balance functions
"""
from app.tests.util import ApiTestCases
from app.util import get_item_price

class BuyingTests(ApiTestCases):
    """Collection of unit tests for the buying endpoints"""

    def test_balance(self):
        """Test if we can get the balance of a user"""
        token = self.login(self.TEST_USER, self.TEST_PASS)
        balance = self.get_balance(token)
        assert balance is not None

    def test_buying_item(self):
        """Test if we can buy an item from the store"""
        token = self.login(self.TEST_USER, self.TEST_PASS)
        item_price = get_item_price(1)
        data = dict(token=token, item_id=1)
        current_balance = self.get_balance(token)

        result = self.app.post('/buy', data=data)

        # Verify we get the transaction id
        assert result.status_code == 200
        assert 'transaction_id' in result.data

        # verify the correct money was reducted from the account
        new_balance = self.get_balance(token)
        assert (current_balance - item_price) == new_balance

    def test_get_items(self):
        """Verify we can retrieve a list of the white team items"""
        result = self.app.get('/items')
        assert result.status_code == 200
        assert 'items' in result.data
        print result.data
