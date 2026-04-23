import pytest
from playwright.sync_api import Page
from pages.cart_page import CartPage


class TestCart:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.cart_page = CartPage(page)
        self.cart_page.load()
    
    def test_cart_page_loads(self):
        assert self.cart_page.page.url == CartPage.URL
    
    def test_cart_page_title(self):
        title = self.cart_page.page.title()
        assert title is not None
        assert len(title) > 0
    
    def test_cart_page_navigation(self):
        self.cart_page.navigate("https://www.webdriveruniversity.com/")
        assert "webdriveruniversity.com" in self.cart_page.page.url
    
    def test_cart_initial_state(self):
        assert self.cart_page.is_cart_empty()