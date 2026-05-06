from playwright.sync_api import Page

class ItemsDetailPage:
    """
    商品详情页的Object Page
   """ 
    def __init__(self,page:Page):
        self.page = page

        #定位器
        self.item_name ='[data-test="inventory_item_name"] '
        self.item_desc = '[data-test="inventory_item_desc"] '
        self.item_price = '[data-test="inventory_item_price"] '
        self.add_to_cart_btn = '[data-test="add-to-cart"] '
        self.back_to_products_btn = '[data-test="back-to-products"] '
        self.remove_btn = '[data-test="remove"] '

    def get_item_name(self) -> str|None:
        """
        获取商品名称
        """
        return self.page.text_content(self.item_name)

    def get_item_desc(self) -> str|None:
        """
        获取商品描述
        """
        return self.page.text_content(self.item_desc)

    def get_item_price(self) -> str|None:
        """
        获取商品价格
        """
        return self.page.text_content(self.item_price)

    def get_add_to_cart_btn(self) -> str|None:
        """
        获取添加到购物车按钮文本
        """
        return self.page.text_content(self.add_to_cart_btn)

    def get_back_to_products_btn(self) -> str|None:
        """
        获取返回商品列表按钮文本
        """
        return self.page.text_content(self.back_to_products_btn)


    def get_remove_btn(self) -> str|None:
        """
        获取从购物车移除按钮文本
        """
        return self.page.text_content(self.remove_btn)
        
