---
name: pytest-runner
description: 运行项目的 pytest 测试套件，并生成 HTML 测试报告
---

# pytest-runner 技能

## 工具要求
执行此技能需要使用以下 MCP 工具：
- terminal: 执行终端命令

## 触发条件
当用户说以下任何一句话时，触发此技能：
- "跑测试"
- "运行测试"
- "执行测试"
- "pytest"
- "运行所有测试"

## 执行步骤

### 步骤1：切换到项目目录并激活虚拟环境
```bash
cd D:\Trae\my_first_test
.venv\Scripts\activate
```

### 步骤2：运行所有测试用例
```bash
pytest tests/test_login.py -v --html=reports/skill_test_report.html --self-contained-html
```

### 步骤3：输出执行结果

根据命令执行结果，判断测试是否通过：

- **如果测试通过**（命令返回码为0）：
  输出："✅ 所有测试通过！报告已生成：reports/skill_test_report.html"

- **如果测试失败**（命令返回码非0）：
  输出："❌ 有测试失败，请查看 reports/skill_test_report.html 获取详细信息"

## 注意事项
1. 确保虚拟环境 .venv 存在
2. 确保已安装所有依赖（pytest、playwright等）
3. 执行前确认当前在项目根目录 D:\Trae\my_first_test