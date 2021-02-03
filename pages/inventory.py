import logging

from selene.api import s, ss, be, query

logger = logging.getLogger()


class InventoryPage:
    div_inventory_item = '.inventory_item'
    div_item_name = '//div[@class="inventory_item_name"][text()="{item_name}"]'

    btn_add_remove = 'button.btn_inventory'

    lbl_item_name = '.inventory_item_name'
    lbl_item_price = '.inventory_item_price'
    lbl_item_description = '.inventory_item_desc'
    lbl_shopping_cart_count = '.shopping_cart_badge'

    def _get_all_items(self):
        items = [{
            'name': item.s(self.lbl_item_name).get(query.text),
            'desc': item.s(self.lbl_item_description).get(query.text),
            'price': item.s(self.lbl_item_price).get(query.text),
            'element': item
        } for item in ss(self.div_inventory_item)]
        return items

    def _get_item_container(self, item_name):
        logger.debug(f'--- Getting container for item {item_name} ---')
        item_name_loc = self.div_item_name.format(item_name=item_name)
        parent_loc = f'{item_name_loc}//ancestor::div[2]'
        parent_container = s(parent_loc)
        return parent_container

    def _get_item_description(self, item_name):
        logger.debug(f'--- Getting description for item {item_name} ---')
        parent_container = self._get_item_container(item_name)
        description_div = parent_container.s(self.lbl_item_desc)
        return description_div.get(query.text)

    def _get_item_price(self, item_name):
        logger.debug(f'--- Getting price for item {item_name} ---')
        parent_container = self._get_item_container(item_name)
        price_div = parent_container.s(self.lbl_item_price)
        return price_div.get(query.text)

    def _add_remove_item(self, add_or_remove, item_name):
        logger.debug(
            f'--- {add_or_remove.title()} item {item_name} to/from cart ---')
        parent_container = self._get_item_container(item_name)
        add_remove_btn = parent_container.s(self.btn_add_remove)
        if add_or_remove.lower() == 'add':
            assert add_remove_btn.get(query.text).upper() == 'ADD TO CART', (
                f'The item {item_name} is already in the cart')
        elif add_or_remove.lower() == 'remove':
            assert add_remove_btn.get(query.text).upper() == 'REMOVE', (
                f'The item {item_name} is not in the cart')
        add_remove_btn.click()

    def _get_cart_count(self):
        logger.debug('--- Getting the cart count ---')
        if not s(self.lbl_shopping_cart_count).with_(timeout=0).wait_until(
                be.visible):
            return 0
        count = s(self.lbl_shopping_cart_count).get(query.text)
        return int(count)

    def _assert_item_shows_in_cart(self, item_name):
        logger.debug(
            f'--- Validating item  {item_name} shows it is in the cart ---')
        parent_container = self._get_item_container(item_name)
        add_btn = parent_container.s(self.btn_add_remove)
        assert add_btn.get(query.text).upper() == 'REMOVE', (
            f'The item {item_name} does not show in cart')

    def _assert_item_shows_available(self, item_name):
        logger.debug(
            f'--- Validating item  {item_name} shows it is available ---')
        parent_container = self._get_item_container(item_name)
        add_btn = parent_container.s(self.btn_add_remove)
        assert add_btn.get(query.text).upper() == 'ADD TO CART', (
            f'The item {item_name} does not show as available')

    def add_item_to_cart(self, item_name):
        logger.info(f'----- Adding item {item_name} to the cart -----')
        current_count = self._get_cart_count()
        self._add_remove_item('add', item_name)
        self._assert_item_shows_in_cart(item_name)
        new_count = self._get_cart_count()
        assert new_count == current_count + 1, 'The cart count did not increment by 1'

    def remove_item_from_cart(self, item_name):
        logger.info(f'----- Removing item {item_name} from the cart -----')
        current_count = self._get_cart_count()
        self._add_remove_item('remove', item_name)
        self._assert_item_shows_available(item_name)
        new_count = self._get_cart_count()
        assert new_count == current_count - 1, 'The cart count did not decrement by 1'

    def add_all_items_to_cart(self):
        logger.info('----- Adding all items to the cart -----')
        items = self._get_all_items()
        for item in items:
            current_count = self._get_cart_count()
            if item['element'].s(self.btn_add_remove).get(
                    query.text).upper() == 'ADD TO CART':
                item['element'].s(self.btn_add_remove).click()
                new_count = self._get_cart_count()
                assert new_count == current_count + 1, 'The cart count did not increment by 1'

    def remove_all_items_from_cart(self):
        logger.info('----- Removing all items from the cart -----')
        items = self._get_all_items()
        for item in items:
            current_count = self._get_cart_count()
            if item['element'].s(self.btn_add_remove).get(
                    query.text).upper() == 'REMOVE':
                item['element'].s(self.btn_add_remove).click()
                new_count = self._get_cart_count()
                assert new_count == current_count - 1, 'The cart count did not decrement by 1'
