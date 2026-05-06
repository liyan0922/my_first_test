---
name: git-quick-commit
description: 快速提交所有修改，需要用户提供提交信息
---

# git-quick-commit 技能

## 工具要求
使用 terminal MCP 工具执行命令。

## 触发条件
用户说"提交代码"、"快速提交"、"commit"时

## 执行动作

1. **首先**，询问用户："请提供本次提交的信息（commit message）："

2. **收到提交信息后**，执行：
   ```bash
   cd D:\Trae\my_first_test && git add . && git commit -m "用户提供的信息"