# 📚 文档索引

欢迎使用 Auto-SignIn v2！这里是完整的文档索引。

---

## 🚀 新手入门

### 快速开始
- **3 分钟上手**：[docs/QUICK_START.md](QUICK_START.md)
- **安装部署**：[README.md](../README.md)

### Cookie 获取（必读）
- **完全指南**：[docs/COOKIE_GUIDE.md](COOKIE_GUIDE.md)
- **网易云音乐教程**：[docs/netease_cookie_tutorial.md](netease_cookie_tutorial.md)

---

## 📖 使用文档

### 基础使用
1. **获取 Cookie** - 按照上述教程获取
2. **添加账号** - `python -m src.cli.main add netease -u "用户名" -c "Cookie"`
3. **执行签到** - `python -m src.cli.main signin --all`
4. **查看结果** - `python -m src.cli.main history`

### 高级用法
- **定时任务** - `python -m src.cli.main schedule --enable -t "08:00"`
- **通知配置** - 编辑 `config/config.yaml`
- **多账号管理** - `python -m src.cli.main list`

---

## 🔧 配置说明

### 配置文件
- **主配置**：`config/config.yaml`
- **账号配置**：`config/accounts.yaml`
- **环境变量**：`.env`

### 配置示例
```yaml
# config/config.yaml
schedule:
  enabled: true
  time: "08:00"

notification:
  enabled: true
  telegram:
    enabled: true
    bot_token: "你的 Bot Token"
    chat_id: "你的 Chat ID"
```

---

## 🐳 部署指南

### Docker 部署
```bash
# 构建镜像
docker build -t autosignin:latest .

# 运行容器
docker run -d --name autosignin \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  -e NETEASE_COOKIES="MUSIC_U=xxx" \
  autosignin:latest
```

### GitHub Actions
1. Fork 项目
2. 添加 Secrets：
   - `NETEASE_COOKIES`
   - `BILIBILI_COOKIES`
3. Actions 自动运行

---

## 📊 平台支持

| 平台 | 状态 | Cookie 要求 | 文档 |
|------|------|------------|------|
| 网易云音乐 | ✅ | MUSIC_U, __csrf | [教程](netease_cookie_tutorial.md) |
| B 站 | ✅ | SESSDATA, bili_jct | [教程](COOKIE_GUIDE.md#哔哩哔哩) |
| CSDN | 🚧 | - | - |
| 淘宝 | 🚧 | - | - |
| 京东 | 🚧 | - | - |

---

## 🔔 通知系统

### 支持的通知方式
- **邮件通知** - SMTP 配置
- **Telegram** - Bot API
- **Webhook** - 自定义 API

### 配置示例
```yaml
# config/config.yaml
notification:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your_email@gmail.com"
    password: "your_password"
    to_email: "receive_email@gmail.com"
  
  telegram:
    enabled: true
    bot_token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    chat_id: "123456789"
```

---

## 🧪 测试与调试

### 测试命令
```bash
# 单元测试
pytest tests/

# 代码格式化
black src/
flake8 src/

# 日志查看
tail -f data/autosignin.log
```

### 调试模式
```bash
# 启用调试模式
export AUTOSIGNIN_DEBUG=true
python -m src.cli.main config --show
```

---

## ❓ 常见问题

### Cookie 相关
- **Q: Cookie 在哪里获取？**
  - A: 查看 [Cookie 获取指南](COOKIE_GUIDE.md)
  
- **Q: Cookie 多久过期？**
  - A: 通常 30 天，建议 25 天更新一次

- **Q: 多账号怎么办？**
  - A: 分别登录获取 Cookie，使用不同浏览器

### 使用问题
- **Q: 签到失败怎么办？**
  - A: Cookie 可能过期，重新获取
  
- **Q: 如何查看签到历史？**
  - A: `python -m src.cli.main history -l 50`

- **Q: 如何设置定时任务？**
  - A: `python -m src.cli.main schedule --enable -t "08:00"`

---

## 🤝 贡献指南

### 添加新平台
1. 在 `src/platforms/` 创建新文件
2. 继承 `BasePlatform` 类
3. 实现 `sign_in_async` 方法
4. 在 `src/core/engine.py` 注册

### 提交代码
1. Fork 项目
2. 创建分支：`git checkout -b feature/your-feature`
3. 提交：`git commit -m "Add: your feature"`
4. 推送：`git push origin feature/your-feature`
5. 创建 Pull Request

---

## 📮 联系方式

- **Email**: your.email@example.com
- **Telegram**: [@yourchannel](https://t.me/yourchannel)
- **Issues**: [GitHub Issues](https://github.com/yourusername/autosignin/issues)
- **讨论区**: [GitHub Discussions](https://github.com/yourusername/autosignin/discussions)

---

## 📝 更新日志

### v2.0.0 (2026-03-08)
- 🎉 完全重构
- ✨ CLI 命令行界面
- 🐳 Docker 支持
- ☁️ GitHub Actions
- 📊 数据库和统计
- 🔔 通知系统

### v1.0.0 (旧版本)
- 基础功能
- tkinter GUI
- 9 个平台支持

---

**🎉 祝你使用愉快！**

如有任何问题，请查看相关文档或提交 Issue。
