import pytest
from playwright.sync_api import Page
from pytest_html import extras


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def browser(browser_type_launch_args):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(**browser_type_launch_args)
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
                screenshot_name = f"reports/screenshots/{item.name}.png"
                page.screenshot(path=screenshot_name)
                report.extra = [
                    pytest_html.extras.image(screenshot_name, name="Screenshot on failure")
                ]
            except:
                pass