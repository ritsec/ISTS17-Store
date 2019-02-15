"""
    Main test file
"""
import unittest
from app.tests.util import ApiTestCases
from app.tests.auth_tests import AuthTests
from app.tests.buying_tests import BuyingTests
from app.tests.transfer_tests import TransferTests


if __name__ == '__main__':
    unittest.main()
