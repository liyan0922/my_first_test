import pytest
from pages.login_page import LoginPage
from utils.screenshot_compare import ScreenshotComparator

class TestGenerateBaseline:
    """生成基准截图（只运行一次）"""
    
    @pytest.fixture
    def comparator(self):
        return ScreenshotComparator()

    def test_generate_login_baseline(self, page, comparator):
        """
        生成登录页面的基准截图
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        page.wait_for_load_state("networkidle")
        comparator.save_baseline(page, "login_page")
        print("✅ 登录页面基准截图生成成功")

    def test_generate_inventory_baseline(self, page, comparator):
        """
        生成商品列表页面的基准截图
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login("standard_user", "secret_sauce")
        page.wait_for_load_state("networkidle")
        comparator.save_baseline(page, "inventory_page")
        print("✅ 商品列表页面基准截图生成成功")

    def test_generate_cart_baseline(self, page, comparator):
        """
        生成购物车页面的基准截图
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login("standard_user", "secret_sauce")
        page.wait_for_load_state("networkidle")
        page.click('.inventory_item_name')
        page.click('[data-test="add-to-cart"]')
        page.click('.shopping_cart_link')
        page.wait_for_load_state("networkidle")
        comparator.save_baseline(page, "cart_page")
        print("✅ 购物车页面基准截图生成成功")