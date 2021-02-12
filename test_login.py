import logging

import pytest
from selene.support.shared import browser

from .base_test import BaseTest

logger = logging.getLogger()


class TestLogin(BaseTest):

    @pytest.fixture(autouse=True)
    def setup(self):
        url = 'https://www.saucedemo.com'
        logger.info(f'----- Opening browser and navigating to {url} -----')
        browser.config.base_url = url

    def test_login(self):
        self.login_page.login_to_application('standard_user', 'secret_sauce')
        self.login_page.assert_logged_in()

    def test_invalid_password(self):
        self.login_page.login_to_application('standard_user', 'bad_password')
        self.login_page.assert_not_logged_in()
        self.login_page.assert_error_matches_expected(
            'Epic sadface: Username and password do not match any user in this service'
        )

    def test_no_user_name(self):
        self.login_page.login_to_application('', 'secret_sauce')
        self.login_page.assert_not_logged_in()
        self.login_page.assert_error_matches_expected(
            'Epic sadface: Username is required')

    def test_no_password(self):
        self.login_page.login_to_application('standard_user', '')
        self.login_page.assert_not_logged_in()
        self.login_page.assert_error_matches_expected(
            'Epic sadface: Password is required')

    def test_user_locked_out(self):
        self.login_page.login_to_application('locked_out_user', 'secret_sauce')
        self.login_page.assert_not_logged_in()
        self.login_page.assert_error_matches_expected(
            'Epic sadface: Sorry, this user has been locked out.')
