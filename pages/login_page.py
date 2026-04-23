from .base_page import BasePage
import os


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page):
        super().__init__(page)
        self.screenshot_dir = "reports/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.alert_text = None
    
    def load(self):
        self.navigate(self.URL)
        self.screenshot_step("01_open_login_page")
    
    def enter_username(self, username: str):
        self.fill(self.USERNAME_INPUT, username)
        self.screenshot_step("02_enter_username")
    
    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)
        self.screenshot_step("03_enter_password")
    
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
        self.screenshot_step("04_click_login_button")
    
    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self) -> str:
        self.wait_for_element(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
    
    def handle_alert(self):
        pass  # saucedemo.com 不使用alert
    
    def get_alert_text(self) -> str:
        return None  # saucedemo.com 不使用alert
    
    def screenshot_step(self, step_name: str):
        screenshot_path = f"{self.screenshot_dir}/{step_name}.png"
        self.screenshot(screenshot_path)
    
    def wait_for_alert(self, timeout: int = 2000):
        self.page.wait_for_timeout(timeout)