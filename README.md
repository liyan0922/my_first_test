# Pytest自动化测试框架

基于Playwright和Page Object模式的自动化测试框架

## 项目结构

```
my_first_test/
├── pages/                  # Page Object模式页面类
│   ├── __init__.py
│   ├── base_page.py        # 基础页面类
│   ├── login_page.py      # 登录页面
│   ├── search_page.py     # 搜索页面
│   └── cart_page.py       # 购物车页面
├── tests/                  # 测试用例
│   ├── __init__.py
│   ├── test_login.py      # 登录测试
│   ├── test_search.py     # 搜索测试
│   └── test_cart.py       # 购物车测试
├── reports/                # 测试报告
│   ├── screenshots/       # 失败截图
│   ├── report.html       # HTML测试报告
│   └── coverage/          # 代码覆盖率报告
├── conftest.py            # pytest配置
├── pytest.ini             # pytest配置文件
└── requirements.txt       # 依赖包
```

## 安装依赖

```bash
pip install -r requirements.txt
```

安装Playwright浏览器驱动：

```bash
python -m playwright install
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_login.py
```

### 运行特定测试类

```bash
pytest tests/test_login.py::TestLogin
```

### 运行特定测试方法

```bash
pytest tests/test_login.py::TestLogin::test_login_with_invalid_credentials
```

### 使用标记运行测试

```bash
pytest -m login
pytest -m search
pytest -m cart
```

### 无头模式运行

```bash
pytest --headless
```

### 慢速模式运行

```bash
pytest --slow-mo=1000
```

## 查看测试报告

测试完成后，HTML报告将保存在 `reports/report.html`

在浏览器中打开报告：

```bash
start reports/report.html
```

## 代码覆盖率

覆盖率报告保存在 `reports/coverage/index.html`

## Page Object模式

框架使用Page Object模式，将页面元素和操作封装在页面类中：

- `BasePage`: 基础页面类，提供通用方法
- `LoginPage`: 登录页面，处理登录相关操作
- `SearchPage`: 搜索页面，处理搜索相关操作
- `CartPage`: 购物车页面，处理购物车相关操作

## 特性

- 使用Playwright进行页面交互
- Page Object设计模式
- 自动生成HTML测试报告
- 代码覆盖率报告
- 失败时自动截图
- 支持无头模式和可视化模式
- 支持慢速模式便于调试