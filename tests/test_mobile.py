import pytest
from pages.login_page import LoginPage

class TestMobileView:
    """移动端模拟测试"""
    @pytest.mark.parametrize("device",[
        "iphone 12",
        "iphone SE",
        "ipad",
        "Pixel 5"
    ])
    def test_mobile_login(self,page,device):
        """
        在不同移动设备上测试登录功能
        """
        # 设置设备视口（简化版，先手动设置尺寸）
        if device == "iphone 12":
            page.set_viewport_size({"width": 390, "height": 844})
        elif device == "iphone SE":
            page.set_viewport_size({"width": 375, "height": 667})
        elif device == "ipad":
            page.set_viewport_size({"width": 768, "height": 1024})
        elif device == "Pixel 5":
            page.set_viewport_size({"width": 393, "height": 851})

        # 执行登录测试
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login("standard_user", "secret_sauce")

        # 验证登录成功
        assert "inventory.html" in page.url, f"{device} 登录失败"
        # 可选：截图保存
        page.screenshot(path=f"reports/screenshots/{device}.png")
        print(f"✅ {device} 测试通过 (视口: {page.viewport_size})")


    def test_touch_actions(self,page):
        """
        测试触摸屏操作
        """
        page.set_viewport_size({"width": 375, "height": 667})

        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)

        # 模拟触摸点击（使用 click 代替 tap，功能类似）
        page.click('[data-test="username"]')
        page.keyboard.type("standard_user")

        page.click('[data-test="password"]')
        page.keyboard.type("secret_sauce")

        page.click('[data-test="login-button"]')

        # 验证登录成功
        assert "inventory.html" in page.url, "登录失败"
        # 可选：截图保存
        page.screenshot(path="reports/screenshots/mobile_login.png")
        print("✅ 移动端登录测试通过")

        

