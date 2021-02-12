from .pages.login import LoginPage
from .pages.inventory import InventoryPage
from .pages.cart import CartPage


class BaseTest:

    login_page = LoginPage()
    inventory_page = InventoryPage()
    cart_page = CartPage()
