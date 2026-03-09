# 🍪 Cookie 获取完全指南

> 本指南将教你如何在各个平台获取签到所需的 Cookie

---

## 📋 目录

- [网易云音乐](#网易云音乐)
- [哔哩哔哩](#哔哩哔哩)
- [CSDN](#csdn)
- [淘宝](#淘宝)
- [京东](#京东)
- [常见问题](#常见问题)

---

## 🎵 网易云音乐

### 方法一：浏览器开发者工具（推荐）

**适用浏览器**：Chrome / Edge / Firefox

#### 步骤：

1. **打开网易云音乐官网**
   - 访问：https://music.163.com
   - **不要关闭页面**

2. **登录账号**
   - 点击右上角"登录"
   - 使用手机号/邮箱/扫码登录
   - 确保登录成功（显示用户名）

3. **打开开发者工具**
   - 按 `F12` 键（或右键 → 检查）
   - 切换到 **Network（网络）** 标签
   - 点击 **清除按钮** 🗑️ 清空现有记录

4. **刷新页面**
   - 按 `F5` 或点击刷新按钮
   - 在 Network 标签会看到很多请求

5. **查找关键请求**
   - 在左侧请求列表中找到 `www` 或根路径的请求
   - 点击该请求

6. **复制 Cookie**
   - 在右侧找到 **Request Headers（请求头）**
   - 找到 `Cookie:` 字段
   - **完整复制** Cookie 值（从 `MUSIC_U=` 开始到分号结束）

7. **验证 Cookie**
   ```bash
   # 应该包含以下关键字段
   MUSIC_U=xxx
   __csrf=xxx
   NMTID=xxx（可选）
   ```

#### 示意图：

```
开发者工具
├── Network (网络)
│   ├── Name: www
│   │   ├── Headers (请求头)
│   │   │   ├── Request Headers
│   │   │   │   └── Cookie: MUSIC_U=xxx; __csrf=xxx; NMTID=xxx
```

---

### 方法二：浏览器控制台（快速）

1. **打开网易云音乐并登录**
   - https://music.163.com

2. **打开控制台**
   - 按 `F12`
   - 切换到 **Console（控制台）** 标签

3. **执行 JavaScript 代码**
   ```javascript
   // 复制并粘贴到控制台，按回车
   console.log(document.cookie);
   ```

4. **复制输出结果**
   - 控制台会打印 Cookie 字符串
   - 完整复制即可

---

### 方法三：浏览器扩展（最简单）

**推荐扩展**：
- Chrome: "EditThisCookie"
- Firefox: "Cookies.txt"
- Edge: "Cookie Editor"

#### 使用步骤：

1. **安装扩展**
   - 打开浏览器扩展商店
   - 搜索并安装 "EditThisCookie"

2. **访问网易云音乐**
   - https://music.163.com
   - 登录账号

3. **导出 Cookie**
   - 点击浏览器工具栏的扩展图标 🍪
   - 点击 **"导出"** 或 **"Copy"** 按钮
   - 选择 **"导出为 JSON"** 或 **"Copy all cookies"**

4. **提取关键字段**
   - 如果导出的是 JSON，找到 `MUSIC_U` 和 `__csrf` 字段
   - 拼接成：`MUSIC_U=值; __csrf=值; NMTID=值`

---

### Cookie 字段说明

| 字段名 | 必需 | 说明 | 有效期 |
|--------|------|------|--------|
| MUSIC_U | ✅ | 主要认证 Token | 30 天 |
| __csrf | ✅ | CSRF 防护 Token | 30 天 |
| NMTID | ⚠️ | 设备 ID（可选） | 长期 |

**最小可用 Cookie**：
```
MUSIC_U=你的值; __csrf=你的值
```

---

### 常见问题

**Q: Cookie 多久过期？**
- MUSIC_U: 通常 30 天
- 建议每 25 天更新一次

**Q: 签到失败怎么办？**
- Cookie 可能已过期
- 重新登录获取新 Cookie

**Q: 多个账号怎么办？**
- 每个账号分别登录获取 Cookie
- 使用不同浏览器或隐私模式

---

## 📺 哔哩哔哩

### 方法一：开发者工具

1. **访问 B 站并登录**
   - https://www.bilibili.com

2. **打开开发者工具**
   - 按 `F12`

3. **切换到 Network**
   - 清除现有记录 🗑️
   - 刷新页面

4. **查找请求**
   - 找到 `www.bilibili.com` 请求

5. **复制 Cookie**
   - 在 Request Headers 中找到 Cookie
   - 完整复制

**必需字段**：
```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

---

### 方法二：控制台一键导出

1. **打开 B 站并登录**

2. **打开控制台（F12）**

3. **执行代码**：
   ```javascript
   // 复制粘贴到控制台
   console.log("SESSDATA=" + document.cookie.split('SESSDATA=')[1].split(';')[0] + 
               "; bili_jct=" + document.cookie.split('bili_jct=')[1].split(';')[0]);
   ```

4. **复制输出结果**

---

## 📝 CSDN

### 获取方法

1. **访问 CSDN**
   - https://www.csdn.net

2. **登录账号**

3. **F12 打开开发者工具**

4. **Network → 刷新 → 复制 Cookie**

**必需字段**：
```
uuid_tt_dd=xxx; UserName=xxx; UserInfo=xxx
```

---

## 🛒 淘宝

### 获取方法

1. **访问淘宝**
   - https://www.taobao.com

2. **登录账号**

3. **F12 → Network → 刷新**

4. **找到 / 请求，复制 Cookie**

**必需字段**：
```
cookie2=xxx; _tb_token_=xxx; lg=xxx
```

⚠️ **注意**：淘宝 Cookie 有效期较短（约 7 天）

---

## 📦 京东

### 获取方法

1. **访问京东**
   - https://www.jd.com

2. **登录账号**

3. **F12 → Network → 刷新**

4. **复制 Cookie**

**必需字段**：
```
pt_key=xxx; pt_pin=xxx
```

---

## 🔧 实用工具

### 1. Cookie 编辑器扩展

**Chrome 扩展推荐**：
- [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
- [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

**Firefox 扩展推荐**：
- [Cookies.txt](https://addons.mozilla.org/firefox/addon/cookies-txt/)

### 2. 在线工具

- Cookie 解析：https://www.browserling.com/tools/decode-uri-component
- Cookie 格式化：https://www.freeformatter.com/json-formatter.html

### 3. 命令行工具

```bash
# 使用 curl 获取 Cookie
curl -c cookies.txt https://music.163.com

# 查看 Cookie 文件
cat cookies.txt
```

---

## ⚠️ 注意事项

### 1. Cookie 安全

- ❌ **不要分享** Cookie 给他人
- ❌ **不要上传** 到公开代码仓库
- ✅ 使用 `.env` 文件存储（已添加到 .gitignore）
- ✅ 定期更新 Cookie

### 2. Cookie 有效期

| 平台 | 有效期 | 建议更新周期 |
|------|--------|-------------|
| 网易云音乐 | 30 天 | 25 天 |
| B 站 | 半年 | 5 个月 |
| CSDN | 30 天 | 25 天 |
| 淘宝 | 7 天 | 5 天 |
| 京东 | 30 天 | 25 天 |

### 3. 多账号管理

**方法一：不同浏览器**
- Chrome → 账号 1
- Firefox → 账号 2
- Edge → 账号 3

**方法二：隐私模式**
- 每次用隐私模式登录获取 Cookie
- 获取后关闭隐私窗口

**方法三：浏览器配置文件**
- Chrome 多用户配置
- Firefox 多容器标签

---

## 📱 手机端获取（高级）

### Android + Termux

1. **安装 Termux**
   ```bash
   pkg install curl
   ```

2. **获取 Cookie**
   ```bash
   curl -c cookies.txt -L https://music.163.com
   cat cookies.txt
   ```

### iOS + Shortcut

1. **创建快捷指令**
   - 获取网页内容
   - 提取响应头
   - 解析 Cookie

---

## 🐛 故障排除

### 问题 1: Cookie 格式错误

**症状**：签到提示 Cookie 格式错误

**解决**：
- 确保包含所有必需字段
- 字段之间用分号 + 空格分隔
- 不要有多余的空格或换行

### 问题 2: Cookie 立即失效

**症状**：刚获取的 Cookie 就无法使用

**可能原因**：
- 账号被限制
- IP 地址变化
- 设备指纹变化

**解决**：
- 重新登录
- 使用固定 IP
- 在同一设备获取和使用

### 问题 3: 找不到 Cookie 字段

**症状**：开发者工具中看不到某些字段

**解决**：
- 确保已登录
- 刷新页面多次
- 尝试访问不同页面（如个人主页）

---

## 📚 相关资源

- [MDN: HTTP Cookies](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Cookies)
- [网易云音乐 API 文档](https://github.com/Binaryify/NeteaseCloudMusicApi)
- [B 站 API 文档](https://github.com/SocialSisterYi/bilibili-API-collect)

---

## 💡 小技巧

1. **定时提醒**：设置日历提醒，Cookie 过期前更新
2. **备份 Cookie**：保存到密码管理器（如 1Password）
3. **自动化更新**：写脚本定期自动获取（需要 Selenium）
4. **多环境隔离**：开发、测试、生产使用不同账号

---

**🎉 现在你已经掌握了所有 Cookie 获取技巧！**

如有问题，请查看 [常见问题](#常见问题) 或提交 Issue。
