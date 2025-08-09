# HNAS 轻量级家庭 NAS 工具 v1.0

![HNAS Logo](https://img.icons8.com/ios-filled/48/3776d6/windows8.png)

HNAS 是一个基于 Python Flask 的轻量级家庭 NAS (网络存储) 工具，拥有 Windows 桌面风格的 Web 界面，支持多用户、文件管理、桌面窗口、开始菜单等特性，适合在家庭或小型局域网中搭建个人文件服务器。

---

## 功能特色

- 🖥️ 桌面/开始菜单风格的 Web UI，支持多窗口、任务栏、窗口最大化/最小化/关闭
- 👥 多用户注册、登录与独立空间，权限互相隔离（未来计划）
- 📁 文件管理器支持文件夹浏览、上传、下载
- 🔒 简单易用，开箱即用，无需数据库

---

## 快速开始

### 1. 环境准备

- Python 3.8 及以上（推荐 3.10+）
- pip

### 2. 安装依赖

```bash
pip install flask
```

### 3. 运行项目

```bash
python app.py
```

- 首次运行自动进入注册页面，后续可访问登录页面
- 默认监听 http://127.0.0.1:5000

---

## 目录结构

```
HNAS/
├── app.py                  # 主程序
├── static/
│   ├── desktop.js          # 桌面/窗口主JS
│   └── desktop.css         # 桌面/任务栏/窗口UI样式
├── templates/
│   ├── index.html          # 桌面主页面
│   ├── login.html          # 登录页面
│   ├── register.html       # 注册页面
│   ├── about_inner.html    # 关于窗口
│   └── filemanager_inner.html # 文件管理器窗口
└── data/
    ├── users/              # 用户文件根目录
    └── system/user/        # 用户信息/配置
```

---

## 截图预览

> ![桌面界面截图](https://github.com/george06350/HNAS/blob/main/data/system/readme.png)  

---

## 常见问题

- **Q:** 为什么打不开网页？
  - A: 请确保 `app.py` 正在运行，且防火墙未阻止 5000 端口。
- **Q:** 文件上传/下载失败？
  - A: 检查 data 目录的读写权限，确保浏览器未阻止弹窗。
- **Q:** 如何修改端口？
  - A: 编辑 `app.py` 最底部的 `app.run(...)`，改为你需要的端口。

---

## 开发&贡献

- 作者：george06350
- 仓库地址：https://github.com/george06350/HNAS

欢迎 Issue 或 PR 交流建议！

---

## 版权声明

```
# =============================================================
#  HNAS - 轻量级家庭NAS工具
#  Copyright (c) 2024-2025 George06350. All Rights Reserved.
#  项目地址: https://github.com/george06350/HNAS
# 
#  本项目源码仅供学习与个人非商业用途使用。
#  未经许可，不得用于商业用途或翻版传播。
# =============================================================
```

---
