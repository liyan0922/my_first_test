import html
import pdb
from socket import timeout
from playwright.sync_api import Page
import pytest
import allure

from pages.login_page import LoginPage
from pages.item_detail_page import ItemsDetailPage



@allure.feature("商品详情页")
class TestItemDetail:
    """
    商品详情页的测试用例
    """

    @allure.story("查看商品详情")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_view_item_detail(self,page):
        """
        测试：登录后点击商品能进入详情页，并验证商品信息
        """

        with allure.step("步骤1：登录网站"):
            #Arrange : 登录
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")

        with allure.step("步骤2：进入商品详情页"):
            #Act : 点击商品
            page.wait_for_selector(".inventory_item_name",timeout=10000)
            page.click(".inventory_item_name")

        with allure.step("步骤3：验证详情页内容"):
            #Assert : 验证商品详情页是否显示
            detail_page = ItemsDetailPage(page)

            #验证页面有商品名称且步为空
            item_name = detail_page.get_item_name
            assert item_name,"商品名称不应该为空"

            #验证添加按钮存在
            add_to_cart_button = detail_page.get_add_to_cart_btn
            assert add_to_cart_button,"添加按钮不存在"

            print(f"✅测试通过，商品名称为：{item_name}")

    
    @allure.story("添加商品到购物车")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_add_item_to_cart_from_detail(self,page):
        """
        测试：在详情页点击Add to cart，验证商品被添加到购物车
        """
        with allure.step("步骤1：登录并进入详情页"):
            #Arrange(准备)
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")
            page.wait_for_selector(".inventory_item_name")
            page.click(".inventory_item_name")
        
        with allure.step("步骤2：点击添加按钮"):
            detail_page = ItemsDetailPage(page)
            #Act(操作)
            page.click(detail_page.add_to_cart_btn)

        
        with allure.step("步骤3：验证添加结果"):
            #Assert(验证),按钮从Add to cart到Remove from cart
            assert detail_page.remove_btn

            #验证购物车徽章显示数量为1
            cat_badge = page.locator(".shopping_cart_badge")
            assert cat_badge.is_visible(), "购物车徽章没有出现"
            assert cat_badge.text_content() == "1", "购物车数量不是1"

    
    @allure.story("移除商品从购物车")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_remove_item_from_cart_in_detail(self,page):
        """
        测试：添加商品后点击Remove，验证商品被移除
        """
        with allure.step("步骤1：登录并进入详情页"):
            #Arrange(准备)
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")


        with allure.step("步骤2：进入详情页并添加商品"):
            page.wait_for_selector(".inventory_item_name")
            page.click(".inventory_item_name")
            page.pause()
            detail_page = ItemsDetailPage(page)
            page.click(detail_page.add_to_cart_btn)
        
        with allure.step("步骤3：点击移除按钮"):
            #Act(执行)
            page.click(detail_page.remove_btn)
        
        with allure.step("步骤4：验证移除结果"):
            #Assert(验证)
            #验证按钮从Remove 到Add to cart
            assert page.locator(detail_page.add_to_cart_btn).is_visible()

            #验证购物车徽章消失
            cart_badge = page.locator(".shopping_cart_badge")
            assert cart_badge.is_visible() == False

    @allure.story("返回商品列表页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_back_to_products(self,page):
        """
        测试：点击Back to products，验证返回商品列表页
        """
        with allure.step("步骤1：登录并进入详情页"):
            #Arrange(准备)
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")
            page.wait_for_selector(".inventory_item_name")
            page.click(".inventory_item_name")
        
        with allure.step("步骤2：验证进入商品列表页"):
            detail_page = ItemsDetailPage(page)
            #Act(操作)
            page.click(detail_page.back_to_products_btn)
            #Assert(验证)
            #验证返回商品列表页
            assert "inventory.html" in page.url

        with allure.step("步骤3：验证商品列表页商品存在"):
            page.wait_for_selector(".inventory_item_name",timeout=10000)
            assert page.is_visible(".inventory_item_name"),"商品列表页商品不存在"





