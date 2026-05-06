import pytest
from playwright.sync_api import Page
from pages import login_page
from pages.login_page import LoginPage


class TestLogin:

    """
    数据驱动测试示例
    """
    @pytest.mark.parametrize("username, password", [
        ("standard_user", "secret_sauce"),      # 标准用户
        ("problem_user", "secret_sauce"),       # 有问题的用户
        ("performance_glitch_user", "secret_sauce"),  # 性能问题用户
        ("error_user", "secret_sauce"),         # 错误用户
        ("visual_user", "secret_sauce"),        # 视觉用户
    ])

    def test_login_with_multiple_users(self,page,username,password):
        """
        测试多个用户都能成功登录
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login(username,password)

        # 验证登录成功，应该跳转到inventory.html页面
        assert "inventory.html" in page.url, f"用户 {username} 登录失败"

        #退出登录，为下一个测试做准备
        page.click("button#react-burger-menu-btn")
        page.click("#logout_sidebar_link")


    
    @pytest.mark.parametrize("username,password,expected_error",[
        ("locked_out_user", "secret_sauce", "locked out"),  # 被锁定的用户
        ("standard_user", "wrong_password", "password"),    # 错误密码
        ("", "secret_sauce", "username"),                  # 空用户名
        ("standard_user", "", "password"),                 # 空密码
    ])
    def test_login_failure_scenarios(self,page,username,password,expected_error):
        """
        测试各种登录失败场景
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login(username,password)
        
        # 验证错误消息包含预期关键字
        error_message = page.locator('[data-test="error"]').text_content()
        assert expected_error.lower() in error_message.lower(),\
            f"期望错误包含'{expected_error}',实际为'{error_message}'"
    
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