import pytest
from pages.login_page import LoginPage
from utils.screenshot_compare import ScreenshotComparator
from pixelmatch import pixelmatch

class TestVisualRegression:
    """视觉回归测试"""

    @pytest.fixture
    def comparator(self):
        return ScreenshotComparator()
    
    def test_login_page_visual(self, comparator, page):
        """
        测试登录页面的视觉一致性
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        
        # 等待页面完全加载
        page.wait_for_load_state("networkidle")
        
        # 对比登录页截图
        is_match = comparator.compare(page, "login_page")
        if not is_match:
            pytest.fail("登录页面与基准截图不一致，请检查 UI 变化")

    def test_inventory_page_visual(self, comparator, page):
        """
        测试商品列表页面的视觉一致性
        """

        # 先登录
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login("standard_user", "secret_sauce")

        # 等待页面稳定
        page.wait_for_load_state("networkidle")

        # 对比商品页截图
        is_match = comparator.compare(page, "inventory_page")
        if not is_match:
            pytest.fail("商品页面与基准截图不一致，请检查 UI 变化")

    def test_cart_page_visual(self, comparator, page):
        """
        测试购物车页面的视觉一致性
        """
        # 登录并添加商品到购物车
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login("standard_user", "secret_sauce")

        # 添加第一个商品到购物车
        page.click('.inventory_item_name')
        page.click('[data-test="add-to-cart"]')
        page.click('.shopping_cart_link')

        page.wait_for_load_state("networkidle")

        is_match = comparator.compare(page, "cart_page")
        if not is_match:
            pytest.fail("购物车页面与基准截图不一致")
        
        