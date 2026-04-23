import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.cart_page import CartPage


class TestCart:
    
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
    
    def test_add_sauce_labs_backpack_to_cart(self, page: Page):
        # 1. 在商品列表页找到名为"Sauce Labs Backpack"的商品
        # 2. 点击该商品下方的"Add to cart" 按钮
        self.cart_page.add_sauce_labs_backpack_to_cart()
        
        # 3. 验证按钮文字变为"Remove"（表示添加成功）
        assert self.cart_page.is_backpack_added(), "Remove button should be visible after adding to cart"
        remove_button_text = self.cart_page.get_remove_button_text()
        assert remove_button_text == "Remove", f"Expected 'Remove' button text, got: {remove_button_text}"
        
        # 4. 点击页面右上角的购物车图标（🛒）
        self.cart_page.go_to_cart()
        
        # 5. 在购物车页面，验证商品名称包含 "Sauce Labs Backpack"
        assert self.cart_page.is_cart_item_visible(), "Cart item should be visible"
        cart_item_name = self.cart_page.get_cart_item_name()
        assert "Sauce Labs Backpack" in cart_item_name, f"Expected 'Sauce Labs Backpack' in cart item name, got: {cart_item_name}"
        
        # 6. 验证商品数量为1
        cart_item_quantity = self.cart_page.get_cart_item_quantity()
        assert cart_item_quantity == "1", f"Expected quantity '1', got: {cart_item_quantity}"
        
        # 截图保存最终结果
        page.screenshot(path="reports/screenshots/04_cart_verification.png")