# 🤝 贡献指南

首先，感谢您考虑为 Auto-SignIn 做出贡献！正是因为像您这样的人，Auto-SignIn 才能成为一个优秀的工具。

## 📋 目录

- [行为准则](#行为准则)
- [我能做什么贡献？](#我能做什么贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [项目结构](#项目结构)
- [开发环境设置](#开发环境设置)
- [测试](#测试)
- [文档](#文档)
- [社区](#社区)

---

## 行为准则

本项目及其所有参与者均受 [Code of Conduct](CODE_OF_CONDUCT.md) 约束。参与本项目即表示您同意遵守其条款。

---

## 我能做什么贡献？

### 🐛 报告 Bug

在提交 Bug 报告之前，请先：
1. 检查 [Issues](https://github.com/badhope/Auto-SignIn/issues) 中是否已有相同问题
2. 确认您使用的是最新版本
3. 阅读文档确认不是使用方式问题

提交 Bug 报告时，请包含：
- **清晰的标题和描述**
- **复现步骤**（越详细越好）
- **预期行为** vs **实际行为**
- **环境信息**（操作系统、Python 版本等）
- **日志输出**或截图
- 可能的解决方案

### 💡 建议新功能

我们欢迎任何改进建议！请包含：
- **清晰的功能描述**
- **使用场景**（为什么需要这个功能？）
- **可能的实现方案**
- 是否愿意自己实现

### 📝 改进文档

文档改进包括：
- 修正拼写或语法错误
- 添加缺失的文档
- 改进现有文档的清晰度
- 翻译文档

### 🔧 提交代码

查看 [Issues](https://github.com/badhope/Auto-SignIn/issues) 中的 `good first issue` 或 `help wanted` 标签。

---

## 开发流程

### 1. Fork 并 Clone 仓库

```bash
# Fork 后 clone 您的仓库
git clone https://github.com/YOUR_USERNAME/Auto-SignIn.git
cd Auto-SignIn

# 添加上游仓库
git remote add upstream https://github.com/badhope/Auto-SignIn.git
```

### 2. 创建分支

```bash
# 从 main 创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档改进
- `refactor/` - 代码重构
- `test/` - 测试相关
- `chore/` - 其他修改

### 3. 进行开发

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果有

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或: venv\Scripts\activate  # Windows
```

### 4. 测试

```bash
# 运行测试
pytest

# 运行特定测试
pytest tests/test_core.py

# 带覆盖率
pytest --cov=autosignin
```

### 5. 提交更改

```bash
git add .
git commit -m "feat: 添加新功能描述"
```

### 6. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

---

## 代码规范

### Python 代码规范

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# ✅ 好的示例
from typing import Dict, List, Optional


class SignInEngine:
    """签到引擎类"""
    
    def __init__(self, config: Dict[str, any]):
        self.config = config
        self._initialized = False
    
    async def sign_in(self, platform: str) -> bool:
        """执行签到
        
        Args:
            platform: 平台名称
            
        Returns:
            签到是否成功
        """
        if not self._initialized:
            raise RuntimeError("Engine not initialized")
        
        return True


# ❌ 不好的示例
def signin(p,d):
    return True
```

### 类型注解

使用类型注解提高代码可读性：

```python
from typing import Dict, List, Optional, Any


def process_account(
    account: Dict[str, Any],
    platform: str,
    enabled: bool = True
) -> Optional[Dict[str, Any]]:
    """处理账号"""
    if not enabled:
        return None
    return {"status": "success"}
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def calculate_reward(points: int, multiplier: float = 1.0) -> float:
    """计算奖励积分
    
    根据用户积分和倍率计算最终奖励。
    
    Args:
        points: 用户当前积分
        multiplier: 奖励倍率，默认为 1.0
        
    Returns:
        计算后的奖励积分
        
    Raises:
        ValueError: 当积分为负数时
        
    Examples:
        >>> calculate_reward(100, 1.5)
        150.0
    """
    if points < 0:
        raise ValueError("积分不能为负数")
    return points * multiplier
```

### 导入顺序

```python
# 标准库
import os
import sys
from typing import Dict, List

# 第三方库
import httpx
from pydantic import BaseModel

# 本地模块
from autosignin.core.engine import SignInEngine
from autosignin.models.signin import SignInResult
```

---

## 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关
- `perf`: 性能优化
- `ci`: CI/CD 相关

### 示例

```bash
# 新功能
git commit -m "feat: 添加抖音平台支持"

# Bug 修复
git commit -m "fix: 修复 Bilibili Cookie 验证失败的问题"

# 文档
git commit -m "docs: 更新 README 中的安装说明"

# 多行提交
git commit -m "feat: 添加健康检查功能

- 添加 Cookie 有效性检查
- 添加系统健康状态监控
- 添加 CLI health 命令

Closes #123"
```

---

## Pull Request 流程

### PR 检查清单

在提交 PR 之前，请确保：

- [ ] 代码遵循项目的代码规范
- [ ] 已添加必要的测试
- [ ] 所有测试都通过
- [ ] 已更新相关文档
- [ ] 提交消息符合规范
- [ ] 分支已与 main 同步

### PR 标题

使用与提交消息相同的格式：

```
feat: 添加新平台支持
fix: 修复签到失败的问题
docs: 更新配置说明
```

### PR 描述模板

```markdown
## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新
- [ ] 其他

## 描述
简要描述您的更改

## 相关 Issue
Closes #123

## 测试
描述您如何测试这些更改

## 截图
如果有 UI 更改，请添加截图
```

### Code Review

- 耐心等待维护者审核
- 及时响应审核意见
- 保持讨论的专业性和友好性

---

## 项目结构

```
Auto-SignIn/
├── autosignin/           # 主包
│   ├── config/          # 配置模块
│   ├── core/            # 核心模块
│   ├── models/          # 数据模型
│   ├── platforms/       # 平台插件
│   ├── resilience/      # 容错模式
│   └── utils/           # 工具函数
├── tests/               # 测试
├── docs/                # 文档
├── main.py              # 入口文件
└── config.example.yml   # 配置示例
```

---

## 开发环境设置

### 系统要求

- Python 3.8+
- Git

### 快速开始

```bash
# 1. Clone 仓库
git clone https://github.com/badhope/Auto-SignIn.git
cd Auto-SignIn

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或: venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装开发依赖
pip install pytest pytest-asyncio pytest-cov black flake8 mypy

# 5. 运行测试
pytest

# 6. 代码格式化
black autosignin/

# 7. 代码检查
flake8 autosignin/
mypy autosignin/
```

---

## 测试

### 运行测试

```bash
# 所有测试
pytest

# 特定文件
pytest tests/test_core.py

# 特定测试
pytest tests/test_core.py::TestSignInEngine

# 带覆盖率
pytest --cov=autosignin --cov-report=html

# 详细输出
pytest -v --tb=short
```

### 编写测试

```python
import pytest
from autosignin.core.engine import SignInEngine


class TestSignInEngine:
    """SignInEngine 测试类"""
    
    @pytest.fixture
    def engine(self):
        """创建测试用的引擎实例"""
        config = {"test": True}
        return SignInEngine(config)
    
    def test_init(self, engine):
        """测试初始化"""
        assert engine.config is not None
    
    @pytest.mark.asyncio
    async def test_sign_in(self, engine):
        """测试签到功能"""
        result = await engine.sign_in("test_platform")
        assert result is not None
```

---

## 文档

### 文档结构

- `README.md` - 项目介绍和快速开始
- `README_EN.md` - 英文文档
- `CHANGELOG.md` - 更新日志
- `CONTRIBUTING.md` - 贡献指南
- `CODE_OF_CONDUCT.md` - 行为准则
- `docs/` - 详细文档

### 文档风格

- 使用清晰简洁的语言
- 提供代码示例
- 使用 Markdown 格式
- 添加适当的标题和列表

---

## 添加新平台

### 步骤

1. 在 `autosignin/platforms/` 创建新文件
2. 继承 `BasePlatform` 类
3. 实现必要的方法
4. 添加测试
5. 更新文档

### 示例

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
    """我的平台签到实现"""
    
    name = "my_platform"
    display_name = "我的平台"
    base_url = "https://api.myplatform.com"
    
    async def sign_in(self, account_name: str, cookies: dict) -> SignInResult:
        """执行签到"""
        result = SignInResult(
            platform=self.name,
            account=account_name
        )
        
        try:
            response = await self.http_client.post(
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

---

## 社区

- [GitHub Issues](https://github.com/badhope/Auto-SignIn/issues) - Bug 报告和功能建议
- [GitHub Discussions](https://github.com/badhope/Auto-SignIn/discussions) - 一般讨论

---

## 许可证

通过贡献代码，您同意您的贡献将根据 [MIT License](LICENSE) 进行许可。

---

<p align="center">
  再次感谢您的贡献！❤️
</p>
