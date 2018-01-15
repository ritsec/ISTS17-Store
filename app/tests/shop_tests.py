"""
    Tests shop functionality
"""
from app.tests.util import AppTestCases
import unittest
import pytest
import time

class ShopTests(AppTestCases):
    """Collection of tests for the shop"""

    def test_shop_buy(self):
        '''The shop page should splash succeed'''
        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "shop"))
        like = self.client.find_elements_by_class_name("buy")
        print("ALL_SPANS: {}".format(like))
        for x in range(0,len(like)):
            if like[x].is_displayed():
                like[x].click()
                time.sleep(2)
                alert = self.client.switch_to_alert()
                time.sleep(2)
                alert.accept()
                
        assert str(self.client.find_element_by_id("content"))
