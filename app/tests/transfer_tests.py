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
        if balance > 1: 
            amount = 1
        else:
            print 'not enough'
        # amount = randint(1, float(balance))
        self.client.get("{}/{}".format(self.APP_URL, "transfer"))

        team_field = self.client.find_element_by_id("team")
        amount_field = self.client.find_element_by_id("amount")

        team_field.send_keys(TEST_TEAM)
        amount_field.send_keys(amount)

        self.client.find_element_by_name("transfer_form").submit()
        time.sleep(10)



        # cookie_list = self.client.get_cookies()
        # print cookie_list
        # token = str(cookie_list[0]['value'])
        # post_data = dict()
        # post_data['token'] = token

        # get balance
        # resp = api_request("get-balance", post_data)
        # balance = resp['balance']
        # print balance
        # # transfer_url = "{}/{}".format(self.APP_URL, "transfer")