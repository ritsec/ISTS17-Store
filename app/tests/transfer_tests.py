"""
    Tests transfer limitations
"""
from app.tests.util import AppTestCases
from app.util import api_request
# from random import randint
import time


class TransferTests(AppTestCases):
    """Collection of tests for the tranfer functionality"""
    

    def test_transfer_splash(self):
        '''The transfer splash page should execute successfully'''
        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "transfer"))
        assert str(self.client.title) == "Transfer"

    def test_transfer(self):
        '''The transfer should execute successfully'''
        TEST_TEAM = "2"

        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "account"))

        balance = self.client.find_element_by_id("balance").text
        self.client.get("{}/{}".format(self.APP_URL, "transfer"))

        team_field = self.client.find_element_by_id("team")
        amount_field = self.client.find_element_by_id("amount")

        team_field.send_keys(TEST_TEAM)
        amount_field.send_keys("1")

        self.client.find_element_by_name("transfer_form").submit()
        assert str(self.client.title) == "Transfer"

        time.sleep(5)
    
    def test_insufficient_transfer(self):
        '''The transfer should error'''
        TEST_TEAM = "2"

        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "account"))

        balance = float(self.client.find_element_by_id("balance").text)+1
        
        self.client.get("{}/{}".format(self.APP_URL, "transfer"))

        team_field = self.client.find_element_by_id("team")
        amount_field = self.client.find_element_by_id("amount")

        team_field.send_keys(TEST_TEAM)
        amount_field.send_keys("1")

        self.client.find_element_by_name("transfer_form").submit()
        # assert str(self.client.find_element_by_id("error") == "Insufficient Funds"
        
        time.sleep(5)