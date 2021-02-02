import logging

import pytest
from selene.support.shared import browser

from .pages.login import LoginPage

logger = logging.getLogger()

login_page = LoginPage()


@pytest.fixture(autouse=True)
def setup():
    url = 'https://www.saucedemo.com'
    logger.info(f'----- Opening browser and navigating to {url} -----'
    browser.config.base_url = url


def test_login():
    login_page.login_to_application('standard_user', 'secret_sauce')
    login_page.assert_logged_in()


def test_invalid_password():
    login_page.login_to_application('standard_user', 'bad_password')
    login_page.assert_not_logged_in()
    login_page.assert_error_matches_expected(
        'Epic sadface: Username and password do not match any user in this service'
    )


def test_no_user_name():
    login_page.login_to_application('', 'secret_sauce')
    login_page.assert_not_logged_in()
    login_page.assert_error_matches_expected(
        'Epic sadface: Username is required')


def test_no_password():
    login_page.login_to_application('standard_user', '')
    login_page.assert_not_logged_in()
    login_page.assert_error_matches_expected(
        'Epic sadface: Password is required')
