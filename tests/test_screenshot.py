import pytest
from playwright.sync_api import Page


class TestScreenshot:
    
    def test_take_screenshot(self, page: Page):
        # 打开网站
        page.goto("https://www.webdriveruniversity.com")
        
        # 等待页面加载完成
        page.wait_for_load_state("networkidle")
        
        # 截图并保存到当前目录
        screenshot_path = "webdriveruniversity_screenshot.png"
        page.screenshot(path=screenshot_path)
        
        print(f"Screenshot saved to: {screenshot_path}")
        
        # 验证截图文件是否存在
        import os
        assert os.path.exists(screenshot_path), f"Screenshot file {screenshot_path} not found"
