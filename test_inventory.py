import logging
import os

import pytest
from selene.support.shared import browser
import yaml

from .base_test import BaseTest

logger = logging.getLogger()


def load_item_information_from_file():
    path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    filename = './inventory.yml'
    with open(f'{path}/{filename}') as f:
        items = yaml.load(f, Loader=yaml.Loader)
    return items['items']


class TestInventory(BaseTest):

    @pytest.fixture(scope='session', autouse=True)
    def setup(self):
        url = 'https://www.saucedemo.com'
        logger.info(f'----- Opening browser and navigating to {url} -----')
        browser.config.base_url = url
        self.login_page.login_to_application('standard_user', 'secret_sauce')
        self.login_page.assert_logged_in()

    def test_item_information(self):
        item_info = load_item_information_from_file()
        for item in item_info:
            self.inventory_page.validate_item_information(item)

    @pytest.mark.dependency(name='add item')
    def test_add_item_to_cart(self):
        self.inventory_page.add_item_to_cart('Sauce Labs Bolt T-Shirt')

    @pytest.mark.dependency(name='remove item', depends=['add item'])
    def test_remove_item_from_cart(self):
        self.inventory_page.remove_item_from_cart('Sauce Labs Bolt T-Shirt')

    @pytest.mark.dependency(name='add all items', depends=['remove item'])
    def test_add_all_items_to_cart(self):
        self.inventory_page.add_all_items_to_cart()

    @pytest.mark.dependency(name='remove all items', depends=['add all items'])
    def test_remove_all_items_from_cart(self):
        self.inventory_page.remove_all_items_from_cart()

    # TODO: Add tests for ordering
