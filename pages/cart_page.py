from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.webdriveruniversity.com/"
    
    ADD_TO_CART_BUTTON = ".btn-add-cart"
    CART_ICON = ".cart-icon"
    CART_ITEMS = ".cart-item"
    CART_TOTAL = ".cart-total"
    
    def __init__(self, page):
        super().__init__(page)
    
    def load(self):
        self.navigate(self.URL)
    
    def add_to_cart(self, product_selector: str):
        self.click(product_selector)
    
    def open_cart(self):
        self.click(self.CART_ICON)
    
    def get_cart_items_count(self) -> int:
        try:
            items = self.page.query_selector_all(self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def get_cart_total(self) -> str:
        return self.get_text(self.CART_TOTAL)
    
    def is_cart_empty(self) -> bool:
        return self.get_cart_items_count() == 0
    
    def simulate_products(self):
        self.page.evaluate('''
            const products = document.createElement('div');
            products.innerHTML = `
                <div class="product-1" style="margin: 20px; padding: 10px; border: 1px solid #ccc;">
                    <h3>Product 1</h3>
                    <button class="btn-add-cart" style="padding: 5px 10px;">Add to Cart</button>
                </div>
                <div class="product-2" style="margin: 20px; padding: 10px; border: 1px solid #ccc;">
                    <h3>Product 2</h3>
                    <button class="btn-add-cart" style="padding: 5px 10px;">Add to Cart</button>
                </div>
            `;
            document.body.appendChild(products);
        ''')
    
    def simulate_cart_update(self, count: int):
        self.page.evaluate(f'''
            const cart = document.createElement('div');
            cart.className = 'cart-items';
            cart.style.cssText = 'margin: 20px; padding: 10px; background: #e8f5e9; border: 1px solid #4caf50;';
            cart.innerText = 'Cart contains {count} item(s)';
            document.body.appendChild(cart);
        ''')
    
    def simulate_cart_total(self, total: str):
        self.page.evaluate(f'''
            const totalDiv = document.createElement('div');
            totalDiv.className = 'cart-total';
            totalDiv.style.cssText = 'margin: 20px; padding: 10px; background: #fff3e0; border: 1px solid #ff9800; font-weight: bold;';
            totalDiv.innerText = 'Total: {total}';
            document.body.appendChild(totalDiv);
        ''')