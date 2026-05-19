import pytest
import allure
import csv
import os
from pages.login_page import LoginPage
import pandas as pd

# 定义 CSV 文件路径
CSV_PATH = os.path.join(os.path.dirname(__file__), "..","test_data","login_users.csv")

def load_login_data_from_csv():
    """从 CSV 文件中读取登录测试数据"""
    data = []
    with open(CSV_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            password = row['password']
            expect_success = row['expect_success']
            data.append((username, password, expect_success.lower() == 'true'))
    return data

@allure.feature("登录功能 - 数据驱动 CSV 方式")
class TestLoginDataDrivenFromCSV:
    @pytest.mark.parametrize("username, password, expect_success", load_login_data_from_csv())
    def test_login_with_csv_data(self, page,username, password, expect_success):
        """
        测试登录功能 - 数据驱动 CSV 方式
        :param page: 测试页面实例
        :param username: 用户名
        :param password: 密码
        :param expect_success: 期望是否登录成功
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login(username, password)

        # Assert - 验证登录结果
        if expect_success:
            assert "inventory.html" in page.url, f"用户 {username} 登录失败"
        else:
            assert "inventory.html" not in page.url, f"用户 {username} 登录成功"
            # 验证错误消息（仅对登录失败的情况）
            error_visible = page.is_visible('[data-test="error"]')
            assert error_visible, f"用户{username}登录失败，错误消息未显示"

def load_login_data_from_excel():
    """从 Excel 文件中读取登录测试数据"""
    excel_path = os.path.join(os.path.dirname(__file__), "..","test_data","login_users.xlsx")
    df = pd.read_excel(excel_path)
    data = []
    for index, row in df.iterrows():
        username = row['username']
        password = row['password']
        expect_success = row['expect_success']
        data.append((username, password, expect_success == True))
    return data


@allure.feature("登录功能 - 数据驱动 Excel 方式")
class TestLoginDataDrivenFromExcel:
    @pytest.mark.parametrize("username, password, expect_success", load_login_data_from_excel())
    def test_login_with_excel_data(self, page, username, password, expect_success):
        """
        测试登录功能 - 数据驱动 Excel 方式
        :param page: 测试页面实例
        :param username: 用户名
        :param password: 密码
        :param expect_success: 期望是否登录成功
        """
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login(username, password)

        # Assert - 验证登录结果
        if expect_success:
            assert "inventory.html" in page.url, f"用户 {username} 登录失败"
        else:
            assert "inventory.html" not in page.url, f"用户 {username} 登录成功"
            # 验证错误消息（仅对登录失败的情况）
            error_visible = page.is_visible('[data-test="error"]')
            assert error_visible, f"用户{username}登录失败，错误消息未显示"





