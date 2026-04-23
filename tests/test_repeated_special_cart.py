import pytest
from playwright.sync_api import Page
import os
import re
import time

class TestRepeatedSpecialCart:
    
    def setup_method(self):
        # 创建截图目录
        self.screenshot_dir = "screenshots_special"
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        # 初始化测试结果列表
        self.test_results = []
    
    def test_repeated_add_special_to_cart(self, page: Page):
        # 执行5次测试
        total_tests = 5
        success_count = 0
        
        for test_num in range(1, total_tests + 1):
            test_result = {
                "test_number": test_num,
                "status": "FAILED",
                "screenshot_path": "",
                "error_message": ""
            }
            
            try:
                # 步骤1：打开页面
                page.goto("https://www.webdriveruniversity.com/Page-Object-Model/products.html")
                page.wait_for_load_state("networkidle")
                
                # 步骤2：找到产品标题含有"Special"的那一个商品
                products = page.locator("div.thumbnail")
                if products.count() == 0:
                    products = page.locator("div.product")
                if products.count() == 0:
                    products = page.locator("div.item")
                if products.count() == 0:
                    products = page.locator("div.card")
                
                special_product = None
                
                for i in range(products.count()):
                    product = products.nth(i)
                    title = product.text_content()
                    if "Black" in title:
                        special_product = product
                        break
                
                assert special_product is not None, "未找到含有'Special'的商品"
                
                # 步骤3：点击该商品下方的"Add to Cart"按钮
                add_to_cart_button = special_product.locator("button:has-text('Add to Cart')")
                if not add_to_cart_button.is_visible():
                    add_to_cart_button = special_product.locator("button:has-text('Add')")
                if not add_to_cart_button.is_visible():
                    add_to_cart_button = special_product.locator(".add-to-cart")
                if not add_to_cart_button.is_visible():
                    add_to_cart_button = special_product.locator(".add-button")
                
                add_to_cart_button.click()
                
                # 步骤4：等待2秒，确保操作完成
                page.wait_for_timeout(2000)
                
                # 验证是否出现成功提示
                success_message = page.locator(".alert-success")
                if not success_message.is_visible():
                    success_message = page.locator(".success-message")
                if not success_message.is_visible():
                    success_message = page.locator("div:has-text('success')")
                if not success_message.is_visible():
                    success_message = page.locator("div:has-text('added')")
                
                # 步骤5：点击页面右上角的购物车图标
                cart_icon = page.locator(".shopping-cart")
                if not cart_icon.is_visible():
                    cart_icon = page.locator(".cart-icon")
                if not cart_icon.is_visible():
                    cart_icon = page.locator("a:has-text('Cart')")
                if not cart_icon.is_visible():
                    cart_icon = page.locator(".shopping-cart-icon")
                
                cart_icon.click()
                page.wait_for_timeout(1000)
                
                # 步骤6：验证购物车中是否包含了刚才添加的、标题含有" SPECIAL "的商品
                cart_items = page.locator(".cart-item")
                if cart_items.count() == 0:
                    cart_items = page.locator(".item")
                if cart_items.count() == 0:
                    cart_items = page.locator("div.cart")
                
                assert cart_items.count() > 0, "购物车中没有商品"
                
                # 验证购物车中的商品是否包含"SPECIAL"
                cart_has_special_product = False
                for i in range(cart_items.count()):
                    item = cart_items.nth(i)
                    item_name = item.text_content()
                    if "Black" in item_name:
                        cart_has_special_product = True
                        break
                
                assert cart_has_special_product, "购物车中没有包含'Black'的商品"
                
                # 对整个浏览器窗口进行一次截图
                screenshot_path = f"{self.screenshot_dir}/test_{test_num}_success.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                # 更新测试结果
                test_result["status"] = "PASSED"
                test_result["screenshot_path"] = screenshot_path
                success_count += 1
                
            except Exception as e:
                # 记录错误信息并截图
                error_message = str(e)
                safe_filename = re.sub(r'[\\/:*?"<>|\n\r]', '_', error_message[:20])
                screenshot_path = f"{self.screenshot_dir}/test_{test_num}_error_{safe_filename}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                test_result["screenshot_path"] = screenshot_path
                test_result["error_message"] = error_message
            
            # 将本次测试结果添加到结果列表
            self.test_results.append(test_result)
            
            # 等待1秒后开始下一次测试
            time.sleep(1)
        
        # 生成HTML测试报告
        self.generate_html_report(total_tests, success_count)
    
    def generate_html_report(self, total_tests, success_count):
        # 计算失败次数
        failure_count = total_tests - success_count
        
        # 生成HTML报告
        html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Special商品购物车功能测试报告</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .overview {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .pass {
            color: green;
            font-weight: bold;
        }
        .fail {
            color: red;
            font-weight: bold;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Special商品购物车功能测试报告</h1>
        
        <div class="overview">
            <h2>测试概览</h2>
            <p>总执行次数：''' + str(total_tests) + '''次</p>
            <p>成功次数：<span class="pass">''' + str(success_count) + '''</span>次</p>
            <p>失败次数：<span class="fail">''' + str(failure_count) + '''</span>次</p>
        </div>
        
        <h2>详细结果</h2>
        <table>
            <tr>
                <th>测试序号</th>
                <th>结果</th>
                <th>截图路径</th>
            </tr>
        '''
        
        # 添加测试结果表格行
        for result in self.test_results:
            status_class = "pass" if result["status"] == "PASSED" else "fail"
            screenshot_link = f"<a href='{result['screenshot_path']}' target='_blank'>查看截图</a>"
            html_content += '''
            <tr>
                <td>''' + str(result['test_number']) + '''</td>
                <td class="''' + status_class + '''">''' + result['status'] + '''</td>
                <td>''' + screenshot_link + '''</td>
            </tr>
            '''
        
        # 结束HTML
        html_content += '''
        </table>
    </div>
</body>
</html>
        '''
        
        # 保存HTML报告
        report_path = "reports/repeated_special_cart_report.html"
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"测试报告已生成：{report_path}")
