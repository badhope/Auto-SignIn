# 更新日志

所有重要的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [2.1.0] - 2026-03-24

### ✨ 新增

- Phase 0: Cookie 健康检查工具 (`autosignin.core.health`)
- Phase 1: 页面内容分析器 (`autosignin.core.page_analyzer`)
  - 跳转广告检测
  - UI 变化检测
  - 登录失效检测
  - 验证码拦截检测
  - 频率限制检测
- Phase 2: 健康检查与自动恢复
  - 系统健康检查器 (`autosignin.core.system_health`)
  - 自动恢复机制 (`autosignin.core.recovery`)
  - 指标收集器 (`MetricsCollector`)
- CLI `health` 命令
- SignInEngine 优雅关闭 (`graceful_shutdown`)

### 🔧 改进

- 调度器优雅关闭
- CLI run 命令集成优雅关闭

## [2.0.0] - 2026-03-24

### ✨ 新增

- 插件架构重构
- 支持知乎、掘金、V2EX 平台
- 容错机制 (重试、熔断、限流、舱壁隔离)
- 响应式设计

### 🔧 改进

- 异步请求优化
- 错误处理完善
- 日志规范化

## [1.0.0] - 2024-XX-XX

### ✨ 新增

- 基础框架搭建
- 支持哔哩哔哩签到
- 支持网易云音乐签到
- 定时任务调度
- 多种通知方式（钉钉、Server酱、PushPlus）
- Docker 支持
- 多账号管理

### 🔧 功能

- 可配置化设计
- 日志记录
- 异步请求
- 错误处理

## [0.1.0] - 2024-XX-XX

### 🎉 初始版本

- 项目初始化
- 基础结构搭建
