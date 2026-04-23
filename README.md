# Pytest + Playwright 自动化测试框架

基于Playwright和Page Object模式的自动化测试框架

## 项目结构

```
my_first_test/
├── pages/                  # Page Object模式页面类
│   ├── __init__.py
│   ├── base_page.py        # 基础页面类
│   ├── login_page.py       # 登录页面
│   ├── search_page.py      # 搜索页面
│   └── cart_page.py        # 购物车页面
├── tests/                  # 测试用例
│   ├── __init__.py
│   ├── test_login.py       # 登录测试
│   ├── test_search.py      # 搜索测试
│   └── test_cart.py        # 购物车测试
├── reports/                # 测试报告
│   ├── screenshots/        # 截图目录
│   ├── report.html        # HTML测试报告
│   └── coverage/          # 代码覆盖率报告
├── conftest.py            # pytest配置
├── pytest.ini             # pytest配置文件
└── requirements.txt       # 依赖包
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 安装浏览器驱动

```bash
python -m playwright install
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行登录测试
```bash
pytest tests/test_login.py
```

### 无头模式运行
```bash
pytest --headless
```

### 慢速模式运行（便于调试）
```bash
pytest --slow-mo=1000
```

## 测试报告

- HTML测试报告：`reports/report.html`
- 代码覆盖率报告：`reports/coverage/index.html`
- 截图：`reports/screenshots/`

## 框架特性

- 使用Playwright进行页面交互
- Page Object设计模式
- 自动生成HTML测试报告
- 代码覆盖率报告
- 失败时自动截图
- 每步操作后截图
- 支持无头模式和可视化模式
- 支持慢速模式便于调试

## 测试用例

### 登录测试

测试网站：https://www.saucedemo.com/

测试场景：
1. 打开登录页面
2. 输入用户名"standard_user"
3. 输入密码"secret_sauce"
4. 点击登录按钮
5. 验证跳转到inventory.html页面

### 购物车测试

测试网站：https://www.saucedemo.com/

测试场景：
1. 登录成功后，在商品列表页找到名为"Sauce Labs Backpack"的商品
2. 点击该商品下方的"Add to cart" 按钮
3. 验证按钮文字变为"Remove"（表示添加成功）
4. 点击页面右上角的购物车图标
5. 在购物车页面，验证商品名称包含 "Sauce Labs Backpack"
6. 验证商品数量为1