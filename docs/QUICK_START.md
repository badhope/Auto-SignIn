# 快速开始 - Cookie 获取指南

## 🎯 3 分钟快速上手

### 方式一：最简单（推荐新手）

1. **安装浏览器扩展**
   - Chrome/Edge: 安装 [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
   - Firefox: 安装 [Cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)

2. **访问网站并登录**
   - 网易云音乐：https://music.163.com
   - B 站：https://www.bilibili.com

3. **导出 Cookie**
   - 点击扩展图标 🍪
   - 点击 "Copy" 或 "导出"
   - 粘贴到命令行

---

### 方式二：无需安装（推荐）

#### 网易云音乐

```bash
# 1. 打开 https://music.163.com 并登录
# 2. 按 F12
# 3. 切换到 Console 标签
# 4. 粘贴以下代码并按回车：

console.log("复制下面的内容：");
console.log(document.cookie);
```

#### B 站

```bash
# 1. 打开 https://www.bilibili.com 并登录
# 2. 按 F12 → Console
# 3. 粘贴代码：

console.log("SESSDATA=" + document.cookie.split('SESSDATA=')[1].split(';')[0] + 
            "; bili_jct=" + document.cookie.split('bili_jct=')[1].split(';')[0]);
```

---

## 📋 详细步骤（图解）

### 步骤 1: 打开开发者工具

```
┌─────────────────────────────────┐
│  浏览器窗口                      │
│  ┌────────────────────────────┐ │
│  │  网页内容                   │ │
│  └────────────────────────────┘ │
│  ┌────────────────────────────┐ │
│  │ 开发者工具 (F12)            │ │
│  │ ├─ Elements               │ │
│  │ ├─ Console ✅             │ │
│  │ ├─ Network                │ │
│  │ └─ ...                    │ │
│  └────────────────────────────┘ │
└─────────────────────────────────┘
```

### 步骤 2: 找到 Cookie

**方法 A: Console 控制台**
```
Console 标签
└── 输入：console.log(document.cookie)
     └── 输出：MUSIC_U=xxx; __csrf=xxx; ...
```

**方法 B: Network 网络**
```
Network 标签
├── 请求列表
│   └── www (点击)
│       └── Headers
│           └── Request Headers
│               └── Cookie: MUSIC_U=xxx; __csrf=xxx
```

---

## ✅ Cookie 格式验证

### 正确格式

```bash
# 网易云音乐（完整）
MUSIC_U=000E19F2EE3D1A8844CC977864B270A0998045BC2587E30286AC70F8F45BC5F2BF9E645AEEF9038A03E360AB31D6ECA3FA20A4CD25DCD29881A300EECFD2580A6777575A6B6B14812E53F8AB197C7FC0721D7B6C1CD35B390F4A2AADEE61120BDC0B57D258989B39391CC969C6CF8790A8F3260F74EE3F550F125D8A432E89B09DDD38859D6C7A665E5E14D6ACFCDBEC4CE4DCD2889BBB2BD9A7B994ED25249FBFDB94FBC79FEB0760E28AB172A840DAE99A6F7DFFDF3F7339594A151675C641C153626592CB775C69E8B62D5522502D5C926576A2A9A824FD6A552A007CF0EE3A3F1913236E12DA82D18FEA28349B40AD2E20C9E7DD458A3C1A50849A36EE0309DB99261D2B7A77C0CECDE5DEAB52DFF817FDB9A65592DA5108EA0DE443AB767D011CD8B089AEC3C50E804D95F1C959C813B22DC5EEB4E15F6A58011BA5DC416DAD25F985E6FD4F8B9EB57140CC285C407BF5D0C27FB5CD2BF94F5A7F0E0A45B6E4D411574BA97C33C34BF6C69EC5C7BA766C550088E44CA5EB0AE796CFCAA61B17913A0F26803FF77A1023E4BE189C5BF30FA20856F076283320D933F180FF22; __csrf=22f9a8e115d0c00be9b13f09b9cb8e18; NMTID=00OFIiZvuZprRN5OkIjmHeFgOcjrYoAAAGctzehwA

# 网易云音乐（最小可用）
MUSIC_U=xxx; __csrf=xxx

# B 站
SESSDATA=xxx; bili_jct=xxx
```

### 错误格式 ❌

```bash
# ❌ 缺少分号
MUSIC_U=xxx __csrf=xxx

# ❌ 缺少空格
MUSIC_U=xxx;__csrf=xxx

# ❌ 只有部分字段
MUSIC_U=xxx

# ❌ 包含多余内容
Cookie: MUSIC_U=xxx  # 不要 "Cookie: " 前缀
```

---

## 🚀 快速测试

获取 Cookie 后，立即测试：

```bash
# 1. 添加账号
python -m src.cli.main add netease -u "我的账号" -c "你的 Cookie"

# 2. 执行签到
python -m src.cli.main signin --platform netease

# 3. 查看结果
python -m src.cli.main history
```

---

## ❓ 常见问题

### Q: Cookie 在哪里？
**A**: 登录后，在浏览器的开发者工具中可以找到

### Q: 为什么我的 Cookie 不能用？
**A**: 
- 可能已过期 → 重新登录获取
- 可能格式错误 → 检查分号和空格
- 可能字段不全 → 确保包含 MUSIC_U 和 __csrf

### Q: Cookie 多久过期？
**A**: 通常 30 天，建议 25 天左右更新一次

### Q: 多账号怎么办？
**A**: 
- 方法 1: 使用不同浏览器
- 方法 2: 使用隐私模式
- 方法 3: 清除 Cookie 后重新登录

### Q: 安全吗？会被盗号吗？
**A**: 
- ✅ Cookie 只在本地使用
- ✅ 不会上传到任何服务器
- ⚠️ 不要分享给他人
- ⚠️ 不要上传到 GitHub

---

## 📞 需要帮助？

如果还有问题：

1. 查看完整文档：[docs/COOKIE_GUIDE.md](docs/COOKIE_GUIDE.md)
2. 提交 Issue: https://github.com/yourusername/autosignin/issues
3. 查看示例：[config/accounts.yaml.example](config/accounts.yaml.example)

---

**🎉 祝你使用愉快！**
