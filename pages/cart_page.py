from .base_page import BasePage
import os


class CartPage(BasePage):
    URL = "https://www.saucedemo.com/"
    
    # 商品页面元素
    SAUCE_LABS_BACKPACK = "[data-test='add-to-cart-sauce-labs-backpack']"
    SAUCE_LABS_BACKPACK_REMOVE = "[data-test='remove-sauce-labs-backpack']"
    SHOPPING_CART_ICON = "#shopping_cart_container"
    
    # 购物车页面元素
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_QUANTITY = ".cart_quantity"
    
    def __init__(self, page):
        super().__init__(page)
        self.screenshot_dir = "reports/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def load(self):
        self.navigate(self.URL)
        self.screenshot_step("01_open_saucedemo")
    
    def add_sauce_labs_backpack_to_cart(self):
        self.wait_for_element(self.SAUCE_LABS_BACKPACK)
        self.click(self.SAUCE_LABS_BACKPACK)
        self.screenshot_step("02_add_backpack_to_cart")
    
    def is_backpack_added(self) -> bool:
        return self.is_visible(self.SAUCE_LABS_BACKPACK_REMOVE)
    
    def get_remove_button_text(self) -> str:
        return self.get_text(self.SAUCE_LABS_BACKPACK_REMOVE)
    
    def go_to_cart(self):
        self.click(self.SHOPPING_CART_ICON)
        self.screenshot_step("03_go_to_cart")
    
    def is_cart_item_visible(self) -> bool:
        return self.is_visible(self.CART_ITEM)
    
    def get_cart_item_name(self) -> str:
        return self.get_text(self.CART_ITEM_NAME)
    
    def get_cart_item_quantity(self) -> str:
        return self.get_text(self.CART_ITEM_QUANTITY)
    
    def screenshot_step(self, step_name: str):
        screenshot_path = f"{self.screenshot_dir}/{step_name}.png"
        self.screenshot(screenshot_path)