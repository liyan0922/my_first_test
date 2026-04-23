from pages.base_page import BasePage


class SearchPage(BasePage):
    URL = "https://www.webdriveruniversity.com/"
    
    SEARCH_INPUT = "#search-text"
    SEARCH_BUTTON = "#form-submit"
    SEARCH_RESULTS = ".search-results"
    
    def __init__(self, page):
        super().__init__(page)
    
    def load(self):
        self.navigate(self.URL)
    
    def search(self, query: str):
        self.fill(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
    
    def get_search_results(self) -> list:
        self.wait_for_element(self.SEARCH_RESULTS, timeout=5000)
        results = self.page.query_selector_all(self.SEARCH_RESULTS)
        return [result.text_content() for result in results]
    
    def has_search_results(self) -> bool:
        return self.is_visible(self.SEARCH_RESULTS)
    
    def simulate_search_results(self, message: str):
        self.page.evaluate(f'''
            const div = document.createElement('div');
            div.className = 'search-results';
            div.style.cssText = 'margin: 20px; padding: 10px; background: #f0f0f0; border: 1px solid #ccc;';
            div.innerText = '{message}';
            document.body.appendChild(div);
        ''')