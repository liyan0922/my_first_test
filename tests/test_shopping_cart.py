import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.cart_page import CartPage


class TestShoppingCart:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)
        self.cart_page = CartPage(page)
        
        # 先登录成功
        self.login_page.load()
        self.login_page.enter_username("standard_user")
        self.login_page.enter_password("secret_sauce")
        self.login_page.click_login_button()
        
        # 验证登录成功
        assert "inventory.html" in page.url, f"Expected 'inventory.html' in URL, got: {page.url}"
    
    def test_add_to_cart(self, page: Page):
        # 测试添加商品到购物车
        self.cart_page.add_sauce_labs_backpack_to_cart()
        
        # 验证商品已添加
        assert self.cart_page.is_backpack_added(), "Remove button should be visible after adding to cart"
        remove_button_text = self.cart_page.get_remove_button_text()
        assert remove_button_text == "Remove", f"Expected 'Remove' button text, got: {remove_button_text}"
        
        # 进入购物车
        self.cart_page.go_to_cart()
        
        # 验证购物车中有商品
        assert self.cart_page.is_cart_item_visible(), "Cart item should be visible"
        cart_item_name = self.cart_page.get_cart_item_name()
        assert "Sauce Labs Backpack" in cart_item_name, f"Expected 'Sauce Labs Backpack' in cart item name, got: {cart_item_name}"
        
        # 验证商品数量
        cart_item_quantity = self.cart_page.get_cart_item_quantity()
        assert cart_item_quantity == "1", f"Expected quantity '1', got: {cart_item_quantity}"
        
        # 截图保存
        page.screenshot(path="reports/screenshots/saucedemo_cart_screenshot.png")