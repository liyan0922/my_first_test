import pytest
from playwright.sync_api import sync_playwright
from pytest_html import extras
import os

import pytest_html

def is_ci_environment():
    """检测是否在 CI 环境中运行（GitHub Actions、GitLab CI 等）"""
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture(scope="function")
def page(browser):
    """从 browser fixture 创建新页面"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
    


@pytest.fixture(scope="function")
def browser():
    """提供浏览器实例，CI 环境中强制 headless=True"""
    with sync_playwright() as p:
        # 根据环境选择 headless 模式
        headless = True if is_ci_environment() else False
        # 可选：你也可以保留其他 launch 参数，如 slow_mo（仅在本地调试时）
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def browser_type_launch_args(pytestconfig):
    launch_options = {}
    headless = pytestconfig.getoption("--headless")
    if headless:
        launch_options["headless"] = True
    else:
        launch_options["headless"] = False
    
    slow_mo = pytestconfig.getoption("--slow-mo")
    if slow_mo:
        launch_options["slow_mo"] = slow_mo
    
    return launch_options


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run tests in headless mode")
    parser.addoption("--slow-mo", type=int, default=None, help="Slow down actions by specified milliseconds")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if "page" in item.fixturenames:
            try:
                page = item.funcargs["page"]
                os.makedirs("reports/screenshots", exist_ok=True)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                screenshot_name = f"reports/screenshots/failure_{item.name}_{timestamp}.png"
                page.screenshot(path=screenshot_name)
                report.extra = [
                    extras.image(screenshot_name, name="Screenshot on failure")
                ]
            except:
                pass