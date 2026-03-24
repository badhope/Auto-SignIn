# Auto-SignIn

A powerful multi-platform automatic sign-in system supporting Bilibili, NetEase Music, Zhihu, Juejin, V2EX and other major platforms.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![GitHub stars](https://img.shields.io/github/stars/badhope/Auto-SignIn)](https://github.com/badhope/Auto-SignIn/stargazers)

[中文](./README.md) | [English](./README_EN.md)

## Features

- **Multi-Platform Support** - Bilibili, NetEase Music, Zhihu, Juejin, V2EX
- **Scheduled Tasks** - Flexible cron expression configuration
- **Docker Ready** - One-click deployment
- **Multi-Account Management** - Simultaneous sign-in for multiple accounts
- **Multi-Channel Notifications** - DingTalk, ServerChan, PushPlus, Email, Telegram
- **Complete Logging** - Full sign-in logs and error tracking
- **Resilience Patterns** - Retry, Circuit Breaker, Rate Limiter, Bulkhead
- **Plugin Architecture** - Easy to extend new platforms

## Supported Platforms

| Platform | Display Name | Status |
|----------|-------------|--------|
| bilibili | Bilibili | ✅ |
| netease_music | NetEase Music | ✅ |
| zhihu | Zhihu | ✅ |
| juejin | Juejin | ✅ |
| v2ex | V2EX | ✅ |

## Quick Start

### Docker Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# Copy configuration file
cp config.example.yml config.yml

# Edit config.yml with your account information
vim config.yml

# Start services
docker-compose up -d
```

### Local Installation

```bash
# Clone repository
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run sign-in
python main.py sign

# Run scheduler
python main.py run
```

## Project Structure

```
Auto-SignIn/
├── autosignin/              # Main package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py               # Command-line interface
│   ├── config/              # Configuration
│   │   ├── __init__.py
│   │   ├── config.py        # ConfigManager
│   │   └── models.py        # Pydantic models
│   ├── core/                # Core modules
│   │   ├── __init__.py
│   │   ├── engine.py        # SignInEngine
│   │   ├── exceptions.py    # Exception classes
│   │   ├── notifier.py      # NotificationManager
│   │   ├── scheduler.py     # TaskScheduler
│   │   └── storage.py       # StorageAdapter
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── account.py       # Account models
│   │   └── signin.py        # SignIn models
│   ├── platforms/           # Platform plugins
│   │   ├── __init__.py
│   │   ├── base.py          # BasePlatform
│   │   ├── manager.py       # PlatformManager
│   │   ├── bilibili.py      # Bilibili plugin
│   │   ├── netease.py       # NetEase Music plugin
│   │   ├── zhihu.py         # Zhihu plugin
│   │   ├── juejin.py        # Juejin plugin
│   │   └── v2ex.py          # V2EX plugin
│   ├── resilience/          # Resilience patterns
│   │   ├── __init__.py
│   │   ├── retry.py         # Retry with exponential backoff
│   │   ├── circuit_breaker.py  # Circuit breaker
│   │   ├── rate_limiter.py    # Rate limiter
│   │   └── bulkhead.py        # Bulkhead isolation
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── logging_config.py   # Logging configuration
├── docs/                    # Documentation
├── tests/                   # Tests
├── main.py                  # Entry point
├── config.example.yml        # Configuration example
├── requirements.txt          # Python dependencies
├── Dockerfile
└── docker-compose.yml
```

## CLI Usage

```bash
# Show help
python main.py --help

# List all platforms
python main.py list

# Show system status
python main.py status

# Sign in to all platforms
python main.py sign

# Sign in to specific platforms
python main.py sign -p bilibili zhihu

# Sign in with specific config file
python main.py -c config.yml sign

# Start scheduler
python main.py run
```

## Configuration

Edit `config.yml`:

```yaml
# Schedule configuration
schedule:
  # Run at 9:00 AM daily
  cron: "0 9 * * *"
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

## How to Get Cookies

### Bilibili
1. Login to https://www.bilibili.com
2. Press F12 → Application → Cookies
3. Copy `SESSDATA`, `bili_jct`, `buvid3`

### NetEase Music
1. Login to https://music.163.com
2. Press F12 → Application → Cookies
3. Copy the full cookie string

### Other Platforms
Similar steps - login and copy cookies from developer tools.

## Adding New Platforms

1. Create a new platform file in `autosignin/platforms/`
2. Inherit from `BasePlatform`
3. Use `@register_platform` decorator
4. Implement `sign_in()` method

```python
from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult

@register_platform(
    name="example",
    display_name="Example Platform",
    version="1.0.0",
    capabilities=["daily_sign"],
    required_fields=["cookie"]
)
class ExamplePlatform(BasePlatform):
    name = "example"
    display_name = "Example Platform"
    base_url = "https://api.example.com"

    async def sign_in(self, account_name: str, cookies: dict) -> SignInResult:
        result = SignInResult(
            platform=self.name,
            account=account_name
        )
        # Implement sign-in logic
        return result
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   SignInEngine                   │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │
│  │   Platform  │  │   Storage  │  │Notifier │  │
│  │   Manager   │  │  Adapter   │  │ Manager │  │
│  └──────┬──────┘  └──────┬──────┘  └────┬────┘  │
│         │                │              │       │
│  ┌──────┴──────┐  ┌──────┴──────┐       │       │
│  │   Platform  │  │    SQLite  │       │       │
│  │   Plugins   │  │   Storage  │       │       │
│  └─────────────┘  └─────────────┘       │       │
│                                          │       │
│  ┌──────────────────────────────────────┐│       │
│  │           Resilience Layer            ││       │
│  │  ┌──────┐ ┌──────────┐ ┌──────────┐ ││       │
│  │  │Retry │ │Circuit   │ │Rate      │ ││       │
│  │  │      │ │Breaker   │ │Limiter   │ ││       │
│  │  └──────┘ └──────────┘ └──────────┘ ││       │
│  └──────────────────────────────────────┘│       │
└─────────────────────────────────────────────────┘
```

## Testing

```bash
# Run all tests
pytest

# Run specific platform tests
pytest tests/test_bilibili.py

# Run with coverage
pytest --cov=autosignin --cov-report=html
```

## Documentation

See [docs/](docs/) for detailed documentation:
- [Problems and Solutions](docs/problems_and_solutions.md)
- [Next Steps](docs/next_steps.md)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[MIT License](LICENSE)

## Disclaimer

This tool is for learning and communication purposes only. Please comply with the terms of service of each platform when using this tool.
