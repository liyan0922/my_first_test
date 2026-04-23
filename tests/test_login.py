import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage


class TestLogin:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)
        self.login_page.load()
    
    def test_login_with_valid_credentials(self, page: Page):
        username = "standard_user"
        password = "secret_sauce"
        
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        
        self.login_page.click_login_button()
        
        self.login_page.wait_for_alert()
        
        page.screenshot(path="reports/screenshots/05_after_alert.png")
        
        # 验证登录成功，应该跳转到inventory.html页面
        assert "inventory.html" in page.url, f"Expected 'inventory.html' in URL, got: {page.url}"
    
    def test_login_with_invalid_credentials(self, page: Page):
        username = "testuser"
        password = "123456"
        
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        
        self.login_page.click_login_button()
        
        self.login_page.wait_for_alert()
        
        page.screenshot(path="reports/screenshots/05_after_alert_invalid.png")
        
        # 验证错误信息显示
        assert self.login_page.is_error_visible(), "Error message should be visible"
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Error message should not be None"
        assert "Username and password do not match any user in this service" in error_message, f"Expected error message to contain 'Username and password do not match any user in this service', got: {error_message}"
    
    def test_login_with_empty_credentials(self, page: Page):
        username = ""
        password = ""
        
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        
        self.login_page.click_login_button()
        
        self.login_page.wait_for_alert()
        
        page.screenshot(path="reports/screenshots/05_empty_credentials_alert.png")
        
        # 验证错误信息显示
        assert self.login_page.is_error_visible(), "Error message should be visible"
        error_message = self.login_page.get_error_message()
        assert error_message is not None, "Error message should not be None"
        assert "Username is required" in error_message, f"Expected error message to contain 'Username is required', got: {error_message}"
    
    def test_login_page_elements_visible(self):
        assert self.login_page.is_visible(LoginPage.USERNAME_INPUT), "Username input should be visible"
        assert self.login_page.is_visible(LoginPage.PASSWORD_INPUT), "Password input should be visible"
        assert self.login_page.is_visible(LoginPage.LOGIN_BUTTON), "Login button should be visible"