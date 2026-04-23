import pytest
from playwright.sync_api import Page
from pages.search_page import SearchPage


class TestSearch:
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.search_page = SearchPage(page)
        self.search_page.load()
    
    def test_search_page_loads(self):
        assert self.search_page.page.url == SearchPage.URL
    
    def test_search_page_title(self):
        title = self.search_page.page.title()
        assert title is not None
        assert len(title) > 0
    
    def test_search_page_navigation(self):
        self.search_page.navigate("https://www.webdriveruniversity.com/")
        assert "webdriveruniversity.com" in self.search_page.page.url