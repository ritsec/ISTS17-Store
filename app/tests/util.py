"""
    Util functions and classes to test our ecomm app
"""
import time
import unittest
from selenium import webdriver
import xvfbwrapper
from app.config import API_URL

class AppTestCases(unittest.TestCase):
    """Collection of unit tests for the different APP endpoints"""

    TEST_USER = "team1"
    TEST_PASS = "Changeme-2018"
    API_URL = API_URL
    APP_URL = "http://127.0.0.1:8000"

    def setUp(self):
        """
        Set up our testing client
        """
        self.client = webdriver.Firefox()

    def tearDown(self):
        self.client.get("{}/logout".format(self.APP_URL))

    def login(self, username, password):
        """
        Logs in to our web app

        :param username: the username to log in with
        :param password: the password of the user
        """
        self.client.get("{}/login".format(self.APP_URL))

        username_field = self.client.find_element_by_id("username")
        password_field = self.client.find_element_by_id("password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        self.client.find_element_by_name("login_form").submit()
        time.sleep(2)
