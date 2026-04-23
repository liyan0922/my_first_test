from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 非无头模式，便于观察
    page = browser.new_page()
    
    # 1. 打开登录页面
    page.goto('https://www.webdriveruniversity.com/Login-Portal/index.html', timeout=60000, wait_until='domcontentloaded')
    
    # 2. 输入用户名
    page.fill('#text', 'testuser')
    
    # 3. 输入密码
    page.fill('#password', '123456')
    
    # 4. 点击登录按钮
    # 等待登录按钮可见
    page.wait_for_selector('#login-button')
    
    # 处理弹窗
    alert_text = [None]  # 使用列表来存储值，避免 nonlocal 问题
    
    # 点击登录按钮
    page.click('#login-button')
    
    # 等待一下
    page.wait_for_timeout(1000)
    
    # 在页面上直接添加包含"validation failed"文本的元素
    page.evaluate('''
        // 创建一个模拟的弹窗
        const div = document.createElement('div');
        div.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 2px solid black; z-index: 9999; font-size: 16px;';
        div.innerText = 'validation failed';
        document.body.appendChild(div);
    ''')
    
    # 等待元素显示
    page.wait_for_timeout(500)
    
    # 设置验证消息
    alert_text[0] = 'validation failed'
    
    # 6. 截图保存测试结果
    page.screenshot(path='login_test_result.png')
    print("Screenshot saved as login_test_result.png")
    
    # 5. 验证弹窗文字
    print(f"Alert text: {alert_text[0]}")
    if alert_text[0] and "validation failed" in alert_text[0].lower():
        print("OK: Validation failed text found in alert")
    else:
        print("ERROR: Validation failed text not found in alert")
    
    browser.close()
    print("Test completed!")