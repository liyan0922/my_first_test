import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage


class TestLogin:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)
        self.login_page.load()
    
    def test_login_with_invalid_credentials(self, page: Page):
        username = "testuser"
        password = "123456"
        
        self.login_page.login(username, password)
        page.wait_for_timeout(1000)
        
        self.login_page.simulate_alert("validation failed")
        page.wait_for_timeout(500)
        
        alert_text = self.login_page.get_alert_text()
        
        assert alert_text == "validation failed"
        assert "validation failed" in alert_text.lower()
    
    def test_login_with_empty_credentials(self, page: Page):
        username = ""
        password = ""
        
        self.login_page.login(username, password)
        page.wait_for_timeout(1000)
        
        self.login_page.simulate_alert("validation failed")
        page.wait_for_timeout(500)
        
        alert_text = self.login_page.get_alert_text()
        
        assert alert_text == "validation failed"
    
    def test_login_page_elements_visible(self):
        assert self.login_page.is_visible(LoginPage.USERNAME_INPUT)
        assert self.login_page.is_visible(LoginPage.PASSWORD_INPUT)
        assert self.login_page.is_visible(LoginPage.LOGIN_BUTTON)