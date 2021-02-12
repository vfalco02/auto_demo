import logging

import pytest
from selene.support.shared import browser

from .base_test import BaseTest

logger = logging.getLogger()


class TestCart(BaseTest):
    test_item = 'Sauce Labs Bolt T-Shirt'

    @pytest.fixture(scope='session', autouse=True)
    def setup(self):
        url = 'https://www.saucedemo.com'
        logger.info(f'----- Opening browser and navigating to {url} -----')
        browser.config.base_url = url
        self.login_page.login_to_application('standard_user', 'secret_sauce')
        self.login_page.assert_logged_in()

    def test_item_in_cart(self):
        self.inventory_page.add_item_to_cart(self.test_item)
        self.cart_page.go_to_cart()
        self.cart_page.assert_item_in_cart(self.test_item)
