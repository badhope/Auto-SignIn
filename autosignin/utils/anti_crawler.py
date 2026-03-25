"""
反反爬虫机制模块
实现多种反反爬虫策略，包括User-Agent随机化、代理IP池、请求间隔控制、验证码识别等
"""

import random
import time
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import asyncio


class AntiCrawlerStrategy(Enum):
    """反爬虫策略枚举"""
    USER_AGENT_RANDOM = "user_agent_random"
    PROXY_POOL = "proxy_pool"
    REQUEST_INTERVAL = "request_interval"
    CAPTCHA_SOLVER = "captcha_solver"
    BEHAVIOR_SIMULATION = "behavior_simulation"
    HEADER_ROTATION = "header_rotation"
    COOKIE_ROTATION = "cookie_rotation"
    REFERER_SPOOF = "referer_spoof"


@dataclass
class PlatformAntiCrawlerInfo:
    """平台反爬虫信息"""
    platform: str
    display_name: str
    anti_crawler_measures: List[str]
    risk_level: str
    recommended_strategies: List[AntiCrawlerStrategy]
    request_limits: Dict[str, Any]
    notes: str


@dataclass
class ProxyInfo:
    """代理信息"""
    host: str
    port: int
    protocol: str = "http"
    username: Optional[str] = None
    password: Optional[str] = None
    expire_time: Optional[str] = None
    region: Optional[str] = None
    speed: Optional[float] = None
    success_rate: Optional[float] = None
    
    def to_proxy_dict(self) -> Dict[str, str]:
        if self.username and self.password:
            proxy_url = f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            proxy_url = f"{self.protocol}://{self.host}:{self.port}"
        
        return {
            "http": proxy_url,
            "https": proxy_url
        }


class UserAgentPool:
    """User-Agent池"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._user_agents = self._load_user_agents()
        self._last_used = {}
    
    def _load_user_agents(self) -> Dict[str, List[str]]:
        return {
            "chrome": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            ],
            "firefox": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            ],
            "safari": [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            ],
            "edge": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            ],
            "mobile": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            ]
        }
    
    def get_random(self, browser_type: str = None) -> str:
        if browser_type and browser_type in self._user_agents:
            return random.choice(self._user_agents[browser_type])
        
        all_user_agents = []
        for agents in self._user_agents.values():
            all_user_agents.extend(agents)
        return random.choice(all_user_agents)
    
    def get_for_platform(self, platform: str) -> str:
        platform_preferences = {
            "bilibili": "chrome",
            "netease_music": "chrome",
            "zhihu": "chrome",
            "juejin": "chrome",
            "v2ex": "chrome",
            "weibo": "mobile",
            "douyin": "mobile",
            "xiaohongshu": "mobile"
        }
        
        browser_type = platform_preferences.get(platform, "chrome")
        return self.get_random(browser_type)


class ProxyPool:
    """代理IP池"""
    
    def __init__(self):
        self._proxies: List[ProxyInfo] = []
        self._failed_proxies: set = set()
        self._current_index = 0
    
    def add_proxy(self, proxy: ProxyInfo):
        self._proxies.append(proxy)
    
    def add_proxies_from_file(self, file_path: str, protocol: str = "http"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"代理文件不存在: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                parts = line.split(":")
                if len(parts) >= 2:
                    proxy = ProxyInfo(
                        host=parts[0],
                        port=int(parts[1]),
                        protocol=protocol
                    )
                    if len(parts) >= 4:
                        proxy.username = parts[2]
                        proxy.password = parts[3]
                    self.add_proxy(proxy)
    
    def get_proxy(self) -> Optional[ProxyInfo]:
        available = [p for p in self._proxies if id(p) not in self._failed_proxies]
        
        if not available:
            self._failed_proxies.clear()
            available = self._proxies
        
        if not available:
            return None
        
        self._current_index = (self._current_index + 1) % len(available)
        return available[self._current_index]
    
    def mark_failed(self, proxy: ProxyInfo):
        self._failed_proxies.add(id(proxy))
    
    def mark_success(self, proxy: ProxyInfo):
        self._failed_proxies.discard(id(proxy))
    
    def get_count(self) -> Dict[str, int]:
        return {
            "total": len(self._proxies),
            "available": len(self._proxies) - len(self._failed_proxies),
            "failed": len(self._failed_proxies)
        }
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ProxyPool":
        pool = cls()
        
        if "file" in config:
            pool.add_proxies_from_file(
                config["file"],
                config.get("protocol", "http")
            )
        
        if "proxies" in config:
            for proxy_config in config["proxies"]:
                proxy = ProxyInfo(
                    host=proxy_config["host"],
                    port=proxy_config["port"],
                    protocol=proxy_config.get("protocol", "http"),
                    username=proxy_config.get("username"),
                    password=proxy_config.get("password")
                )
                pool.add_proxy(proxy)
        
        return pool


class RequestIntervalController:
    """请求间隔控制器"""
    
    def __init__(
        self,
        min_interval: float = 1.0,
        max_interval: float = 3.0,
        adaptive: bool = True
    ):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.adaptive = adaptive
        self._last_request_time = 0
        self._request_count = 0
        self._failure_count = 0
        self._current_interval = min_interval
    
    def wait(self):
        elapsed = time.time() - self._last_request_time
        
        if elapsed < self._current_interval:
            sleep_time = self._current_interval - elapsed
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
        self._request_count += 1
        
        if self.adaptive:
            self._adjust_interval()
    
    async def async_wait(self):
        elapsed = time.time() - self._last_request_time
        
        if elapsed < self._current_interval:
            sleep_time = self._current_interval - elapsed
            await asyncio.sleep(sleep_time)
        
        self._last_request_time = time.time()
        self._request_count += 1
        
        if self.adaptive:
            self._adjust_interval()
    
    def _adjust_interval(self):
        if self._request_count % 10 == 0 and self._failure_count > 0:
            failure_rate = self._failure_count / self._request_count
            if failure_rate > 0.3:
                self._current_interval = min(
                    self._current_interval * 1.5,
                    self.max_interval
                )
            elif failure_rate < 0.1:
                self._current_interval = max(
                    self._current_interval * 0.9,
                    self.min_interval
                )
    
    def record_failure(self):
        self._failure_count += 1
    
    def record_success(self):
        pass
    
    def get_random_interval(self) -> float:
        return random.uniform(self.min_interval, self.max_interval)


class CaptchaSolver:
    """验证码识别器"""
    
    def __init__(self, solver_type: str = "ddddocr"):
        self.solver_type = solver_type
        self._ddddocr = None
        self._ocr = None
    
    def _init_ddddocr(self):
        if self._ddddocr is None:
            try:
                import ddddocr
                self._ddddocr = ddddocr
                self._ocr = ddddocr.DdddOcr()
            except ImportError:
                raise ImportError(
                    "ddddocr库未安装，请运行: pip install ddddocr"
                )
    
    def solve_image(self, image_data: bytes) -> str:
        if self.solver_type == "ddddocr":
            return self._solve_with_ddddocr(image_data)
        else:
            raise ValueError(f"不支持的验证码识别类型: {self.solver_type}")
    
    def _solve_with_ddddocr(self, image_data: bytes) -> str:
        self._init_ddddocr()
        return self._ocr.classification(image_data)
    
    def solve_slider(
        self,
        background_image: bytes,
        slider_image: bytes
    ) -> int:
        self._init_ddddocr()
        det = self._ddddocr.DdddOcr(det=False, ocr=False)
        return det.slide_match(slider_image, background_image, simple_target=True)


class BehaviorSimulator:
    """用户行为模拟器"""
    
    def __init__(self):
        self._mouse_positions: List[tuple] = []
        self._scroll_positions: List[int] = []
    
    def generate_mouse_path(
        self,
        start: tuple,
        end: tuple,
        steps: int = 20
    ) -> List[tuple]:
        path = []
        
        x_step = (end[0] - start[0]) / steps
        y_step = (end[1] - start[1]) / steps
        
        for i in range(steps + 1):
            progress = i / steps
            ease = self._ease_out_quad(progress)
            
            x = start[0] + (end[0] - start[0]) * ease
            y = start[1] + (end[1] - start[1]) * ease
            
            x += random.uniform(-2, 2)
            y += random.uniform(-2, 2)
            
            path.append((int(x), int(y)))
        
        return path
    
    def _ease_out_quad(self, t: float) -> float:
        return 1 - (1 - t) ** 2
    
    def generate_scroll_pattern(
        self,
        total_distance: int,
        direction: str = "down"
    ) -> List[int]:
        positions = [0]
        current = 0
        
        while current < total_distance:
            step = random.randint(50, 200)
            current = min(current + step, total_distance)
            positions.append(current)
            
            if random.random() < 0.2:
                positions.append(current - random.randint(10, 30))
                positions.append(current)
        
        return positions
    
    def generate_reading_time(self, content_length: int) -> float:
        base_time = content_length / 500
        variation = random.uniform(0.5, 1.5)
        return base_time * variation
    
    def generate_typing_pattern(self, text: str) -> List[float]:
        intervals = []
        
        for i, char in enumerate(text):
            if char == " ":
                interval = random.uniform(0.15, 0.3)
            elif char in ".,!?":
                interval = random.uniform(0.3, 0.5)
            else:
                interval = random.uniform(0.05, 0.15)
            
            if random.random() < 0.1:
                interval += random.uniform(0.1, 0.3)
            
            intervals.append(interval)
        
        return intervals


class HeaderRotator:
    """请求头轮换器"""
    
    def __init__(self):
        self._accept_headers = [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        ]
        
        self._accept_languages = [
            "zh-CN,zh;q=0.9,en;q=0.8",
            "zh-CN,zh;q=0.9",
            "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        ]
        
        self._accept_encodings = [
            "gzip, deflate, br",
            "gzip, deflate",
        ]
    
    def get_headers(self, user_agent: str, referer: str = None) -> Dict[str, str]:
        headers = {
            "User-Agent": user_agent,
            "Accept": random.choice(self._accept_headers),
            "Accept-Language": random.choice(self._accept_languages),
            "Accept-Encoding": random.choice(self._accept_encodings),
            "Connection": "keep-alive",
            "Cache-Control": random.choice(["max-age=0", "no-cache"]),
        }
        
        if referer:
            headers["Referer"] = referer
        
        return headers
    
    def get_platform_headers(self, platform: str) -> Dict[str, str]:
        platform_configs = {
            "bilibili": {
                "Referer": "https://www.bilibili.com/",
                "Origin": "https://www.bilibili.com",
            },
            "netease_music": {
                "Referer": "https://music.163.com/",
            },
            "zhihu": {
                "Referer": "https://www.zhihu.com/",
            },
            "juejin": {
                "Referer": "https://juejin.cn/",
            },
            "v2ex": {
                "Referer": "https://www.v2ex.com/",
            },
        }
        
        return platform_configs.get(platform, {})


class AntiCrawlerManager:
    """反反爬虫管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.user_agent_pool = UserAgentPool()
        self.proxy_pool = ProxyPool()
        self.interval_controller = RequestIntervalController()
        self.captcha_solver = CaptchaSolver()
        self.behavior_simulator = BehaviorSimulator()
        self.header_rotator = HeaderRotator()
        
        if "proxy" in self.config:
            self.proxy_pool = ProxyPool.from_config(self.config["proxy"])
        
        if "interval" in self.config:
            self.interval_controller = RequestIntervalController(
                min_interval=self.config["interval"].get("min", 1.0),
                max_interval=self.config["interval"].get("max", 3.0)
            )
    
    def get_request_config(self, platform: str) -> Dict[str, Any]:
        user_agent = self.user_agent_pool.get_for_platform(platform)
        headers = self.header_rotator.get_headers(user_agent)
        platform_headers = self.header_rotator.get_platform_headers(platform)
        headers.update(platform_headers)
        
        config = {
            "headers": headers,
            "timeout": self.config.get("timeout", 30),
        }
        
        proxy = self.proxy_pool.get_proxy()
        if proxy:
            config["proxies"] = proxy.to_proxy_dict()
        
        return config
    
    def before_request(self, platform: str = None):
        self.interval_controller.wait()
    
    async def async_before_request(self, platform: str = None):
        await self.interval_controller.async_wait()
    
    def after_request(self, success: bool, proxy: ProxyInfo = None):
        if success:
            self.interval_controller.record_success()
            if proxy:
                self.proxy_pool.mark_success(proxy)
        else:
            self.interval_controller.record_failure()
            if proxy:
                self.proxy_pool.mark_failed(proxy)
    
    def solve_captcha(self, image_data: bytes) -> str:
        return self.captcha_solver.solve_image(image_data)


class PlatformAntiCrawlerRegistry:
    """平台反爬虫信息注册表"""
    
    _platforms: Dict[str, PlatformAntiCrawlerInfo] = {}
    
    @classmethod
    def register(cls, info: PlatformAntiCrawlerInfo):
        cls._platforms[info.platform] = info
    
    @classmethod
    def get(cls, platform: str) -> Optional[PlatformAntiCrawlerInfo]:
        return cls._platforms.get(platform)
    
    @classmethod
    def get_all(cls) -> List[PlatformAntiCrawlerInfo]:
        return list(cls._platforms.values())
    
    @classmethod
    def initialize(cls):
        platforms_data = [
            {
                "platform": "bilibili",
                "display_name": "哔哩哔哩",
                "anti_crawler_measures": [
                    "User-Agent检测",
                    "Referer验证",
                    "请求频率限制",
                    "Cookie有效性检测",
                    "风控系统（账号异常检测）"
                ],
                "risk_level": "中等",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                    AntiCrawlerStrategy.HEADER_ROTATION,
                ],
                "request_limits": {
                    "max_requests_per_minute": 60,
                    "max_requests_per_hour": 1000,
                },
                "notes": "B站风控较严格，建议使用真实Cookie，避免频繁请求"
            },
            {
                "platform": "netease_music",
                "display_name": "网易云音乐",
                "anti_crawler_measures": [
                    "请求签名验证",
                    "Cookie验证",
                    "请求频率限制",
                    "IP限制"
                ],
                "risk_level": "中等",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                ],
                "request_limits": {
                    "max_requests_per_minute": 30,
                },
                "notes": "网易云API需要签名，建议使用官方接口"
            },
            {
                "platform": "zhihu",
                "display_name": "知乎",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "验证码（频繁访问时）",
                    "登录状态检测",
                    "反爬虫JS检测"
                ],
                "risk_level": "较高",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                    AntiCrawlerStrategy.CAPTCHA_SOLVER,
                ],
                "request_limits": {
                    "max_requests_per_minute": 20,
                },
                "notes": "知乎反爬较严格，频繁访问会触发验证码"
            },
            {
                "platform": "juejin",
                "display_name": "掘金",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "Cookie验证",
                    "User-Agent检测"
                ],
                "risk_level": "低",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                ],
                "request_limits": {
                    "max_requests_per_minute": 60,
                },
                "notes": "掘金反爬相对宽松，正常请求即可"
            },
            {
                "platform": "v2ex",
                "display_name": "V2EX",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "登录状态检测",
                    "IP限制"
                ],
                "risk_level": "低",
                "recommended_strategies": [
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                ],
                "request_limits": {
                    "max_requests_per_minute": 30,
                },
                "notes": "V2EX对未登录用户限制较严格"
            },
            {
                "platform": "weibo",
                "display_name": "微博",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "验证码",
                    "登录状态检测",
                    "IP封禁",
                    "风控系统"
                ],
                "risk_level": "高",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.PROXY_POOL,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                    AntiCrawlerStrategy.CAPTCHA_SOLVER,
                ],
                "request_limits": {
                    "max_requests_per_minute": 10,
                },
                "notes": "微博反爬非常严格，建议使用代理池"
            },
            {
                "platform": "douyin",
                "display_name": "抖音",
                "anti_crawler_measures": [
                    "请求签名验证",
                    "设备指纹检测",
                    "请求频率限制",
                    "验证码",
                    "风控系统"
                ],
                "risk_level": "高",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.PROXY_POOL,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                    AntiCrawlerStrategy.BEHAVIOR_SIMULATION,
                ],
                "request_limits": {
                    "max_requests_per_minute": 20,
                },
                "notes": "抖音反爬非常严格，需要设备签名"
            },
            {
                "platform": "xiaohongshu",
                "display_name": "小红书",
                "anti_crawler_measures": [
                    "请求签名验证",
                    "设备指纹检测",
                    "请求频率限制",
                    "验证码"
                ],
                "risk_level": "高",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.PROXY_POOL,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                ],
                "request_limits": {
                    "max_requests_per_minute": 15,
                },
                "notes": "小红书需要签名和设备指纹"
            },
            {
                "platform": "tieba",
                "display_name": "百度贴吧",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "验证码",
                    "登录状态检测",
                    "BDUSS验证"
                ],
                "risk_level": "中等",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                    AntiCrawlerStrategy.CAPTCHA_SOLVER,
                ],
                "request_limits": {
                    "max_requests_per_minute": 30,
                },
                "notes": "贴吧需要BDUSS Cookie"
            },
            {
                "platform": "csdn",
                "display_name": "CSDN",
                "anti_crawler_measures": [
                    "请求频率限制",
                    "登录状态检测",
                    "验证码（部分操作）"
                ],
                "risk_level": "低",
                "recommended_strategies": [
                    AntiCrawlerStrategy.USER_AGENT_RANDOM,
                    AntiCrawlerStrategy.REQUEST_INTERVAL,
                ],
                "request_limits": {
                    "max_requests_per_minute": 60,
                },
                "notes": "CSDN反爬相对宽松"
            },
        ]
        
        for data in platforms_data:
            info = PlatformAntiCrawlerInfo(
                platform=data["platform"],
                display_name=data["display_name"],
                anti_crawler_measures=data["anti_crawler_measures"],
                risk_level=data["risk_level"],
                recommended_strategies=data["recommended_strategies"],
                request_limits=data["request_limits"],
                notes=data["notes"]
            )
            cls.register(info)


PlatformAntiCrawlerRegistry.initialize()


def get_platform_anti_crawler_info(platform: str) -> Optional[Dict[str, Any]]:
    """获取平台反爬虫信息"""
    info = PlatformAntiCrawlerRegistry.get(platform)
    if info:
        return {
            "platform": info.platform,
            "display_name": info.display_name,
            "anti_crawler_measures": info.anti_crawler_measures,
            "risk_level": info.risk_level,
            "recommended_strategies": [s.value for s in info.recommended_strategies],
            "request_limits": info.request_limits,
            "notes": info.notes
        }
    return None


def get_all_platforms_info() -> List[Dict[str, Any]]:
    """获取所有平台反爬虫信息"""
    return [
        get_platform_anti_crawler_info(p.platform)
        for p in PlatformAntiCrawlerRegistry.get_all()
    ]
