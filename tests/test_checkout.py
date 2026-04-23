import pytest
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(scope="function")
def setup_checkout(page):
    """设置测试环境：登录并添加商品到购物车"""
    login_page = LoginPage(page)
    cart_page = CartPage(page)
    
    # 登录
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    
    # 添加商品到购物车
    cart_page.add_sauce_labs_backpack_to_cart()
    assert cart_page.is_backpack_added(), "商品未成功添加到购物车"
    
    # 进入购物车页面
    cart_page.go_to_cart()
    assert cart_page.is_cart_item_visible(), "购物车页面未显示商品"
    assert cart_page.get_cart_item_name() == "Sauce Labs Backpack", "购物车中的商品名称不正确"
    
    yield page


def test_checkout_flow(setup_checkout):
    """测试结账流程"""
    page = setup_checkout
    checkout_page = CheckoutPage(page)
    
    # 点击Checkout按钮
    checkout_page.click_checkout()
    
    # 填写结账信息
    checkout_page.fill_checkout_information("Test", "User", "12345")
    
    # 点击Continue按钮
    checkout_page.click_continue()
    
    # 验证商品名称
    assert checkout_page.get_item_name() == "Sauce Labs Backpack", "概览页面商品名称不正确"
    
    # 点击Finish按钮
    checkout_page.click_finish()
    
    # 验证订单完成
    assert checkout_page.get_order_confirmation() == "Thank you for your order!", "订单未成功完成"
