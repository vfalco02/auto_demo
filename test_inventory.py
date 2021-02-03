import logging

import pytest
from selene.support.shared import browser

from .pages.login import LoginPage
from .pages.inventory import InventoryPage

logger = logging.getLogger()

login_page = LoginPage()
inventory_page = InventoryPage()


@pytest.fixture(scope='session', autouse=True)
def setup():
    url = 'https://www.saucedemo.com'
    logger.info(f'----- Opening browser and navigating to {url} -----')
    browser.config.base_url = url
    login_page.login_to_application('standard_user', 'secret_sauce')
    login_page.assert_logged_in()


@pytest.mark.dependency(name='add item')
def test_add_item_to_cart():
    inventory_page.add_item_to_cart('Sauce Labs Bolt T-Shirt')


@pytest.mark.dependency(name='remove item', depends=['add item'])
def test_remove_item_from_cart():
    inventory_page.remove_item_from_cart('Sauce Labs Bolt T-Shirt')


@pytest.mark.dependency(name='add all items', depends=['remove item'])
def test_add_all_items_to_cart():
    inventory_page.add_all_items_to_cart()


@pytest.mark.dependency(name='remove all items', depends=['add all items'])
def test_remove_all_items_from_cart():
    inventory_page.remove_all_items_from_cart()
