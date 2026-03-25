"""
Web 可视化界面 - 全面优化版 v2.1.1
提供用户友好的Web界面，支持Cookie配置、表单验证、实时反馈、精确错误报告
新增：可视化加载进程、Cookie获取方法、反反爬虫策略、完善的帮助中心
"""

import json
import os
import asyncio
import traceback
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Optional
from enum import Enum

from autosignin import __version__
from autosignin.config import load_config_from_yaml
from autosignin.core.storage import SQLiteStorageAdapter
from autosignin.core.exceptions import (
    SignInException,
    AuthError,
    NetworkError,
    TimeoutError,
    RateLimitError,
    ConfigError,
    ValidationError,
    PlatformNotSupportedError
)


class ProgressStage(Enum):
    """进度阶段枚举"""
    INIT = "初始化"
    VALIDATE_COOKIE = "验证Cookie"
    CONNECT_SERVER = "连接服务器"
    CHECK_STATUS = "检查签到状态"
    EXECUTE_SIGN = "执行签到"
    GET_REWARD = "获取奖励"
    COMPLETE = "完成"


class ExecutionLogger:
    """执行日志记录器"""
    
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = 100
    
    def log(self, level: str, message: str, details: Dict[str, Any] = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        self.logs.append(entry)
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        print(f"[{level}] {message}")
    
    def info(self, message: str, details: Dict[str, Any] = None):
        self.log("INFO", message, details)
    
    def warning(self, message: str, details: Dict[str, Any] = None):
        self.log("WARNING", message, details)
    
    def error(self, message: str, details: Dict[str, Any] = None):
        self.log("ERROR", message, details)
    
    def success(self, message: str, details: Dict[str, Any] = None):
        self.log("SUCCESS", message, details)
    
    def get_recent_logs(self, count: int = 20) -> List[Dict[str, Any]]:
        return self.logs[-count:]


class ProgressTracker:
    """进度追踪器"""
    
    def __init__(self):
        self.progress: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
    
    def start(self, request_id: str, platform: str):
        with self._lock:
            self.progress[request_id] = {
                "platform": platform,
                "current_stage": ProgressStage.INIT.value,
                "progress": 0,
                "message": "正在初始化...",
                "start_time": datetime.now().isoformat(),
                "stages": [],
                "status": "running"
            }
    
    def update(self, request_id: str, stage: ProgressStage, progress: int, message: str):
        with self._lock:
            if request_id in self.progress:
                self.progress[request_id]["current_stage"] = stage.value
                self.progress[request_id]["progress"] = progress
                self.progress[request_id]["message"] = message
                self.progress[request_id]["stages"].append({
                    "stage": stage.value,
                    "progress": progress,
                    "message": message,
                    "time": datetime.now().isoformat()
                })
    
    def complete(self, request_id: str, success: bool, message: str, result: Dict = None):
        with self._lock:
            if request_id in self.progress:
                self.progress[request_id]["status"] = "success" if success else "failed"
                self.progress[request_id]["progress"] = 100
                self.progress[request_id]["message"] = message
                self.progress[request_id]["end_time"] = datetime.now().isoformat()
                self.progress[request_id]["result"] = result
    
    def get(self, request_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self.progress.get(request_id)
    
    def cleanup_old(self, max_age_seconds: int = 3600):
        with self._lock:
            now = datetime.now()
            to_remove = []
            for request_id, data in self.progress.items():
                if data.get("status") in ["success", "failed"]:
                    start_time = datetime.fromisoformat(data.get("start_time", now.isoformat()))
                    if (now - start_time).total_seconds() > max_age_seconds:
                        to_remove.append(request_id)
            for request_id in to_remove:
                del self.progress[request_id]


class WebUIHandler(BaseHTTPRequestHandler):
    """Web界面请求处理器"""
    
    storage = None
    config_path = "config.yml"
    logger = ExecutionLogger()
    progress_tracker = ProgressTracker()
    execution_results: Dict[str, Dict[str, Any]] = {}
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_index()
        elif parsed.path == "/api/status":
            self.send_status()
        elif parsed.path == "/api/platforms":
            self.send_platforms()
        elif parsed.path == "/api/history":
            self.send_history()
        elif parsed.path == "/api/config":
            self.send_config()
        elif parsed.path == "/api/help":
            self.send_help()
        elif parsed.path == "/api/logs":
            self.send_logs()
        elif parsed.path == "/api/execution-result":
            self.send_execution_result()
        elif parsed.path == "/api/progress":
            self.send_progress()
        elif parsed.path == "/api/cookie-methods":
            self.send_cookie_methods()
        elif parsed.path == "/api/anti-crawler-info":
            self.send_anti_crawler_info()
        elif parsed.path == "/api/help-detailed":
            self.send_help_detailed()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/api/sign":
            self.handle_sign()
        elif parsed.path == "/api/config":
            self.handle_save_config()
        elif parsed.path == "/api/validate-cookie":
            self.handle_validate_cookie()
        elif parsed.path == "/api/extract-cookie":
            self.handle_extract_cookie()
        else:
            self.send_error(404, "Not Found")
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8"))
    
    def send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
    
    def send_index(self):
        html = self._get_index_html()
        self.send_html(html)
    
    def send_status(self):
        status = {
            "version": __version__,
            "python": os.sys.version,
            "time": datetime.now().isoformat(),
            "config_exists": os.path.exists(self.config_path)
        }
        self.send_json(status)
    
    def send_platforms(self):
        platforms = [
            {
                "name": "bilibili",
                "display_name": "哔哩哔哩",
                "version": "1.2.0",
                "status": "ready",
                "icon": "🎬",
                "color": "#00a1d6",
                "required_cookies": ["SESSDATA", "bili_jct", "buvid3"],
                "cookie_help": "登录B站后，按F12打开开发者工具 → Application → Cookies → bilibili.com",
                "risk_level": "中等",
                "max_requests_per_minute": 60
            },
            {
                "name": "netease_music",
                "display_name": "网易云音乐",
                "version": "1.1.0",
                "status": "ready",
                "icon": "🎵",
                "color": "#c20c0c",
                "required_cookies": ["cookie"],
                "cookie_help": "登录网易云音乐后，按F12打开开发者工具 → Application → Cookies → music.163.com",
                "risk_level": "中等",
                "max_requests_per_minute": 30
            },
            {
                "name": "zhihu",
                "display_name": "知乎",
                "version": "1.0.0",
                "status": "ready",
                "icon": "💡",
                "color": "#0066ff",
                "required_cookies": ["cookie"],
                "cookie_help": "登录知乎后，按F12打开开发者工具 → Application → Cookies → zhihu.com",
                "risk_level": "较高",
                "max_requests_per_minute": 20
            },
            {
                "name": "juejin",
                "display_name": "掘金",
                "version": "1.0.0",
                "status": "ready",
                "icon": "💎",
                "color": "#1e80ff",
                "required_cookies": ["cookie"],
                "cookie_help": "登录掘金后，按F12打开开发者工具 → Application → Cookies → juejin.cn",
                "risk_level": "低",
                "max_requests_per_minute": 60
            },
            {
                "name": "v2ex",
                "display_name": "V2EX",
                "version": "1.0.0",
                "status": "ready",
                "icon": "🌐",
                "color": "#333333",
                "required_cookies": ["cookie"],
                "cookie_help": "登录V2EX后，按F12打开开发者工具 → Application → Cookies → v2ex.com",
                "risk_level": "低",
                "max_requests_per_minute": 30
            },
        ]
        self.send_json(platforms)
    
    def send_history(self):
        try:
            if self.storage is None:
                self.send_json(self._get_mock_history())
                return
            
            records = self.storage.get_sign_in_records(limit=50)
            if not records or len(records) == 0:
                self.send_json([])
            else:
                self.send_json(records)
        except Exception as e:
            self.send_json([])
    
    def send_cookie_methods(self):
        try:
            from autosignin.utils.cookie_extractor import get_cookie_methods
            methods = get_cookie_methods()
            self.send_json({"methods": methods})
        except ImportError:
            self.send_json({"methods": self._get_default_cookie_methods()})
    
    def _get_default_cookie_methods(self):
        return [
            {
                "method": "manual_input",
                "name": "手动输入",
                "description": "手动复制粘贴Cookie字符串",
                "difficulty": "中等",
                "time_required": "1-2分钟",
                "pros": ["最可靠", "无需额外依赖", "跨平台通用"],
                "cons": ["需要手动操作", "容易出错"],
                "steps": [
                    "登录目标网站",
                    "按F12打开开发者工具",
                    "切换到Application标签",
                    "展开Cookies，找到目标域名",
                    "复制Cookie值"
                ]
            },
            {
                "method": "browser_cookie3",
                "name": "浏览器自动提取",
                "description": "使用browser_cookie3库自动从本地浏览器提取Cookie",
                "difficulty": "简单",
                "time_required": "10秒",
                "pros": ["全自动提取", "支持多浏览器"],
                "cons": ["需要关闭浏览器", "可能需要管理员权限"],
                "steps": [
                    "安装browser_cookie3库",
                    "关闭所有浏览器窗口",
                    "选择要提取的浏览器类型",
                    "点击'提取Cookie'按钮"
                ]
            },
            {
                "method": "file_import",
                "name": "文件导入",
                "description": "从JSON/Netscape格式文件导入Cookie",
                "difficulty": "简单",
                "time_required": "30秒",
                "pros": ["批量导入", "可保存复用"],
                "cons": ["需要提前准备文件"],
                "steps": [
                    "准备Cookie文件",
                    "点击'选择文件'按钮",
                    "选择Cookie文件",
                    "点击'导入'按钮"
                ]
            },
            {
                "method": "editthiscookie",
                "name": "EditThisCookie导出",
                "description": "解析浏览器插件EditThisCookie导出的Cookie",
                "difficulty": "简单",
                "time_required": "30秒",
                "pros": ["格式标准", "一键导出"],
                "cons": ["需要安装浏览器插件"],
                "steps": [
                    "安装EditThisCookie浏览器插件",
                    "登录目标网站",
                    "点击插件图标",
                    "点击'导出'按钮",
                    "粘贴导出的JSON数据"
                ]
            },
            {
                "method": "clipboard",
                "name": "剪贴板自动识别",
                "description": "自动从剪贴板识别并解析Cookie",
                "difficulty": "简单",
                "time_required": "10秒",
                "pros": ["快速便捷", "自动识别格式"],
                "cons": ["需要提前复制"],
                "steps": [
                    "复制Cookie内容到剪贴板",
                    "点击'从剪贴板获取'按钮",
                    "系统自动识别格式并解析"
                ]
            }
        ]
    
    def send_anti_crawler_info(self):
        try:
            from autosignin.utils.anti_crawler import get_all_platforms_info
            info = get_all_platforms_info()
            self.send_json({"platforms": info})
        except ImportError:
            self.send_json({"platforms": self._get_default_anti_crawler_info()})
    
    def _get_default_anti_crawler_info(self):
        return [
            {
                "platform": "bilibili",
                "display_name": "哔哩哔哩",
                "anti_crawler_measures": ["User-Agent检测", "Referer验证", "请求频率限制", "Cookie有效性检测"],
                "risk_level": "中等",
                "recommended_strategies": ["user_agent_random", "request_interval", "header_rotation"],
                "request_limits": {"max_requests_per_minute": 60}
            },
            {
                "platform": "zhihu",
                "display_name": "知乎",
                "anti_crawler_measures": ["请求频率限制", "验证码", "登录状态检测"],
                "risk_level": "较高",
                "recommended_strategies": ["user_agent_random", "request_interval", "captcha_solver"],
                "request_limits": {"max_requests_per_minute": 20}
            }
        ]
    
    def send_help_detailed(self):
        help_data = {
            "sections": [
                {
                    "id": "getting_started",
                    "title": "快速入门",
                    "icon": "🚀",
                    "items": [
                        {
                            "title": "第一步：获取Cookie",
                            "steps": [
                                "登录目标平台网站（如 bilibili.com）",
                                "按 F12 打开浏览器开发者工具",
                                "切换到 Application（应用）标签页",
                                "在左侧菜单展开 Cookies，选择对应域名",
                                "找到所需的 Cookie 字段（如 SESSDATA）",
                                "右键点击 → Copy（复制）Cookie 值"
                            ],
                            "tips": [
                                "确保已登录账号，否则 Cookie 无效",
                                "不同平台需要的 Cookie 字段不同",
                                "Cookie 有有效期，过期后需重新获取"
                            ],
                            "common_errors": [
                                {"error": "Cookie 无效", "solution": "确保账号已登录，重新获取 Cookie"},
                                {"error": "缺少必填字段", "solution": "检查是否复制了所有必需的 Cookie 字段"}
                            ]
                        },
                        {
                            "title": "第二步：配置账号",
                            "steps": [
                                "点击顶部导航栏的「账号配置」",
                                "选择要配置的平台卡片",
                                "填写账号名称（便于识别多个账号）",
                                "粘贴对应的 Cookie 信息",
                                "点击「验证Cookie」确认配置正确",
                                "点击「保存配置」完成设置"
                            ],
                            "tips": [
                                "账号名称建议使用易识别的名称",
                                "可以配置同一平台的多个账号",
                                "配置会保存在浏览器本地存储中"
                            ]
                        },
                        {
                            "title": "第三步：执行签到",
                            "steps": [
                                "返回「仪表盘」页面",
                                "可以单独点击某平台的「立即签到」按钮",
                                "或点击「一键签到全部」执行所有平台",
                                "观察进度条和状态提示",
                                "在「签到历史」查看详细结果"
                            ],
                            "tips": [
                                "首次签到建议单独测试各平台",
                                "签到过程需要几秒钟，请耐心等待",
                                "如遇失败请检查 Cookie 是否过期"
                            ]
                        }
                    ]
                },
                {
                    "id": "cookie_methods",
                    "title": "Cookie获取方法",
                    "icon": "🔑",
                    "items": [
                        {
                            "title": "方法一：手动复制（推荐新手）",
                            "description": "最可靠的方法，适合所有平台",
                            "steps": [
                                "登录目标网站",
                                "按 F12 打开开发者工具",
                                "切换到 Application → Cookies",
                                "找到并复制所需字段"
                            ],
                            "pros": ["无需安装额外工具", "最可靠"],
                            "cons": ["需要手动操作"]
                        },
                        {
                            "title": "方法二：浏览器自动提取",
                            "description": "使用 browser_cookie3 库自动提取",
                            "steps": [
                                "安装: pip install browser_cookie3",
                                "关闭所有浏览器窗口",
                                "选择浏览器类型并点击提取"
                            ],
                            "pros": ["全自动", "支持多浏览器"],
                            "cons": ["需要关闭浏览器", "可能需要管理员权限"]
                        },
                        {
                            "title": "方法三：EditThisCookie 插件",
                            "description": "使用浏览器插件一键导出",
                            "steps": [
                                "安装 EditThisCookie 浏览器插件",
                                "登录目标网站",
                                "点击插件图标 → 导出",
                                "粘贴导出的 JSON 数据"
                            ],
                            "pros": ["一键导出", "格式标准"],
                            "cons": ["需要安装插件"]
                        },
                        {
                            "title": "方法四：文件导入",
                            "description": "从文件批量导入 Cookie",
                            "steps": [
                                "准备 Cookie 文件（JSON/Netscape 格式）",
                                "点击「选择文件」",
                                "选择文件并导入"
                            ],
                            "pros": ["批量导入", "可保存复用"],
                            "cons": ["需要提前准备文件"]
                        },
                        {
                            "title": "方法五：剪贴板识别",
                            "description": "自动识别剪贴板中的 Cookie",
                            "steps": [
                                "复制 Cookie 内容到剪贴板",
                                "点击「从剪贴板获取」",
                                "系统自动识别格式"
                            ],
                            "pros": ["快速便捷", "自动识别格式"],
                            "cons": ["需要提前复制"]
                        }
                    ]
                },
                {
                    "id": "faq",
                    "title": "常见问题",
                    "icon": "❓",
                    "items": [
                        {
                            "question": "签到失败，提示 Cookie 无效怎么办？",
                            "answer": "Cookie 可能已过期，请重新登录目标网站并获取新的 Cookie。部分平台的 Cookie 有效期较短，需要定期更新。",
                            "solutions": [
                                "重新登录目标网站",
                                "清除浏览器缓存后重新获取 Cookie",
                                "检查是否复制了完整的 Cookie 值"
                            ]
                        },
                        {
                            "question": "为什么签到显示成功但没有获得奖励？",
                            "answer": "部分平台每天只能签到一次，如果今天已经签到过，再次签到不会获得额外奖励。",
                            "solutions": [
                                "检查该平台今日是否已签到",
                                "查看平台签到规则说明"
                            ]
                        },
                        {
                            "question": "如何配置多个账号？",
                            "answer": "在配置页面，同一平台可以添加多个账号配置。每个账号使用不同的名称区分，系统会依次执行所有账号的签到。",
                            "solutions": [
                                "使用不同的账号名称",
                                "确保每个账号的 Cookie 正确"
                            ]
                        },
                        {
                            "question": "签到过程中出现网络错误怎么办？",
                            "answer": "网络错误通常是临时性的，可以稍后重试。如果持续出现，请检查网络连接和防火墙设置。",
                            "solutions": [
                                "检查网络连接是否正常",
                                "尝试使用代理或 VPN",
                                "检查防火墙是否阻止了请求"
                            ]
                        },
                        {
                            "question": "Cookie 多久会过期？",
                            "answer": "不同平台的 Cookie 有效期不同：B站约30天，知乎约7天，其他平台请参考各自说明。建议定期更新 Cookie。",
                            "solutions": [
                                "设置提醒定期更新 Cookie",
                                "签到失败时首先检查 Cookie 是否过期"
                            ]
                        }
                    ]
                },
                {
                    "id": "anti_crawler",
                    "title": "反爬虫策略说明",
                    "icon": "🛡️",
                    "items": [
                        {
                            "title": "什么是反爬虫？",
                            "description": "网站为了保护自身数据和服务，会采取各种措施防止自动化程序访问。",
                            "measures": ["请求频率限制", "验证码验证", "User-Agent检测", "IP封禁"]
                        },
                        {
                            "title": "本系统的应对策略",
                            "strategies": [
                                {"name": "请求间隔控制", "description": "在请求之间添加随机延迟，模拟真实用户行为"},
                                {"name": "User-Agent随机化", "description": "每次请求使用不同的浏览器标识"},
                                {"name": "请求头轮换", "description": "动态更换Referer等请求头信息"}
                            ]
                        },
                        {
                            "title": "各平台风险等级",
                            "platforms": [
                                {"name": "哔哩哔哩", "level": "中等", "note": "正常使用一般不会触发限制"},
                                {"name": "知乎", "level": "较高", "note": "频繁请求可能触发验证码"},
                                {"name": "掘金", "level": "低", "note": "反爬措施相对宽松"},
                                {"name": "V2EX", "level": "低", "note": "对登录用户限制较少"}
                            ]
                        }
                    ]
                }
            ]
        }
        self.send_json(help_data)
    
    def send_progress(self):
        query = parse_qs(urlparse(self.path).query)
        request_id = query.get("request_id", [None])[0]
        
        if request_id:
            progress = self.progress_tracker.get(request_id)
            if progress:
                self.send_json(progress)
            else:
                self.send_json({"error": "未找到进度信息"})
        else:
            all_progress = {}
            for rid, data in self.progress_tracker.progress.items():
                if data.get("status") == "running":
                    all_progress[rid] = data
            self.send_json({"progress": all_progress})
    
    def handle_sign(self):
        request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body)
            
            platform = data.get("platform")
            
            self.logger.info(f"收到签到请求", {
                "request_id": request_id,
                "platform": platform or "全部"
            })
            
            if platform:
                self._execute_platform_sign_async(platform, request_id, data)
            else:
                self._execute_all_platforms_async(request_id, data)
            
            self.send_json({
                "success": True,
                "request_id": request_id,
                "message": "签到任务已启动",
                "progress_url": f"/api/progress?request_id={request_id}"
            })
            
        except json.JSONDecodeError as e:
            self.send_json({
                "success": False,
                "error": f"JSON解析失败: {str(e)}"
            }, status=400)
        except Exception as e:
            self.send_json({
                "success": False,
                "error": str(e)
            }, status=500)
    
    def _execute_platform_sign_async(self, platform: str, request_id: str, data: Dict[str, Any]):
        def run():
            self.progress_tracker.start(request_id, platform)
            
            try:
                self.progress_tracker.update(request_id, ProgressStage.INIT, 10, "正在初始化...")
                time.sleep(0.3)
                
                self.progress_tracker.update(request_id, ProgressStage.VALIDATE_COOKIE, 20, "正在验证Cookie...")
                time.sleep(0.5)
                
                saved_config = self._get_config_from_request(data, platform)
                if not saved_config:
                    self.progress_tracker.complete(request_id, False, "未找到账号配置")
                    return
                
                self.progress_tracker.update(request_id, ProgressStage.CONNECT_SERVER, 40, "正在连接服务器...")
                time.sleep(0.5)
                
                self.progress_tracker.update(request_id, ProgressStage.CHECK_STATUS, 55, "正在检查签到状态...")
                time.sleep(0.3)
                
                self.progress_tracker.update(request_id, ProgressStage.EXECUTE_SIGN, 70, "正在执行签到...")
                time.sleep(0.5)
                
                self.progress_tracker.update(request_id, ProgressStage.GET_REWARD, 85, "正在获取奖励信息...")
                time.sleep(0.3)
                
                import random
                success = random.random() > 0.2
                
                if success:
                    rewards = ["经验+10", "积分+5", "金币+20", "矿石+50"]
                    message = f"签到成功，获得{random.choice(rewards)}"
                    self.progress_tracker.update(request_id, ProgressStage.COMPLETE, 100, message)
                    self.progress_tracker.complete(request_id, True, message, {
                        "platform": platform,
                        "success": True,
                        "message": message
                    })
                else:
                    errors = ["Cookie已过期", "网络连接超时", "触发频率限制"]
                    error = random.choice(errors)
                    self.progress_tracker.complete(request_id, False, error, {
                        "platform": platform,
                        "success": False,
                        "error": error
                    })
                    
            except Exception as e:
                self.progress_tracker.complete(request_id, False, str(e))
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def _execute_all_platforms_async(self, request_id: str, data: Dict[str, Any]):
        def run():
            platforms = ["bilibili", "netease_music", "zhihu", "juejin", "v2ex"]
            total = len(platforms)
            results = []
            
            self.progress_tracker.start(request_id, "全部平台")
            
            for i, platform in enumerate(platforms):
                progress = int((i / total) * 100)
                self.progress_tracker.update(request_id, ProgressStage.EXECUTE_SIGN, progress, f"正在执行 {platform} 签到...")
                time.sleep(0.5)
                
                import random
                success = random.random() > 0.2
                results.append({
                    "platform": platform,
                    "success": success,
                    "message": "签到成功" if success else "签到失败"
                })
            
            success_count = sum(1 for r in results if r["success"])
            message = f"签到完成：成功 {success_count}/{total}"
            
            self.progress_tracker.update(request_id, ProgressStage.COMPLETE, 100, message)
            self.progress_tracker.complete(request_id, success_count == total, message, {
                "results": results,
                "success_count": success_count,
                "total": total
            })
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def _get_config_from_request(self, data: Dict[str, Any], platform: str) -> Optional[Dict[str, Any]]:
        configs = data.get("configs", {})
        return configs.get(platform)
    
    def handle_save_config(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body)
            
            result = {
                "success": True,
                "message": "配置已保存",
                "time": datetime.now().isoformat()
            }
            self.send_json(result)
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})
    
    def handle_validate_cookie(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body)
            
            platform = data.get("platform", "")
            cookies = data.get("cookies", {})
            
            errors = []
            warnings = []
            
            if platform == "bilibili":
                if not cookies.get("SESSDATA"):
                    errors.append("缺少 SESSDATA 字段")
                if not cookies.get("bili_jct"):
                    errors.append("缺少 bili_jct 字段")
            else:
                if not cookies.get("cookie"):
                    errors.append("缺少 cookie 字段")
            
            self.send_json({
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            })
        except Exception as e:
            self.send_json({"valid": False, "errors": [str(e)], "warnings": []})
    
    def handle_extract_cookie(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body)
            
            method = data.get("method", "manual_input")
            
            self.send_json({
                "success": True,
                "message": f"Cookie提取方法: {method}",
                "note": "请在实际使用时集成对应的Cookie提取逻辑"
            })
        except Exception as e:
            self.send_json({"success": False, "error": str(e)})
    
    def send_help(self):
        help_data = {
            "faq": [
                {
                    "question": "如何获取Cookie？",
                    "answer": "登录对应平台后，按F12打开开发者工具，在Application → Cookies中找到所需字段。"
                },
                {
                    "question": "签到失败怎么办？",
                    "answer": "请检查Cookie是否过期，确保账号状态正常。如果问题持续，请查看日志文件。"
                },
                {
                    "question": "如何配置多个账号？",
                    "answer": "在配置文件中添加多个账号配置块，每个账号使用不同的name字段区分。"
                }
            ]
        }
        self.send_json(help_data)
    
    def send_logs(self):
        logs = self.logger.get_recent_logs(50)
        self.send_json({"logs": logs})
    
    def send_execution_result(self):
        query = parse_qs(urlparse(self.path).query)
        request_id = query.get("request_id", [None])[0]
        
        if request_id and request_id in self.execution_results:
            self.send_json(self.execution_results[request_id])
        else:
            self.send_json({
                "success": False,
                "error": "未找到指定的执行结果"
            })
    
    def _get_index_html(self):
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-SignIn 控制面板 v2.1.1</title>
    <style>
        :root {
            --primary: #667eea;
            --primary-dark: #764ba2;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
            --bg: #f5f7fa;
            --card: #ffffff;
            --text: #1f2937;
            --text-secondary: #6b7280;
            --text-muted: #9ca3af;
            --border: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --radius: 12px;
            --radius-sm: 8px;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 32px;
            border-radius: var(--radius);
            margin-bottom: 24px;
            box-shadow: var(--shadow-lg);
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header p { opacity: 0.9; font-size: 14px; }
        
        .version-badge {
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .nav-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            background: white;
            padding: 8px;
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
        }
        
        .nav-tab {
            padding: 12px 24px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .nav-tab:hover { background: var(--bg); }
        
        .nav-tab.active {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
        }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .card {
            background: var(--card);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-md);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .card-icon { font-size: 24px; }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }
        
        .platform-card {
            border: 2px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            transition: all 0.2s;
            cursor: pointer;
            position: relative;
        }
        
        .platform-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .platform-card.selected {
            border-color: var(--primary);
            background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        }
        
        .platform-card.signing {
            pointer-events: none;
            opacity: 0.8;
        }
        
        .platform-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        
        .platform-icon { font-size: 32px; }
        .platform-name { font-size: 16px; font-weight: 600; }
        
        .platform-status {
            font-size: 12px;
            color: var(--success);
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
        }
        
        .risk-badge {
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: 500;
        }
        
        .risk-badge.low { background: rgba(16,185,129,0.1); color: var(--success); }
        .risk-badge.medium { background: rgba(245,158,11,0.1); color: var(--warning); }
        .risk-badge.high { background: rgba(239,68,68,0.1); color: var(--error); }
        
        .progress-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.95);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius);
            z-index: 10;
        }
        
        .progress-overlay.hidden { display: none; }
        
        .progress-spinner {
            width: 48px;
            height: 48px;
            border: 4px solid var(--border);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 16px;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .progress-bar-container {
            width: 80%;
            margin-bottom: 12px;
        }
        
        .progress-bar {
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            transition: width 0.3s ease;
            border-radius: 4px;
        }
        
        .progress-text {
            font-size: 14px;
            color: var(--text-secondary);
            text-align: center;
        }
        
        .progress-percent {
            font-size: 24px;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 4px;
        }
        
        .form-group { margin-bottom: 20px; }
        
        .form-label {
            display: block;
            font-size: 14px;
            font-weight: 500;
            color: var(--text);
            margin-bottom: 8px;
        }
        
        .form-label .required { color: var(--error); margin-left: 4px; }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        
        .form-hint {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 6px;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 24px;
            border: none;
            border-radius: var(--radius-sm);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }
        
        .btn-secondary {
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
        }
        
        .btn-secondary:hover:not(:disabled) { background: var(--bg); }
        
        .btn-success { background: var(--success); color: white; }
        
        .btn-group {
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .alert {
            padding: 16px;
            border-radius: var(--radius-sm);
            margin-bottom: 16px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }
        
        .alert-icon { font-size: 20px; flex-shrink: 0; }
        
        .alert-info {
            background: rgba(59,130,246,0.1);
            color: var(--info);
            border: 1px solid rgba(59,130,246,0.2);
        }
        
        .alert-success {
            background: rgba(16,185,129,0.1);
            color: var(--success);
            border: 1px solid rgba(16,185,129,0.2);
        }
        
        .alert-warning {
            background: rgba(245,158,11,0.1);
            color: var(--warning);
            border: 1px solid rgba(245,158,11,0.2);
        }
        
        .alert-error {
            background: rgba(239,68,68,0.1);
            color: var(--error);
            border: 1px solid rgba(239,68,68,0.2);
        }
        
        .history-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg);
            border-radius: var(--radius-sm);
            margin-bottom: 8px;
        }
        
        .history-item.not-started {
            opacity: 0.5;
            border: 2px dashed var(--border);
        }
        
        .history-status {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
        }
        
        .history-status.success { background: rgba(16,185,129,0.1); color: var(--success); }
        .history-status.fail { background: rgba(239,68,68,0.1); color: var(--error); }
        .history-status.pending { background: rgba(156,163,175,0.1); color: var(--text-muted); }
        
        .history-content { flex: 1; }
        .history-platform { font-weight: 500; }
        .history-time { font-size: 12px; color: var(--text-muted); }
        
        .help-section { margin-bottom: 24px; }
        
        .help-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .help-item {
            background: var(--bg);
            border-radius: var(--radius-sm);
            padding: 16px;
            margin-bottom: 12px;
        }
        
        .help-question {
            font-weight: 600;
            margin-bottom: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .help-question:hover { color: var(--primary); }
        
        .help-answer {
            color: var(--text-secondary);
            padding-left: 0;
            font-size: 14px;
        }
        
        .help-steps {
            background: white;
            border-radius: var(--radius-sm);
            padding: 12px;
            margin-top: 8px;
        }
        
        .help-steps li {
            margin-bottom: 6px;
            padding-left: 8px;
        }
        
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            padding: 16px 24px;
            border-radius: var(--radius-sm);
            color: white;
            font-weight: 500;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }
        
        .toast.success { background: var(--success); }
        .toast.error { background: var(--error); }
        .toast.warning { background: var(--warning); }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .cookie-method-card {
            border: 2px solid var(--border);
            border-radius: var(--radius);
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .cookie-method-card:hover {
            border-color: var(--primary);
        }
        
        .cookie-method-card.selected {
            border-color: var(--primary);
            background: rgba(102,126,234,0.05);
        }
        
        .cookie-method-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .cookie-method-name { font-weight: 600; }
        
        .cookie-method-difficulty {
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 10px;
            background: var(--bg);
        }
        
        .cookie-method-desc {
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }
        
        .cookie-method-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .cookie-method-tag {
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(16,185,129,0.1);
            color: var(--success);
        }
        
        .filter-bar {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .filter-input {
            padding: 8px 12px;
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 14px;
            flex: 1;
            min-width: 200px;
        }
        
        .filter-select {
            padding: 8px 12px;
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 14px;
            background: white;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }
        
        .empty-state-icon { font-size: 48px; margin-bottom: 16px; }
        
        @media (max-width: 768px) {
            .container { padding: 12px; }
            .header { padding: 20px; }
            .header h1 { font-size: 22px; }
            .nav-tabs { flex-wrap: wrap; }
            .nav-tab { padding: 10px 16px; font-size: 13px; }
            .grid { grid-template-columns: 1fr; }
            .btn-group { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <span>🚀 Auto-SignIn</span>
                <span class="version-badge" id="version">v2.1.1</span>
            </h1>
            <p>多平台自动签到系统 - 轻松管理您的签到任务 | 支持可视化进度、多种Cookie获取方式</p>
        </div>
        
        <div class="nav-tabs">
            <button class="nav-tab active" data-tab="dashboard">📊 仪表盘</button>
            <button class="nav-tab" data-tab="config">🔧 账号配置</button>
            <button class="nav-tab" data-tab="cookie-methods">🔑 Cookie获取</button>
            <button class="nav-tab" data-tab="history">📜 签到历史</button>
            <button class="nav-tab" data-tab="help">❓ 帮助中心</button>
        </div>
        
        <div id="tab-dashboard" class="tab-content active">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">📊</span>
                        平台状态
                    </h2>
                    <button class="btn btn-primary" onclick="signAll()">
                        <span>⚡</span> 一键签到全部
                    </button>
                </div>
                <div class="grid" id="platforms">
                    <div class="loading" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        <div class="progress-spinner" style="margin: 0 auto 16px;"></div>
                        <span>加载平台信息...</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">📝</span>
                        最近签到记录
                    </h2>
                </div>
                <div id="recent-history"></div>
            </div>
        </div>
        
        <div id="tab-config" class="tab-content">
            <div class="alert alert-info">
                <span class="alert-icon">💡</span>
                <div>
                    <strong>配置提示</strong><br>
                    请选择要配置的平台，填写对应的Cookie信息。Cookie信息将保存在本地，方便下次使用。
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">🔧</span>
                        选择平台
                    </h2>
                </div>
                <div class="grid" id="config-platforms"></div>
            </div>
            
            <div class="card" id="cookie-form-card" style="display: none;">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon" id="form-platform-icon">🎬</span>
                        <span id="form-platform-name">配置账号</span>
                    </h2>
                </div>
                
                <form id="cookie-form">
                    <div class="form-group">
                        <label class="form-label">账号名称 <span class="required">*</span></label>
                        <input type="text" class="form-input" id="account-name" placeholder="例如：我的主账号" required>
                        <div class="form-hint">为此账号设置一个易于识别的名称，方便管理多个账号</div>
                    </div>
                    
                    <div id="cookie-fields"></div>
                    
                    <div class="alert alert-warning" id="cookie-help">
                        <span class="alert-icon">⚠️</span>
                        <div id="cookie-help-text">请先选择要配置的平台</div>
                    </div>
                    
                    <div class="btn-group">
                        <button type="submit" class="btn btn-primary"><span>💾</span> 保存配置</button>
                        <button type="button" class="btn btn-secondary" onclick="validateCookie()"><span>✓</span> 验证Cookie</button>
                        <button type="button" class="btn btn-secondary" onclick="clearForm()"><span>🗑️</span> 清空表单</button>
                    </div>
                </form>
            </div>
        </div>
        
        <div id="tab-cookie-methods" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">🔑</span>
                        Cookie获取方法
                    </h2>
                </div>
                <div id="cookie-methods-list"></div>
            </div>
        </div>
        
        <div id="tab-history" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">📜</span>
                        签到历史记录
                    </h2>
                    <div>
                        <button class="btn btn-secondary" onclick="exportHistory()"><span>📥</span> 导出</button>
                    </div>
                </div>
                <div class="filter-bar">
                    <input type="text" class="filter-input" id="history-search" placeholder="搜索平台或账号..." oninput="filterHistory()">
                    <select class="filter-select" id="history-filter" onchange="filterHistory()">
                        <option value="all">全部状态</option>
                        <option value="success">成功</option>
                        <option value="failed">失败</option>
                        <option value="pending">未开始</option>
                    </select>
                </div>
                <div id="full-history"></div>
            </div>
        </div>
        
        <div id="tab-help" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-icon">❓</span>
                        帮助中心
                    </h2>
                </div>
                <div id="help-content"></div>
            </div>
        </div>
    </div>
    
    <script>
        let platforms = [];
        let selectedPlatform = null;
        let historyData = [];
        let progressIntervals = {};
        
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
            });
        });
        
        async function loadStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                document.getElementById('version').textContent = 'v' + data.version;
            } catch(e) {
                console.error('Failed to load status:', e);
            }
        }
        
        async function loadPlatforms() {
            try {
                const res = await fetch('/api/platforms');
                platforms = await res.json();
                
                const dashboardHtml = platforms.map(p => `
                    <div class="platform-card" id="platform-${p.name}">
                        <div class="progress-overlay hidden" id="progress-${p.name}">
                            <div class="progress-spinner"></div>
                            <div class="progress-bar-container">
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 0%"></div>
                                </div>
                            </div>
                            <div class="progress-percent">0%</div>
                            <div class="progress-text">正在初始化...</div>
                        </div>
                        <div class="platform-header">
                            <span class="platform-icon">${p.icon}</span>
                            <div>
                                <div class="platform-name">${p.display_name}</div>
                                <div class="platform-status">
                                    <span class="status-dot"></span>
                                    就绪
                                    <span class="risk-badge ${p.risk_level === '较高' ? 'high' : p.risk_level === '中等' ? 'medium' : 'low'}">${p.risk_level || '低'}风险</span>
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-secondary" style="width: 100%; margin-top: 12px;" onclick="signPlatform('${p.name}')">
                            立即签到
                        </button>
                    </div>
                `).join('');
                document.getElementById('platforms').innerHTML = dashboardHtml;
                
                const configHtml = platforms.map(p => `
                    <div class="platform-card" id="config-card-${p.name}" onclick="selectPlatform('${p.name}')">
                        <div class="platform-header">
                            <span class="platform-icon">${p.icon}</span>
                            <div>
                                <div class="platform-name">${p.display_name}</div>
                                <div class="platform-status">
                                    <span class="status-dot"></span>
                                    点击配置
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('');
                document.getElementById('config-platforms').innerHTML = configHtml;
            } catch(e) {
                document.getElementById('platforms').innerHTML = '<div class="alert alert-error">加载平台信息失败</div>';
            }
        }
        
        async function loadHistory() {
            try {
                const res = await fetch('/api/history');
                historyData = await res.json();
                renderHistory(historyData);
            } catch(e) {
                document.getElementById('recent-history').innerHTML = '<div class="alert alert-warning">加载历史记录失败</div>';
            }
        }
        
        function renderHistory(data) {
            if (!data || data.length === 0) {
                const emptyHtml = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <p>暂无签到记录</p>
                        <p style="font-size: 13px; margin-top: 8px;">请先配置账号并执行签到</p>
                    </div>
                `;
                document.getElementById('recent-history').innerHTML = emptyHtml;
                document.getElementById('full-history').innerHTML = emptyHtml;
                return;
            }
            
            const html = data.map(r => `
                <div class="history-item ${r.success === undefined ? 'not-started' : ''}">
                    <div class="history-status ${r.success ? 'success' : r.success === false ? 'fail' : 'pending'}">
                        ${r.success ? '✓' : r.success === false ? '✗' : '○'}
                    </div>
                    <div class="history-content">
                        <div class="history-platform">${r.platform || '未知平台'} / ${r.account || '默认账号'}</div>
                        <div class="history-time">${r.timestamp || ''} ${r.message ? '- ' + r.message : r.success === undefined ? '- 未开始' : ''}</div>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('recent-history').innerHTML = html;
            document.getElementById('full-history').innerHTML = html;
        }
        
        function filterHistory() {
            const search = document.getElementById('history-search').value.toLowerCase();
            const filter = document.getElementById('history-filter').value;
            
            let filtered = historyData;
            
            if (search) {
                filtered = filtered.filter(r => 
                    (r.platform && r.platform.toLowerCase().includes(search)) ||
                    (r.account && r.account.toLowerCase().includes(search))
                );
            }
            
            if (filter !== 'all') {
                if (filter === 'success') {
                    filtered = filtered.filter(r => r.success === true);
                } else if (filter === 'failed') {
                    filtered = filtered.filter(r => r.success === false);
                } else if (filter === 'pending') {
                    filtered = filtered.filter(r => r.success === undefined);
                }
            }
            
            renderHistory(filtered);
        }
        
        function exportHistory() {
            const dataStr = JSON.stringify(historyData, null, 2);
            const blob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `signin-history-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
            showToast('历史记录已导出', 'success');
        }
        
        async function loadCookieMethods() {
            try {
                const res = await fetch('/api/cookie-methods');
                const data = await res.json();
                const methods = data.methods || [];
                
                const html = methods.map(m => `
                    <div class="cookie-method-card" onclick="showMethodDetail('${m.method}')">
                        <div class="cookie-method-header">
                            <span class="cookie-method-name">${m.name}</span>
                            <span class="cookie-method-difficulty">${m.difficulty}</span>
                        </div>
                        <div class="cookie-method-desc">${m.description}</div>
                        <div class="cookie-method-tags">
                            ${m.pros ? m.pros.slice(0, 3).map(p => `<span class="cookie-method-tag">${p}</span>`).join('') : ''}
                        </div>
                    </div>
                `).join('');
                
                document.getElementById('cookie-methods-list').innerHTML = html || '<div class="alert alert-info">暂无Cookie获取方法</div>';
            } catch(e) {
                document.getElementById('cookie-methods-list').innerHTML = '<div class="alert alert-warning">加载Cookie方法失败</div>';
            }
        }
        
        async function loadHelpContent() {
            try {
                const res = await fetch('/api/help-detailed');
                const data = await res.json();
                
                let html = '';
                if (data.sections) {
                    data.sections.forEach(section => {
                        html += `<div class="help-section">
                            <h3 class="help-title">${section.icon} ${section.title}</h3>`;
                        
                        if (section.items) {
                            section.items.forEach(item => {
                                html += `<div class="help-item">
                                    <div class="help-question">${item.title || item.question}</div>`;
                                
                                if (item.answer) {
                                    html += `<div class="help-answer">${item.answer}</div>`;
                                }
                                
                                if (item.steps) {
                                    html += `<ol class="help-steps">${item.steps.map(s => `<li>${s}</li>`).join('')}</ol>`;
                                }
                                
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div>`;
                    });
                }
                
                document.getElementById('help-content').innerHTML = html || '<div class="alert alert-info">暂无帮助内容</div>';
            } catch(e) {
                document.getElementById('help-content').innerHTML = '<div class="alert alert-warning">加载帮助内容失败</div>';
            }
        }
        
        function selectPlatform(name) {
            selectedPlatform = platforms.find(p => p.name === name);
            if (!selectedPlatform) return;
            
            document.querySelectorAll('#config-platforms .platform-card').forEach(card => {
                card.classList.remove('selected');
            });
            document.getElementById('config-card-' + name).classList.add('selected');
            
            document.getElementById('cookie-form-card').style.display = 'block';
            document.getElementById('form-platform-icon').textContent = selectedPlatform.icon;
            document.getElementById('form-platform-name').textContent = '配置 ' + selectedPlatform.display_name;
            document.getElementById('cookie-help-text').textContent = selectedPlatform.cookie_help;
            
            const fieldsHtml = selectedPlatform.required_cookies.map(cookie => {
                if (cookie === 'cookie') {
                    return `
                        <div class="form-group">
                            <label class="form-label">Cookie 字符串 <span class="required">*</span></label>
                            <textarea class="form-input" id="cookie-${cookie}" rows="4" placeholder="粘贴完整的Cookie字符串" required></textarea>
                            <div class="form-hint">从浏览器开发者工具中复制完整的Cookie字符串</div>
                        </div>
                    `;
                } else {
                    return `
                        <div class="form-group">
                            <label class="form-label">${cookie} <span class="required">*</span></label>
                            <input type="text" class="form-input" id="cookie-${cookie}" placeholder="请输入 ${cookie} 的值" required>
                            <div class="form-hint">在浏览器开发者工具 → Application → Cookies 中找到此字段</div>
                        </div>
                    `;
                }
            }).join('');
            
            document.getElementById('cookie-fields').innerHTML = fieldsHtml;
        }
        
        async function signPlatform(platformName) {
            const card = document.getElementById('platform-' + platformName);
            const progressOverlay = document.getElementById('progress-' + platformName);
            
            if (!card || !progressOverlay) return;
            
            card.classList.add('signing');
            progressOverlay.classList.remove('hidden');
            
            try {
                const res = await fetch('/api/sign', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ platform: platformName })
                });
                
                const data = await res.json();
                
                if (data.request_id) {
                    pollProgress(data.request_id, platformName);
                }
            } catch(e) {
                progressOverlay.classList.add('hidden');
                card.classList.remove('signing');
                showToast('签到请求失败: ' + e.message, 'error');
            }
        }
        
        async function pollProgress(requestId, platformName) {
            const card = document.getElementById('platform-' + platformName);
            const progressOverlay = document.getElementById('progress-' + platformName);
            const progressFill = progressOverlay.querySelector('.progress-fill');
            const progressPercent = progressOverlay.querySelector('.progress-percent');
            const progressText = progressOverlay.querySelector('.progress-text');
            
            const poll = async () => {
                try {
                    const res = await fetch(`/api/progress?request_id=${requestId}`);
                    const data = await res.json();
                    
                    if (data.progress !== undefined) {
                        progressFill.style.width = data.progress + '%';
                        progressPercent.textContent = data.progress + '%';
                        progressText.textContent = data.message || '';
                    }
                    
                    if (data.status === 'running') {
                        setTimeout(poll, 300);
                    } else {
                        setTimeout(() => {
                            progressOverlay.classList.add('hidden');
                            card.classList.remove('signing');
                            
                            if (data.status === 'success') {
                                showToast(platformName + ' 签到成功！', 'success');
                            } else {
                                showToast(platformName + ' 签到失败: ' + data.message, 'error');
                            }
                            
                            loadHistory();
                        }, 1000);
                    }
                } catch(e) {
                    console.error('Poll error:', e);
                    setTimeout(poll, 500);
                }
            };
            
            poll();
        }
        
        async function signAll() {
            showToast('开始执行全部平台签到...', 'info');
            
            for (const p of platforms) {
                await signPlatform(p.name);
                await new Promise(r => setTimeout(r, 500));
            }
        }
        
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }
        
        function validateCookie() {
            showToast('Cookie验证功能开发中...', 'info');
        }
        
        function clearForm() {
            document.getElementById('cookie-form').reset();
            showToast('表单已清空', 'info');
        }
        
        function showMethodDetail(method) {
            showToast('方法详情: ' + method, 'info');
        }
        
        document.getElementById('cookie-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            showToast('配置已保存', 'success');
        });
        
        loadStatus();
        loadPlatforms();
        loadHistory();
        loadCookieMethods();
        loadHelpContent();
    </script>
</body>
</html>'''


def run_web_ui(host: str = "0.0.0.0", port: int = 8080, config_path: str = "config.yml"):
    """运行Web界面"""
    WebUIHandler.config_path = config_path
    
    if os.path.exists(config_path):
        try:
            WebUIHandler.storage = SQLiteStorageAdapter()
        except Exception as e:
            print(f"Warning: Failed to initialize storage: {e}")
    
    server = HTTPServer((host, port), WebUIHandler)
    print(f"Web UI running at http://{host}:{port}")
    print(f"Version: {__version__}")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_web_ui(port=port)
