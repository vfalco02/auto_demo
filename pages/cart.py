import logging

from selene.support.shared import browser
from selene.api import s, ss, by, have, query

logger = logging.getLogger()


class CartPage:

    # LOCATORS
    btn_shopping_cart = '#shopping_cart_container'
    btn_continue_shopping = by.text('Continue Shopping')
    btn_checkout = '.checkout_button'
    btn_remove = '.cart_button'

    row_cart_item = '.cart_item'

    # HELPER METHODS
    def _get_item_row(self, item_name):
        logger.debug(f'--- Getting row for item "{item_name}" ---')
        rows = ss(self.row_cart_item)
        for row in rows:
            if item_name in row.get(query.text):
                return row
        return None

    # FULL METHODS
    def assert_item_in_cart(self, item_name):
        logger.info(f'--- Validating item "{item_name}" is in cart ---')
        assert self._get_item_row(item_name) is not None, \
            f'Item "{item_name}"" not in cart.'

    def assert_item_not_in_cart(self, item_name):
        logger.info(f'--- Validating item "{item_name}" is NOT in cart ---')
        assert self._get_item_row(item_name) is None, \
            f'Item "{item_name}"" in cart.'

    def go_to_cart(self):
        s(self.btn_shopping_cart).click()
        browser.should(have.url_containing('/cart.html'))

    def continue_shopping(self):
        s(self.btn_continue_shopping).click()
        browser.should(have.url_containing('/inventory.html'))

    def checkout(self):
        s(self.btn_checkout).click()
        browser.should(have.url_containing('/checkout-step-one.html'))

    def remove_item(self, item_name):
        self.assert_item_in_cart(item_name)
        row = self._get_item_row(item_name)
        row.s(self.btn_remove).click()
        self.assert_item_not_in_cart(item_name)
