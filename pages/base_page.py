from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        self.page.goto(url)
    
    def click(self, selector: str):
        self.page.click(selector)
    
    def fill(self, selector: str, value: str):
        self.page.fill(selector, value)
    
    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)
    
    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def screenshot(self, path: str):
        self.page.screenshot(path=path)