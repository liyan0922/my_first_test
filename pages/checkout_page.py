from .base_page import BasePage
import os


class CheckoutPage(BasePage):
    # 结账页面元素
    CHECKOUT_BUTTON = "[data-test='checkout']"
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    FINISH_BUTTON = "[data-test='finish']"
    ORDER_CONFIRMATION = "[data-test='complete-header']"
    ITEM_NAME = ".inventory_item_name"
    
    def __init__(self, page):
        super().__init__(page)
        self.screenshot_dir = "reports/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def click_checkout(self):
        self.wait_for_element(self.CHECKOUT_BUTTON)
        self.click(self.CHECKOUT_BUTTON)
        self.screenshot_step("04_click_checkout")
    
    def fill_checkout_information(self, first_name, last_name, postal_code):
        self.wait_for_element(self.FIRST_NAME_INPUT)
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        self.screenshot_step("05_fill_checkout_info")
    
    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)
        self.screenshot_step("06_click_continue")
    
    def get_item_name(self):
        return self.get_text(self.ITEM_NAME)
    
    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        self.screenshot_step("07_click_finish")
    
    def get_order_confirmation(self):
        return self.get_text(self.ORDER_CONFIRMATION)
    
    def screenshot_step(self, step_name: str):
        screenshot_path = f"{self.screenshot_dir}/{step_name}.png"
        self.screenshot(screenshot_path)