<p align="center">
  <a href="https://github.com/badhope/Auto-SignIn">
    <img src="https://img.shields.io/badge/Auto--SignIn-v2.1.0-brightgreen?style=for-the-badge&logo=github" alt="Auto-SignIn">
  </a>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python" alt="Python">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker" alt="Docker">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/actions">
    <img src="https://img.shields.io/badge/Tests-Passing-brightgreen?style=flat-square&logo=github-actions" alt="Tests">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/stargazers">
    <img src="https://img.shields.io/github/stars/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Stars">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/network/members">
    <img src="https://img.shields.io/github/forks/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Forks">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/issues">
    <img src="https://img.shields.io/github/issues/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Issues">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/pulls">
    <img src="https://img.shields.io/github/issues-pr/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Pull Requests">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/releases">
    <img src="https://img.shields.io/github/v/release/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Release">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/commits/main">
    <img src="https://img.shields.io/github/last-commit/badhope/Auto-SignIn?style=flat-square&logo=github" alt="Last Commit">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/blob/main/CODE_OF_CONDUCT.md">
    <img src="https://img.shields.io/badge/Code%20of%20Conduct-1.0-ff69b4?style=flat-square" alt="Code of Conduct">
  </a>
  <a href="https://github.com/badhope/Auto-SignIn/blob/main/CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/Contributions-Welcome-orange?style=flat-square" alt="Contributing">
  </a>
</p>

<p align="center">
  <a href="https://codecov.io/gh/badhope/Auto-SignIn">
    <img src="https://img.shields.io/codecov/c/github/badhope/Auto-SignIn?style=flat-square&logo=codecov" alt="Coverage">
  </a>
  <a href="https://pepy.tech/project/autosignin">
    <img src="https://img.shields.io/pypi/dm/autosignin?style=flat-square&logo=pypi" alt="Downloads">
  </a>
  <a href="https://pypi.org/project/autosignin/">
    <img src="https://img.shields.io/pypi/v/autosignin?style=flat-square&logo=pypi" alt="PyPI">
  </a>
  <a href="https://hub.docker.com/r/badhope/autosignin">
    <img src="https://img.shields.io/docker/pulls/badhope/autosignin?style=flat-square&logo=docker" alt="Docker Pulls">
  </a>
</p>

<h3 align="center">🚀 多平台自动签到系统</h3>

<p align="center">
  一个功能强大、易于扩展的自动签到工具，支持多种主流平台<br>
  <a href="./README.md">简体中文</a> | <a href="./README_EN.md">English</a>
</p>

---

## 📑 目录

- [✨ 功能特性](#-功能特性)
- [🎯 支持的平台](#-支持的平台)
- [📸 截图预览](#-截图预览)
- [🚀 快速开始](#-快速开始)
  - [Docker 部署（推荐）](#docker-部署推荐)
  - [本地运行](#本地运行)
  - [Web 界面](#web-界面)
- [📖 使用指南](#-使用指南)
  - [命令行使用](#命令行使用)
  - [配置说明](#配置说明)
  - [获取 Cookie](#获取-cookie)
- [🏗️ 架构设计](#️-架构设计)
- [🔌 添加新平台](#-添加新平台)
- [🧪 测试](#-测试)
- [📦 项目结构](#-项目结构)
- [🤝 贡献指南](#-贡献指南)
- [📝 更新日志](#-更新日志)
- [👥 贡献者](#-贡献者)
- [📄 许可证](#-许可证)
- [⚠️ 免责声明](#️-免责声明)
- [❤️ 致谢](#️-致谢)

---

## ✨ 功能特性

<table>
<tr>
<td width="50%">

### 🎯 核心功能

- **多平台支持** - 哔哩哔哩、网易云音乐、知乎、掘金、V2EX
- **定时任务** - 支持 Cron 表达式灵活配置
- **Docker 支持** - 一键部署，开箱即用
- **多账号管理** - 支持多账号同时签到
- **Web 界面** - 友好的可视化操作界面

</td>
<td width="50%">

### 🛡️ 高级特性

- **多渠道通知** - 钉钉、Server酱、PushPlus、邮件、Telegram
- **完整日志** - 完整的签到日志和错误追踪
- **容错机制** - 重试、熔断、限流、舱壁隔离
- **插件架构** - 轻松扩展新平台
- **健康检查** - Cookie 有效性与系统健康监控

</td>
</tr>
</table>

---

## 🎯 支持的平台

| 平台 | 显示名 | 状态 | 签到类型 |
|------|--------|------|----------|
| <img src="https://www.bilibili.com/favicon.ico" width="16" height="16"/> bilibili | 哔哩哔哩 | ✅ 已支持 | 每日签到、直播签到 |
| <img src="https://music.163.com/favicon.ico" width="16" height="16"/> netease_music | 网易云音乐 | ✅ 已支持 | 每日签到 |
| <img src="https://www.zhihu.com/favicon.ico" width="16" height="16"/> zhihu | 知乎 | ✅ 已支持 | 每日签到 |
| <img src="https://juejin.cn/favicon.ico" width="16" height="16"/> juejin | 掘金 | ✅ 已支持 | 每日签到 |
| <img src="https://www.v2ex.com/favicon.ico" width="16" height="16"/> v2ex | V2EX | ✅ 已支持 | 每日签到 |

> 💡 **提示**: 更多平台正在开发中，欢迎提交 Issue 或 PR 添加新平台支持！

---

## 📸 截图预览

### Web 界面

![Web UI](https://via.placeholder.com/800x450?text=Web+UI+Screenshot)

### 命令行界面

![CLI](https://via.placeholder.com/800x450?text=CLI+Screenshot)

---

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# 1️⃣ 克隆仓库
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# 2️⃣ 复制配置文件
cp config.example.yml config.yml

# 3️⃣ 编辑配置文件，添加你的账号信息
vim config.yml

# 4️⃣ 启动服务
docker-compose up -d

# 5️⃣ 查看日志
docker-compose logs -f
```

<details>
<summary>🔧 Docker Compose 配置详解</summary>

```yaml
version: '3.8'

services:
  autosignin:
    image: badhope/autosignin:latest
    container_name: autosignin
    restart: unless-stopped
    volumes:
      - ./config.yml:/app/config.yml
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
      - LOG_LEVEL=INFO
    ports:
      - "8080:8080"  # Web UI
```

</details>

### 本地运行

```bash
# 1️⃣ 克隆仓库
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# 2️⃣ 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或: venv\Scripts\activate  # Windows

# 3️⃣ 安装依赖
pip install -r requirements.txt

# 4️⃣ 复制配置文件
cp config.example.yml config.yml

# 5️⃣ 编辑配置文件
vim config.yml

# 6️⃣ 执行签到
python main.py sign

# 7️⃣ 启动调度器
python main.py run
```

### Web 界面

```bash
# 启动 Web 界面
python main.py web

# 访问 http://localhost:8080
```

---

## 📖 使用指南

### 命令行使用

```bash
# 显示帮助
python main.py --help

# 列出所有平台
python main.py list

# 显示系统状态
python main.py status

# 执行签到
python main.py sign

# 指定平台签到
python main.py sign -p bilibili zhihu

# 使用指定配置文件
python main.py -c config.yml sign

# 启动调度器
python main.py run

# 启动 Web 界面
python main.py web --host 0.0.0.0 --port 8080

# 健康检查
python main.py health
```

### 配置说明

<details>
<summary>📝 完整配置示例</summary>

```yaml
# 定时任务配置
schedule:
  expression: "0 9 * * *"  # 每天上午9点执行
  timezone: "Asia/Shanghai"

# 通知配置
notifications:
  dingtalk:
    enabled: false
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
    secret: "xxx"

  serverchan:
    enabled: false
    key: "xxx"

  pushplus:
    enabled: false
    token: "xxx"

  email:
    enabled: false
    smtp_server: "smtp.qq.com"
    smtp_port: 587
    sender: "your@email.com"
    password: "xxx"
    receiver: "receiver@email.com"

  telegram:
    enabled: false
    bot_token: "xxx"
    chat_id: "xxx"

# 账号配置
accounts:
  bilibili:
    - name: "账号1"
      sessdata: "xxx"
      bili_jct: "xxx"
      buvid3: "xxx"
      enabled: true

  netease_music:
    - name: "账号1"
      cookie: "xxx"
      enabled: true

  zhihu:
    - name: "账号1"
      cookie: "xxx"
      enabled: true

  juejin:
    - name: "账号1"
      cookie: "xxx"
      enabled: true

  v2ex:
    - name: "账号1"
      cookie: "xxx"
      enabled: true
```

</details>

### 获取 Cookie

<details>
<summary>📺 哔哩哔哩</summary>

1. 登录 https://www.bilibili.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 在左侧找到 `Cookies` → `https://www.bilibili.com`
5. 复制以下字段的值：
   - `SESSDATA`
   - `bili_jct`
   - `buvid3`

</details>

<details>
<summary>🎵 网易云音乐</summary>

1. 登录 https://music.163.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 在左侧找到 `Cookies` → `https://music.163.com`
5. 复制完整的 Cookie 字符串

</details>

<details>
<summary>📖 知乎</summary>

1. 登录 https://www.zhihu.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 在左侧找到 `Cookies` → `https://www.zhihu.com`
5. 复制完整的 Cookie 字符串

</details>

<details>
<summary>💎 掘金</summary>

1. 登录 https://juejin.cn
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 在左侧找到 `Cookies` → `https://juejin.cn`
5. 复制完整的 Cookie 字符串

</details>

<details>
<summary>🌐 V2EX</summary>

1. 登录 https://www.v2ex.com
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签
4. 在左侧找到 `Cookies` → `https://www.v2ex.com`
5. 复制完整的 Cookie 字符串

</details>

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI / Web UI                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      SignInEngine                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Core Components                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │   Platform  │  │   Storage   │  │  Notifier   │  │   │
│  │  │   Manager   │  │   Adapter   │  │   Manager   │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │   │
│  └─────────┼────────────────┼────────────────┼─────────┘   │
│            │                │                │              │
│  ┌─────────▼────────────────▼────────────────▼─────────┐   │
│  │              Resilience Layer                        │   │
│  │  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐ │   │
│  │  │ Retry  │  │ Circuit  │  │  Rate    │  │Bulk-  │ │   │
│  │  │        │  │ Breaker  │  │ Limiter  │  │head   │ │   │
│  │  └────────┘  └──────────┘  └──────────┘  └───────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Platform Plugins                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Bilibili │  │  Netease │  │  Zhihu   │  │  Juejin  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   V2EX   │  │  Custom  │  │  Custom  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 添加新平台

<details>
<summary>📖 详细教程</summary>

### 1. 创建平台文件

在 `autosignin/platforms/` 目录下创建新文件，例如 `my_platform.py`

### 2. 实现平台类

```python
from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult

@register_platform(
    name="my_platform",
    display_name="我的平台",
    version="1.0.0",
    capabilities=["daily_sign"],
    required_fields=["cookie"]
)
class MyPlatform(BasePlatform):
    name = "my_platform"
    display_name = "我的平台"
    base_url = "https://api.myplatform.com"

    async def sign_in(self, account_name: str, cookies: dict) -> SignInResult:
        """实现签到逻辑"""
        result = SignInResult(
            platform=self.name,
            account=account_name
        )
        
        try:
            # 调用平台 API
            response = await self.http_client.get(
                f"{self.base_url}/checkin",
                cookies=cookies
            )
            
            if response.status_code == 200:
                result.success = True
                result.message = "签到成功"
            else:
                result.success = False
                result.message = "签到失败"
                
        except Exception as e:
            result.success = False
            result.message = str(e)
            
        return result
```

### 3. 注册平台

平台会自动注册，无需手动添加到 `__init__.py`

### 4. 配置账号

在 `config.yml` 中添加：

```yaml
accounts:
  my_platform:
    - name: "账号1"
      cookie: "xxx"
      enabled: true
```

</details>

---

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_core.py

# 运行特定平台测试
pytest tests/test_bilibili.py

# 带覆盖率报告
pytest --cov=autosignin --cov-report=html

# 详细输出
pytest -v --tb=short
```

---

## 📦 项目结构

```
Auto-SignIn/
├── .github/                    # GitHub 配置
│   ├── ISSUE_TEMPLATE/         # Issue 模板
│   ├── PULL_REQUEST_TEMPLATE/  # PR 模板
│   └── workflows/              # GitHub Actions
├── autosignin/                 # 主包
│   ├── config/                 # 配置模块
│   ├── core/                   # 核心模块
│   ├── models/                 # 数据模型
│   ├── platforms/              # 平台插件
│   ├── resilience/             # 容错模式
│   └── utils/                  # 工具函数
├── docs/                       # 文档
├── tests/                      # 测试
├── .gitignore                  # Git 忽略文件
├── CHANGELOG.md                # 更新日志
├── CODE_OF_CONDUCT.md          # 行为准则
├── CONTRIBUTING.md             # 贡献指南
├── LICENSE                     # 许可证
├── README.md                   # 中文文档
├── README_EN.md                # 英文文档
├── SECURITY.md                 # 安全政策
├── config.example.yml          # 配置示例
├── docker-compose.yml          # Docker Compose 配置
├── Dockerfile                  # Docker 镜像
├── main.py                     # 入口文件
├── pyproject.toml              # 项目配置
└── requirements.txt            # Python 依赖
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 贡献方式

- 🐛 提交 Bug 报告
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🌍 翻译文档

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

详细指南请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细的版本更新历史。

### 最新版本

**[2.1.0] - 2026-03-24**

#### ✨ 新增
- Cookie 健康检查工具
- 页面内容分析器
- 健康检查与自动恢复
- CLI `health` 命令
- 优雅关闭机制

#### 🔧 改进
- 调度器优雅关闭
- 错误处理完善

---

## 👥 贡献者

感谢所有贡献者的付出！

<a href="https://github.com/badhope/Auto-SignIn/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=badhope/Auto-SignIn" />
</a>

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

```
MIT License

Copyright (c) 2024 badhope

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⚠️ 免责声明

本工具仅供学习交流使用，请勿用于商业用途。使用本工具时请遵守相关平台的服务条款。开发者不对使用本工具产生的任何后果负责。

---

## ❤️ 致谢

- 感谢所有贡献者的付出
- 感谢所有 Star 和 Fork 的用户
- 感谢以下开源项目：
  - [httpx](https://www.python-httpx.org/)
  - [pydantic](https://pydantic-docs.helpmanual.io/)
  - [APScheduler](https://apscheduler.readthedocs.io/)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/badhope">badhope</a>
</p>

<p align="center">
  <a href="https://github.com/badhope/Auto-SignIn">
    <img src="https://img.shields.io/badge/⬆%20回到顶部-blue?style=for-the-badge" alt="Back to top">
  </a>
</p>
