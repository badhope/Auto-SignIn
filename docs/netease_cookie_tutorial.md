# 🎵 网易云音乐 Cookie 获取详细教程

> 图文并茂，手把手教你获取 Cookie

---

## 📱 方法一：Chrome/Edge 浏览器（最推荐）

### 步骤 1: 访问网易云音乐

打开浏览器，访问：https://music.163.com

![步骤 1](https://via.placeholder.com/800x400?text=打开网易云音乐官网)

---

### 步骤 2: 登录账号

点击右上角"登录"，使用以下方式之一登录：
- 手机号 + 验证码
- 邮箱 + 密码
- 微信扫码
- QQ 登录

![步骤 2](https://via.placeholder.com/800x400?text=登录账号)

---

### 步骤 3: 打开开发者工具

**方式 A**: 按键盘 `F12` 键  
**方式 B**: 按 `Ctrl + Shift + I`（Mac: `Cmd + Option + I`）  
**方式 C**: 右键点击页面 → 选择"检查"

![步骤 3](https://via.placeholder.com/800x400?text=F12 打开开发者工具)

---

### 步骤 4: 切换到 Console 标签

在开发者工具顶部找到 "Console"（控制台）标签并点击

![步骤 4](https://via.placeholder.com/800x400?text=切换到 Console 标签)

---

### 步骤 5: 执行代码获取 Cookie

在控制台输入以下代码（或复制粘贴），然后按回车：

```javascript
console.log("===== Cookie 获取工具 =====");
console.log("完整 Cookie:");
console.log(document.cookie);
console.log("\n格式化后:");
const cookies = document.cookie.split('; ').map(c => {
  const [name, value] = c.split('=');
  return `  ${name}: ${value.substring(0, 20)}...`;
});
cookies.forEach(c => console.log(c));
console.log("========================");
```

![步骤 5](https://via.placeholder.com/800x400?text=执行代码获取 Cookie)

---

### 步骤 6: 复制 Cookie

控制台会显示类似这样的输出：

```
===== Cookie 获取工具 =====
完整 Cookie:
MUSIC_U=000E19F2EE3D1A8844CC977864B270A0...; __csrf=22f9a8e115d0c00be9b13f09b9cb8e18; NMTID=00OFIiZvuZprRN5OkIjmHeFgOcjrYoAAAGctzehwA

格式化后:
  MUSIC_U: 000E19F2EE3D1A8844CC...
  __csrf: 22f9a8e115d0c00be9b1...
  NMTID: 00OFIiZvuZprRN5OkIjm...
========================
```

**复制"完整 Cookie"那一行的内容**

---

### 步骤 7: 验证 Cookie 格式

检查复制的 Cookie 是否包含：
- ✅ `MUSIC_U=xxx`
- ✅ `__csrf=xxx`
- ✅ 字段之间用 `; `（分号 + 空格）分隔

**正确示例**：
```
MUSIC_U=000E19F2EE3D1A8844CC977864B270A0...; __csrf=22f9a8e115d0c00be9b13f09b9cb8e18; NMTID=00OFIiZvuZprRN5OkIjmHeFgOcjrYoAAAGctzehwA
```

---

## 🦊 方法二：Firefox 浏览器

### 步骤 1-3: 同上

打开 Firefox → 访问 music.163.com → 登录 → 按 F12

---

### 步骤 4: 切换到控制台

点击 "控制台" 标签

---

### 步骤 5: 执行相同代码

复制粘贴上面的 JavaScript 代码

---

## 🌐 方法三：使用浏览器扩展（最简单）

### 安装 EditThisCookie

1. **打开扩展商店**
   - Chrome: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
   - Edge: 同上（支持 Chrome 扩展）
   - Firefox: https://addons.mozilla.org/firefox/addon/cookies-txt/

2. **点击"添加到 Chrome"**

3. **等待安装完成**

---

### 使用扩展

1. **访问网易云音乐并登录**
   - https://music.163.com

2. **点击扩展图标**
   - 浏览器右上角会出现 🍪 图标
   - 点击它

3. **导出 Cookie**
   - 在弹出窗口中点击 "Copy" 按钮
   - 或点击 "Export" → "Copy all cookies"

4. **复制结果**
   - 会自动复制到剪贴板

---

## 📋 方法四：Network 方式（备用）

如果 Console 方式不行，可以用这个方法：

### 步骤 1: 打开 Network 标签

按 F12 后，点击 "Network"（网络）标签

---

### 步骤 2: 清除记录

点击 🗑️ 按钮清空现有记录

---

### 步骤 3: 刷新页面

按 `F5` 或点击刷新按钮

---

### 步骤 4: 找到关键请求

在左侧请求列表中找到：
- 第一个请求（通常是 `www` 或 `music.163.com`）
- 或任何状态码为 200 的请求

---

### 步骤 5: 查看请求头

点击该请求 → 在右侧找到 "Request Headers"（请求头）

---

### 步骤 6: 复制 Cookie

找到 `Cookie:` 字段，复制后面的值

---

## 🔍 Cookie 字段详解

### 必需字段

| 字段 | 说明 | 示例 |
|------|------|------|
| MUSIC_U | 主要认证 Token | `MUSIC_U=000E19F2...` |
| __csrf | CSRF 防护 Token | `__csrf=22f9a8e1...` |

### 可选字段

| 字段 | 说明 | 是否必需 |
|------|------|----------|
| NMTID | 设备 ID | 可选 |
| _ntes_nuid | 用户 ID | 可选 |
| _ntes_nnid | 会话 ID | 可选 |

---

## ✅ 验证 Cookie 是否有效

### 方法 1: 使用命令行工具

```bash
# 添加账号
python -m src.cli.main add netease -u "测试账号" -c "你的 Cookie"

# 执行签到
python -m src.cli.main signin --platform netease

# 查看结果
python -m src.cli.main history
```

如果显示 "✅ 签到成功"，说明 Cookie 有效！

---

### 方法 2: 在线测试

访问：https://music.163.com/api/nuser/account/get

在浏览器控制台执行：

```javascript
fetch('https://music.163.com/api/nuser/account/get', {
  headers: {
    'Cookie': document.cookie
  }
})
.then(r => r.json())
.then(d => console.log(d))
```

如果返回账号信息，说明 Cookie 有效。

---

## ⚠️ 常见问题

### Q1: Cookie 中包含中文怎么办？
**A**: 正常复制即可，系统会自动处理

### Q2: 复制的 Cookie 很长，正常吗？
**A**: 正常！MUSIC_U 本身就很长（200+ 字符）

### Q3: 找不到 __csrf 字段？
**A**: 
- 刷新页面多次
- 访问个人主页（https://music.163.com/user/home）
- 重新登录

### Q4: Cookie 格式不对？
**A**: 确保：
- 字段之间用 `; `（分号 + 空格）分隔
- 没有 "Cookie: " 前缀
- 没有多余的空格或换行

### Q5: 签到失败，提示 Cookie 过期？
**A**: 
- Cookie 有效期 30 天
- 重新登录获取新的 Cookie
- 建议每 25 天更新一次

---

## 🎯 最佳实践

1. **获取时间**: 登录成功后立即获取
2. **保存位置**: 保存到 `.env` 文件或密码管理器
3. **更新提醒**: 设置日历提醒，25 天后更新
4. **多账号**: 使用不同浏览器或隐私模式
5. **安全性**: 不要分享，不要上传 GitHub

---

## 📞 还是不会？

### 视频教程

B 站搜索："Cookie 获取教程"

### 图文帮助

查看完整文档：[docs/COOKIE_GUIDE.md](docs/COOKIE_GUIDE.md)

### 提交问题

GitHub Issues: https://github.com/yourusername/autosignin/issues

---

**🎉 祝你成功获取 Cookie！**

获取到 Cookie 后，就可以开始使用 Auto-SignIn v2 进行自动签到啦！

```bash
# 开始使用
python -m src.cli.main add netease -u "我的账号" -c "你的 Cookie"
python -m src.cli.main signin --all
```
