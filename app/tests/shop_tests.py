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
        '''The shop page should succeed'''
        self.login(self.TEST_USER, self.TEST_PASS)
        self.client.get("{}/{}".format(self.APP_URL, "shop"))
        buttons = self.client.find_elements_by_class_name("buy")
        for x in range(0,len(buttons)):
            if buttons[x].is_displayed():
                buttons[x].click()
                time.sleep(2)
                assert str(self.client.find_element_by_id("result").text) == "Item bought"
                time.sleep(2)


    def test_unauthenticated_shop_buy(self):
        '''The shop page should fail'''
        self.client.get("{}/{}".format(self.APP_URL, "shop"))
        buttons = self.client.find_elements_by_class_name("buy")
        for x in range(0,len(buttons)):
            if buttons[x].is_displayed():
                buttons[x].click()
                time.sleep(2)
                assert self.client.find_element_by_id("result")
                time.sleep(2)