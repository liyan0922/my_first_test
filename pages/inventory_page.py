
from typing import List
from playwright.sync_api import Page


class InventoryPage:
    """
    商品列表页的 Page Object
    """
    def __init__(self, page: Page):
        self.page = page

        #排序下拉框
        self.sort_dropdown = '[data-test="product-sort-container"]'

        # 商品元素
        self.product_names = '.inventory_item_name'
        self.product_prices = '.inventory_item_price'
        self.product_items = '.inventory_item'

        # 添加到购物车按钮（通过商品名称定位）
        def add_to_cart_button(self, product_name: str):
            return f'text="{product_name}" >> xpath=ancestor::div[@class="inventory_item"]//button[text()="Add to cart"]'

    def sort_by(self,option: str):
        """按指定选项排序
        Args:
            option (str): 'az', 'za', 'lohi', 'hilo'
        """
        self.page.select_option(self.sort_dropdown, option)
        # 等待排序完成（等待商品列表刷新）
        self.page.wait_for_selector(self.product_names)
    
    def get_product_names(self):
        """获取所有商品名称"""
        names = self.page.locator(self.product_names).all_text_contents()
        return [name.strip() for name in names]

    def get_product_prices(self) -> List[float]:
        """获取所有商品价格"""
        price_elements = self.page.locator(self.product_prices).all_text_contents()
        # 将 "$29.99" 转换为 29.99
        return [float(price.replace('$', '')) for price in price_elements]

    def get_all_products(self) -> List[dict]:
        """获取所有商品信息（名称+价格）"""
        names = self.get_product_names()
        prices = self.get_product_prices()
        return [{'name': name, 'price': price} for name, price in zip(names, prices)]

    def is_sorted_by_name_ascending(self) -> bool:
        """检查商品是否按名称升序排序"""
        names = self.get_product_names()
        return names == sorted(names)

    def is_sorted_by_name_descending(self) -> bool:
        """检查商品是否按名称降序排序"""
        names = self.get_product_names()
        return names == sorted(names, reverse=True)

    def is_sorted_by_price_ascending(self) -> bool:
        """检查商品是否按价格升序排序"""
        prices = self.get_product_prices()
        return prices == sorted(prices)

    def is_sorted_by_price_descending(self) -> bool:
        """检查商品是否按价格降序排序"""
        prices = self.get_product_prices()
        return prices == sorted(prices, reverse=True)

    def add_to_cart(self, product_name: str):
        """添加指定商品到购物车"""
        # 通过商品名称找到对应的添加按钮
        product_item = self.page.locator(f'.inventory_item:has-text({product_name})')
        add_button = product_item.locator('button')
        add_button.click()
