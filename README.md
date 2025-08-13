# HNAS 轻量级家庭 NAS 工具 v3.0 更新日志

![HNAS Logo](https://img.icons8.com/ios-filled/48/3776d6/windows8.png)

---

## 功能特色

- 🖥️ 桌面/开始菜单风格的 Web UI，支持多窗口、任务栏、窗口最大化/最小化/关闭
- 👥 多用户注册、登录与独立空间，权限互相隔离（未来计划）
- 📁 文件管理器支持文件夹浏览、上传、下载
- 🔒 简单易用，开箱即用，无需数据库

---

## v3.0 主要更新内容

### 新增功能

- **全新用户与数据目录结构**  
  - 用户数据目录由 `/data/users` 移动到 `/data/system/users`，用户信息由 `/data/system/user` 移动到 `/data/system/user-data`，结构更规范，便于管理和备份。
  - 文件管理器路径自动适配新结构，兼容旧数据平滑升级（需手动移动旧目录）。

- **“system目录” 独立浏览入口**  
  - 文件管理器新增“system目录”入口，超级管理员可直接浏览 `/data/system` 下全部内容，权限更细致。
  - 路径统一前缀 `system_dir`，安全隔离其它目录。

- **多账号隔离与安全增强**  
  - 用户文件夹和配置信息严格权限隔离，防止越权访问。
  - 普通用户仅可访问个人空间和壁纸文件夹，重要数据更安全。

- **UI & 体验优化**  
  - 文件管理器导航更清晰，路径显示与跳转逻辑优化。
  - 壁纸与用户设置界面细节改进，交互更友好。

### 优化与修复

- **代码结构升级**
  - 全面梳理路径相关代码，消除硬编码，新增全局目录常量，便于后续扩展维护。
  - 修复部分情况下路径拼接导致的 bug，提升健壮性。

- **兼容性与性能提升**
  - 强化多用户并发场景下的数据一致性，减少冲突与异常。
  - 文件上传/下载/浏览更流畅。

### 兼容性与升级说明

- **升级建议**：  
  - 先备份原有 `/data/users` 和 `/data/system/user` 目录；  
  - 停止 HNAS 服务后，将 `data/users` 移动到 `data/system/users`，`data/system/user` 移动到 `data/system/user-data`；  
  - 启动 3.0 版即可平滑升级，无需其它配置。
- Python 3.8 及以上
- 项目结构与旧版兼容，详见新版说明文档

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
    ├── system/
    │   ├── users/          # 用户文件根目录（新版路径）
    │   ├── user-data/      # 用户信息/配置（新版路径）
    │   └── wallpaper/      # 壁纸目录
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
## 🤖 AI 功能扩展模组（v3.1+ 实验性）
HNAS 不只是存储工具，它现在也会思考、吐槽、陪你 debug。欢迎进入 NAS 的灵魂觉醒时代。
***

### ✨ 新增功能
#### AI 文件摘要与搜索助手

上传 PDF、TXT、Markdown 后，AI 可自动生成摘要、提取关键字，支持自然语言搜索：「帮我找昨天的备忘录」。

后端集成 OpenAI / HuggingFace 模型，前端新增「摘要」按钮。

#### NAS 聊天助理（Beta）

桌面新增「NAS 助理」窗口，可与 NAS 聊天：「我今天该备份吗？」、「你怎么看我上传的 anime？」

支持实时对话、情绪回应，偶尔还会吐槽你。

#### Goblin 模式 AI 回应

每次操作都有 AI 式吐槽：「你又上传了 300MB 的动漫？NAS 表示压力很大。」

Debug 时自动生成 meme：「Permission denied？你是谁我不认得。」

#### 使用者行为分析（实验性）

自动分析使用者活跃时间、常用文件类型，推荐备份时间与分类建议。

支持图表展示，未来计划加入「NAS 心情日记」。

## #🧪 启用方式
安装额外依赖：

```bash
pip install openai langchain flask-socketio
```
在 app.py 中启用 AI 模块：

```python
from ai_module import GoblinAI
```
goblin = GoblinAI()
前端新增聊天窗口与摘要按钮（参考 templates/ai_chat.html）
