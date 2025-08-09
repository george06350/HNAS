# HNAS 轻量级家庭 NAS 工具 v2.0 更新日志

![HNAS Logo](https://img.icons8.com/ios-filled/48/3776d6/windows8.png)

---

## 功能特色

- 🖥️ 桌面/开始菜单风格的 Web UI，支持多窗口、任务栏、窗口最大化/最小化/关闭
- 👥 多用户注册、登录与独立空间，权限互相隔离（未来计划）
- 📁 文件管理器支持文件夹浏览、上传、下载
- 🔒 简单易用，开箱即用，无需数据库

---

## v2.0 主要更新内容

### 新增功能

- **桌面壁纸自定义**
  - 支持在【设置】页面选择壁纸1/壁纸2，壁纸目录为 `/data/system/wallpaper`，用户可自行添加图片。
  - 首次启动自动创建 wallpaper 文件夹，并下载官方默认壁纸（wallpaper1.png、wallpaper2.png）。
  - 桌面背景根据设置页选择的壁纸1实时生效，无需刷新缓存。

- **壁纸预览**
  - 设置页支持壁纸图片预览。

### 优化与修复

- **代码结构优化**
  - 壁纸设置与桌面背景渲染分离，后端统一读取壁纸配置。
  - 支持低版本 Flask（去除 `@app.before_first_request`，改为全局初始化）。
- **UI 保持一致**
  - 桌面页面（index.html）保留原有 Windows 风格、开始菜单、窗口管理等所有功能，壁纸功能无缝集成不影响旧功能。
- **健壮性增强**
  - 自动检测并补全壁纸目录及默认资源，避免因缺失文件导致异常。

### 兼容性与升级说明

- Python 3.8 及以上（推荐 3.10+）
- 安装依赖：`pip install flask`
- 项目结构和原有功能保持一致

---

## 快速开始

### 1. 环境准备

- Python 3.8 及以上
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
