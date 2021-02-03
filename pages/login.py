import logging

from selene.api import s, have, query
from selene.support.shared import browser

logger = logging.getLogger()


class LoginPage:

    # LOCATORS
    txt_user_name = '#user-name'
    txt_password = '#password'

    btn_login = '#login-button'

    err_error = 'h3[data-test="error"]'

    # HELPER METHODS
    def _navigate_to_login(self):
        logger.debug('--- Navigating to login page -----')
        browser.open('/index.html')

    def _enter_user_name(self, user_name):
        logger.debug('--- Entering user name: %s ---', user_name)
        s(self.txt_user_name).set_value(user_name)

    def _enter_password(self, password):
        logger.debug('--- Entering password ---')
        s(self.txt_password).set_value(password)

    def _click_login(self):
        logger.debug('--- Clicking login button ---')
        s(self.btn_login).click()

    def _get_error_text(self):
        logger.debug('--- Getting error text ---')
        s(self.err_error).get(query.text)

    def assert_logged_in(self):
        logger.debug('--- Validating user is logged in ---')
        browser.should(have.url_containing('/inventory.html'))

    def assert_not_logged_in(self):
        logger.debug('--- Validating user is not logged in ---')
        browser.should(have.url_containing('/index.html'))

    # FULL METHODS
    def login_to_application(self, user_name, password):
        logger.info('----- Logging into application with user_name: %s -----',
                    user_name)
        self._navigate_to_login()
        self._enter_user_name(user_name)
        self._enter_password(password)
        self._click_login()

    def assert_error_matches_expected(self, expected_text):
        logger.info('----- Validating error message matches "%s" -----',
                    expected_text)
        actual_error = s(self.err_error).get(query.text)
        assert actual_error == expected_text, f'{actual_error} != {expected_text}'
