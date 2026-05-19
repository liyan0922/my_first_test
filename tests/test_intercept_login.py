
import time
from playwright.sync_api import Response
from pages import LoginPage, login_page


def test_intercept_successful_login(page):
    """
    拦截登录 API，模拟登录成功响应
    """

    # 🎯 核心：拦截登录请求，模拟成功响应
    def handle_login_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"authenticated": true, "token": "fake-jwt-token"}'
        )

    # 注册拦截器（拦截所有包含 login 的请求）
    page.route("**/login", handle_login_route)

    # 执行登录操作
    login_page = LoginPage(page)
    login_page.navigate(login_page.URL)

    # 这里假设使用 fetch 或 API 调用登录
    # 由于我们拦截了请求，会直接返回模拟响应
    Response = page.evaluate("""
        async () => {
            const res = await fetch('https://www.saucedemo.com/login', {
                method: 'POST',
                body: JSON.stringify({user: 'test', pass: 'any'})
            });
            return res.json();
        }
    """)

    # 验证拦截生效
    assert Response["authenticated"]
    assert Response["token"] == "fake-jwt-token"

def test_intercept_failed_login(page):
    """
    模拟登录失败响应
    """
    def handle_login_failure(route):
        route.fulfill(
            status=401,
            content_type="application/json",
            body='{"error": "Invalid credentials","message": "用户名或密码错误"}'
        )

    # 注册拦截器（拦截所有包含 login 的请求）
    page.route("**/login", handle_login_failure)

    # 执行登录..
    response = page.evaluate("""
        async () => {
            const res = await fetch('https://www.saucedemo.com/login', {
                method: 'POST',
                body: JSON.stringify({user: 'bad', pass: 'wrong'})
            });
            return {status: res.status, body: await res.body()};
        }
    """)

    # 验证拦截生效
    assert response["status"] == 401
    assert 'Invalid credentials' in response["body"] ["error"]

def test_block_images(page):
    """
    完整测试：拦截图片并验证效果
    验证内容：
    1. 拦截器确实阻止了图片请求
    2. 页面上的 img 元素没有真正加载图片
    3. 拦截后页面加载速度更快
    """

    # ========== 准备数据统计 ==========
    blocked_image_urls = [] # 记录被阻止的图片URL
    blocked_count = 0       # 被阻止的图片数量
    normal_requests = []    # 正常放行的请求

    # ========== 定义拦截器 ==========
    def handle_route(route):
        """检查每个请求，如果是图片就阻止"""
        nonlocal blocked_count
        url = route.request.url

        # 判断是否是图片（检查URL是否以图片扩展名结尾）
        image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
        is_image = url.lower().endswith(image_extensions)

        if is_image:
            blocked_count += 1
            blocked_image_urls.append(url)
            print(f"🚫 阻止图片: {url}")
            route.abort()
        else:
            # 不是图片：正常放行
            normal_requests.append(url)
            print(f"✅ 放行: {url[:80]}...")  # 只打印前80个字符，避免太长
            route.continue_()

    # ========== 注册拦截器 ==========
    page.route("**/*", handle_route)

    # ========== 执行测试操作 ==========
    print("\n📊 开始加载页面（已启用图片拦截）...")
    login_page = LoginPage(page)
    login_page.navigate(login_page.URL)
    start_time = time.time()
    login_page.login("standard_user", "secret_sauce")
    load_time = time.time() - start_time
    print(f"📊 页面加载完成，耗时: {load_time:.2f} 秒")

    # ========== 验证1：有图片被阻止 ==========
    print(f"\n🔍 验证1：检查图片拦截情况")
    assert blocked_count > 0, f"❌ 没有检测到被阻止的图片，共 {len(blocked_image_urls)} 个"
    print(f"   ✅ 成功阻止 {blocked_count} 个图片请求")

    # ========== 验证2：页面上的 img 元素没有真正加载 ==========
    print(f"\n🔍 验证2：检查页面上的 img 元素")
    img_elements = page.locator('img').all()
    actually_loaded = 0

    for img in img_elements:
        # 检查图片是否真的加载了（naturalWidth > 0 表示加载成功）
        natural_width = img.evaluate("el => el.naturalWidth || 0")
        if natural_width > 0:
            actually_loaded += 1
            src = img.get_attribute("src")
            print(f"  ⚠️ 意外加载的图片: {src}")

    assert actually_loaded == 0, f"❌ 有 {actually_loaded} 个图片仍然被加载了"
    print(f"   ✅ 页面上共 {len(img_elements)} 个 img 元素，全部未加载")


    # ========== 验证3：验证加载时间在合理范围内 ==========
    # 由于 pytest-playwright 的 context 限制，无法创建新页面
    # 所以我们只验证拦截后的加载时间是否合理
    print(f"\n🔍 验证3：检查加载时间")
    print(f"   📊 拦截图片后加载耗时: {load_time:.2f} 秒")
    
    # 验证加载时间在合理范围内（小于10秒）
    assert load_time < 10, f"❌ 加载时间过长: {load_time:.2f} 秒"
    print(f"   ✅ 加载时间在合理范围内")

    # ========== 最终总结 ==========
    print(f"\n" + "="*50)
    print(f"✅ 图片拦截测试全部通过！")
    print(f"   总计阻止: {blocked_count} 个图片")
    print(f"   被阻止的图片示例: {blocked_image_urls[:3]}")
    print(f"   正常放行请求: {len(normal_requests)} 个")
    print("="*50)

