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

<h3 align="center">🚀 Multi-Platform Auto Sign-In System</h3>

<p align="center">
  A powerful and extensible automatic sign-in tool supporting multiple major platforms<br>
  <a href="./README.md">简体中文</a> | <a href="./README_EN.md">English</a>
</p>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🎯 Supported Platforms](#-supported-platforms)
- [📸 Screenshots](#-screenshots)
- [🚀 Quick Start](#-quick-start)
  - [Docker Deployment (Recommended)](#docker-deployment-recommended)
  - [Local Installation](#local-installation)
  - [Web Interface](#web-interface)
- [📖 User Guide](#-user-guide)
  - [CLI Usage](#cli-usage)
  - [Configuration](#configuration)
  - [Getting Cookies](#getting-cookies)
- [🏗️ Architecture](#️-architecture)
- [🔌 Adding New Platforms](#-adding-new-platforms)
- [🧪 Testing](#-testing)
- [📦 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📝 Changelog](#-changelog)
- [👥 Contributors](#-contributors)
- [📄 License](#-license)
- [⚠️ Disclaimer](#️-disclaimer)
- [❤️ Acknowledgments](#️-acknowledgments)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features

- **Multi-Platform Support** - Bilibili, NetEase Music, Zhihu, Juejin, V2EX
- **Scheduled Tasks** - Flexible cron expression configuration
- **Docker Ready** - One-click deployment
- **Multi-Account Management** - Simultaneous sign-in for multiple accounts
- **Web Interface** - User-friendly visual interface

</td>
<td width="50%">

### 🛡️ Advanced Features

- **Multi-Channel Notifications** - DingTalk, ServerChan, PushPlus, Email, Telegram
- **Complete Logging** - Full sign-in logs and error tracking
- **Resilience Patterns** - Retry, Circuit Breaker, Rate Limiter, Bulkhead
- **Plugin Architecture** - Easy to extend new platforms
- **Health Check** - Cookie validity and system health monitoring

</td>
</tr>
</table>

---

## 🎯 Supported Platforms

| Platform | Display Name | Status | Sign-in Type |
|----------|-------------|--------|--------------|
| <img src="https://www.bilibili.com/favicon.ico" width="16" height="16"/> bilibili | Bilibili | ✅ Supported | Daily sign-in, Live check-in |
| <img src="https://music.163.com/favicon.ico" width="16" height="16"/> netease_music | NetEase Music | ✅ Supported | Daily sign-in |
| <img src="https://www.zhihu.com/favicon.ico" width="16" height="16"/> zhihu | Zhihu | ✅ Supported | Daily sign-in |
| <img src="https://juejin.cn/favicon.ico" width="16" height="16"/> juejin | Juejin | ✅ Supported | Daily sign-in |
| <img src="https://www.v2ex.com/favicon.ico" width="16" height="16"/> v2ex | V2EX | ✅ Supported | Daily sign-in |

> 💡 **Tip**: More platforms are under development. Feel free to submit an Issue or PR to add new platform support!

---

## 📸 Screenshots

### Web Interface

![Web UI](https://via.placeholder.com/800x450?text=Web+UI+Screenshot)

### Command Line Interface

![CLI](https://via.placeholder.com/800x450?text=CLI+Screenshot)

---

## 🚀 Quick Start

### Docker Deployment (Recommended)

```bash
# 1️⃣ Clone repository
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# 2️⃣ Copy configuration file
cp config.example.yml config.yml

# 3️⃣ Edit config.yml with your account information
vim config.yml

# 4️⃣ Start services
docker-compose up -d

# 5️⃣ View logs
docker-compose logs -f
```

<details>
<summary>🔧 Docker Compose Configuration Details</summary>

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

### Local Installation

```bash
# 1️⃣ Clone repository
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Copy configuration file
cp config.example.yml config.yml

# 5️⃣ Edit configuration file
vim config.yml

# 6️⃣ Run sign-in
python main.py sign

# 7️⃣ Start scheduler
python main.py run
```

### Web Interface

```bash
# Start Web interface
python main.py web

# Access http://localhost:8080
```

---

## 📖 User Guide

### CLI Usage

```bash
# Show help
python main.py --help

# List all platforms
python main.py list

# Show system status
python main.py status

# Run sign-in
python main.py sign

# Sign in to specific platforms
python main.py sign -p bilibili zhihu

# Use specific config file
python main.py -c config.yml sign

# Start scheduler
python main.py run

# Start Web interface
python main.py web --host 0.0.0.0 --port 8080

# Health check
python main.py health
```

### Configuration

<details>
<summary>📝 Complete Configuration Example</summary>

```yaml
# Schedule configuration
schedule:
  expression: "0 9 * * *"  # Run at 9:00 AM daily
  timezone: "Asia/Shanghai"

# Notification configuration
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

# Account configuration
accounts:
  bilibili:
    - name: "account1"
      sessdata: "xxx"
      bili_jct: "xxx"
      buvid3: "xxx"
      enabled: true

  netease_music:
    - name: "account1"
      cookie: "xxx"
      enabled: true

  zhihu:
    - name: "account1"
      cookie: "xxx"
      enabled: true

  juejin:
    - name: "account1"
      cookie: "xxx"
      enabled: true

  v2ex:
    - name: "account1"
      cookie: "xxx"
      enabled: true
```

</details>

### Getting Cookies

<details>
<summary>📺 Bilibili</summary>

1. Login to https://www.bilibili.com
2. Press `F12` to open Developer Tools
3. Switch to `Application` tab
4. Find `Cookies` → `https://www.bilibili.com` on the left
5. Copy the values of the following fields:
   - `SESSDATA`
   - `bili_jct`
   - `buvid3`

</details>

<details>
<summary>🎵 NetEase Music</summary>

1. Login to https://music.163.com
2. Press `F12` to open Developer Tools
3. Switch to `Application` tab
4. Find `Cookies` → `https://music.163.com` on the left
5. Copy the full cookie string

</details>

<details>
<summary>📖 Zhihu</summary>

1. Login to https://www.zhihu.com
2. Press `F12` to open Developer Tools
3. Switch to `Application` tab
4. Find `Cookies` → `https://www.zhihu.com` on the left
5. Copy the full cookie string

</details>

<details>
<summary>💎 Juejin</summary>

1. Login to https://juejin.cn
2. Press `F12` to open Developer Tools
3. Switch to `Application` tab
4. Find `Cookies` → `https://juejin.cn` on the left
5. Copy the full cookie string

</details>

<details>
<summary>🌐 V2EX</summary>

1. Login to https://www.v2ex.com
2. Press `F12` to open Developer Tools
3. Switch to `Application` tab
4. Find `Cookies` → `https://www.v2ex.com` on the left
5. Copy the full cookie string

</details>

---

## 🏗️ Architecture

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

## 🔌 Adding New Platforms

<details>
<summary>📖 Detailed Tutorial</summary>

### 1. Create Platform File

Create a new file in the `autosignin/platforms/` directory, e.g., `my_platform.py`

### 2. Implement Platform Class

```python
from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult

@register_platform(
    name="my_platform",
    display_name="My Platform",
    version="1.0.0",
    capabilities=["daily_sign"],
    required_fields=["cookie"]
)
class MyPlatform(BasePlatform):
    name = "my_platform"
    display_name = "My Platform"
    base_url = "https://api.myplatform.com"

    async def sign_in(self, account_name: str, cookies: dict) -> SignInResult:
        """Implement sign-in logic"""
        result = SignInResult(
            platform=self.name,
            account=account_name
        )
        
        try:
            # Call platform API
            response = await self.http_client.get(
                f"{self.base_url}/checkin",
                cookies=cookies
            )
            
            if response.status_code == 200:
                result.success = True
                result.message = "Sign-in successful"
            else:
                result.success = False
                result.message = "Sign-in failed"
                
        except Exception as e:
            result.success = False
            result.message = str(e)
            
        return result
```

### 3. Register Platform

The platform will be automatically registered, no need to manually add to `__init__.py`

### 4. Configure Account

Add to `config.yml`:

```yaml
accounts:
  my_platform:
    - name: "account1"
      cookie: "xxx"
      enabled: true
```

</details>

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_core.py

# Run specific platform test
pytest tests/test_bilibili.py

# With coverage report
pytest --cov=autosignin --cov-report=html

# Verbose output
pytest -v --tb=short
```

---

## 📦 Project Structure

```
Auto-SignIn/
├── .github/                    # GitHub configuration
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   ├── PULL_REQUEST_TEMPLATE/  # PR templates
│   └── workflows/              # GitHub Actions
├── autosignin/                 # Main package
│   ├── config/                 # Configuration module
│   ├── core/                   # Core modules
│   ├── models/                 # Data models
│   ├── platforms/              # Platform plugins
│   ├── resilience/             # Resilience patterns
│   └── utils/                  # Utility functions
├── docs/                       # Documentation
├── tests/                      # Tests
├── .gitignore                  # Git ignore file
├── CHANGELOG.md                # Changelog
├── CODE_OF_CONDUCT.md          # Code of Conduct
├── CONTRIBUTING.md             # Contributing guide
├── LICENSE                     # License
├── README.md                   # Chinese documentation
├── README_EN.md                # English documentation
├── SECURITY.md                 # Security policy
├── config.example.yml          # Configuration example
├── docker-compose.yml          # Docker Compose config
├── Dockerfile                  # Docker image
├── main.py                     # Entry point
├── pyproject.toml              # Project configuration
└── requirements.txt            # Python dependencies
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Ways to Contribute

- 🐛 Submit bug reports
- 💡 Propose new features
- 📝 Improve documentation
- 🔧 Submit code fixes
- 🌍 Translate documentation

### Contribution Process

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Latest Version

**[2.1.0] - 2026-03-24**

#### ✨ Added
- Cookie health check tool
- Page content analyzer
- Health check and auto-recovery
- CLI `health` command
- Graceful shutdown mechanism

#### 🔧 Improved
- Scheduler graceful shutdown
- Error handling improvements

---

## 👥 Contributors

Thanks to all contributors!

<a href="https://github.com/badhope/Auto-SignIn/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=badhope/Auto-SignIn" />
</a>

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

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

## ⚠️ Disclaimer

This tool is for learning and communication purposes only. Please comply with the terms of service of each platform when using this tool. The developers are not responsible for any consequences resulting from the use of this tool.

---

## ❤️ Acknowledgments

- Thanks to all contributors
- Thanks to all users who starred and forked
- Thanks to the following open-source projects:
  - [httpx](https://www.python-httpx.org/)
  - [pydantic](https://pydantic-docs.helpmanual.io/)
  - [APScheduler](https://apscheduler.readthedocs.io/)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/badhope">badhope</a>
</p>

<p align="center">
  <a href="https://github.com/badhope/Auto-SignIn">
    <img src="https://img.shields.io/badge/⬆%20Back%20to%20Top-blue?style=for-the-badge" alt="Back to top">
  </a>
</p>
