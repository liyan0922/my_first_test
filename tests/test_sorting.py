import allure
from playwright.sync_api import Page
import pytest
from pages import LoginPage, login_page
from pages.inventory_page import InventoryPage

@allure.feature("商品排序功能")
class TestProductSorting:
        """商品排序功能的数据驱动测试"""
        @pytest.mark.parametrize("sort_option,expected_order", [
            pytest.param("az", "is_sorted_by_name_ascending",id = "按名称正序"),
            pytest.param("za", "is_sorted_by_name_descending",id = "按名称倒序"),
            pytest.param("lohi", "is_sorted_by_price_ascending",id = "按价格低到高排序"),
            pytest.param("hilo", "is_sorted_by_price_descending",id = "按价格高到低排序"),
            ])
        
        @allure.story("排序功能验证")
        def test_sorting(self, page: Page, sort_option: str, expected_order: str):
            # 测试商品列表的排序功能
            # Arrange - 准备
            with allure.step("登录网站"):
                login_page = LoginPage(page)
                login_page.navigate(login_page.URL)
                login_page.login("standard_user", "secret_sauce")

            with allure.step("进入商品列表页"):
                inventory_page = InventoryPage(page)
                
            with allure.step(f'执行排序操作：{sort_option}'):
                inventory_page.sort_by(sort_option)

            with allure.step(f'验证排序结果：{expected_order}'):
                # 动态调用对应的验证方法
                check_method = getattr(inventory_page, expected_order)
                assert check_method(), f"排序 {sort_option} 后，顺序不正确"

        @pytest.mark.parametrize("sort_option,expected_order", [
            ("az", ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt", 
                "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)"]),
            ("za", ["Test.allTheThings() T-Shirt (Red)", "Sauce Labs Onesie", "Sauce Labs Fleece Jacket",
                "Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light", "Sauce Labs Backpack"]),
            ])
        @allure.story("排序后商品名称验证")
        def test_sorting_expected_names(self, page: Page, sort_option: str, expected_order: list):
            """使用数据驱动验证排序后的具体商品顺序
        
        这个测试更具体，直接验证排序后的商品名称列表是否符合预期"""
            # Arrange - 准备
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")
            inventory_page = InventoryPage(page)

            # Act    
            inventory_page.sort_by(sort_option)
            actual_names = inventory_page.get_product_names()

            # Assert
            assert actual_names == expected_order, f"排序 {sort_option} 后，商品顺序与预期不符\n期望: {expected_order}\n实际: {actual_names}"
            

        @pytest.mark.parametrize("sort_option,expected_first_price,expected_last_price", [
            ("lohi", 7.99, 49.99),
            ("hilo", 49.99, 7.99),
            ])
        @allure.story("排序后商品价格验证")
        def test_sorting_price_range(self, page: Page, sort_option: str, expected_first_price: float, expected_last_price: float):
            """验证排序后的价格符合预期范围"""
            # Arrange - 准备
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")
            inventory_page = InventoryPage(page)
            # Act    
            inventory_page.sort_by(sort_option)
            prices = inventory_page.get_product_prices()
            # Assert
            assert prices[0] == expected_first_price, f"第一个商品价格应为 {expected_first_price}，实际为 {prices[0]}"
            assert prices[-1] == expected_last_price, f"最后一个商品价格应为 {expected_last_price}，实际为 {prices[-1]}"
        
        @allure.story("购物车操作不影响排序")
        def test_sorting_unchanged_after_add_to_cart(self, page: Page):
            """验证：添加商品到购物车后，商品列表的排序不受影响"""
            # Arrange - 准备
            login_page = LoginPage(page)
            login_page.navigate(login_page.URL)
            login_page.login("standard_user", "secret_sauce")
            inventory_page = InventoryPage(page)

            # 默认排序是名称 A-Z，记录添加前的商品名称列表
            before_names = inventory_page.get_product_names()

            # Act - 操作：随机添加第一个商品到购物车
            first_product_name = before_names[0]
            inventory_page.add_to_cart(first_product_name)

            # Assert - 验证添加后，商品名称列表是否保持不变
            after_names = inventory_page.get_product_names()
            assert after_names == before_names, f"添加商品 {first_product_name} 后，商品列表排序被改变"

            
            

