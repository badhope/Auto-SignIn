"""
Cookie 获取模块 - 支持多种Cookie获取方式
提供浏览器自动提取、手动输入、文件导入等多种Cookie获取方法
"""

import os
import json
import time
import random
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import platform


class CookieMethod(Enum):
    """Cookie获取方法枚举"""
    BROWSER_AUTO = "browser_auto"
    MANUAL_INPUT = "manual_input"
    FILE_IMPORT = "file_import"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    BROWSER_COOKIE3 = "browser_cookie3"
    EDITTHISCOOKIE = "editthiscookie"
    CLIPBOARD = "clipboard"


@dataclass
class CookieMethodDetail:
    """Cookie获取方法详情"""
    method: CookieMethod
    name: str
    description: str
    difficulty: str
    time_required: str
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    platforms: List[str] = field(default_factory=list)


@dataclass
class CookieExtractionResult:
    """Cookie提取结果"""
    success: bool
    cookies: Dict[str, Any]
    method: CookieMethod
    message: str
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CookieExtractor:
    """Cookie提取器基类"""
    
    def __init__(self):
        self.method = CookieMethod.MANUAL_INPUT
    
    def extract(self, **kwargs) -> CookieExtractionResult:
        raise NotImplementedError


class BrowserAutoExtractor(CookieExtractor):
    """浏览器自动提取Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.BROWSER_AUTO
    
    def extract(self, domain: str = None, browser: str = "chrome") -> CookieExtractionResult:
        try:
            cookies = self._extract_from_browser(browser, domain)
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功从{browser}浏览器提取Cookie"
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="浏览器Cookie提取失败",
                error=str(e)
            )
    
    def _extract_from_browser(self, browser: str, domain: str = None) -> Dict[str, Any]:
        cookies = {}
        
        if browser.lower() == "chrome":
            cookies = self._extract_chrome_cookies(domain)
        elif browser.lower() == "firefox":
            cookies = self._extract_firefox_cookies(domain)
        elif browser.lower() == "edge":
            cookies = self._extract_edge_cookies(domain)
        else:
            raise ValueError(f"不支持的浏览器: {browser}")
        
        return cookies
    
    def _extract_chrome_cookies(self, domain: str = None) -> Dict[str, Any]:
        system = platform.system()
        
        if system == "Windows":
            cookie_path = os.path.expanduser(
                "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"
            )
        elif system == "Darwin":
            cookie_path = os.path.expanduser(
                "~/Library/Application Support/Google/Chrome/Default/Cookies"
            )
        else:
            cookie_path = os.path.expanduser(
                "~/.config/google-chrome/Default/Cookies"
            )
        
        if not os.path.exists(cookie_path):
            raise FileNotFoundError(f"Chrome Cookie文件不存在: {cookie_path}")
        
        return {"path": cookie_path, "browser": "chrome", "domain": domain}
    
    def _extract_firefox_cookies(self, domain: str = None) -> Dict[str, Any]:
        system = platform.system()
        
        if system == "Windows":
            cookie_path = os.path.expanduser(
                "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
            )
        elif system == "Darwin":
            cookie_path = os.path.expanduser(
                "~/Library/Application Support/Firefox/Profiles"
            )
        else:
            cookie_path = os.path.expanduser(
                "~/.mozilla/firefox"
            )
        
        if not os.path.exists(cookie_path):
            raise FileNotFoundError(f"Firefox Profile目录不存在: {cookie_path}")
        
        return {"path": cookie_path, "browser": "firefox", "domain": domain}
    
    def _extract_edge_cookies(self, domain: str = None) -> Dict[str, Any]:
        system = platform.system()
        
        if system == "Windows":
            cookie_path = os.path.expanduser(
                "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies"
            )
        else:
            raise OSError("Edge浏览器Cookie提取仅支持Windows系统")
        
        if not os.path.exists(cookie_path):
            raise FileNotFoundError(f"Edge Cookie文件不存在: {cookie_path}")
        
        return {"path": cookie_path, "browser": "edge", "domain": domain}


class BrowserCookie3Extractor(CookieExtractor):
    """使用browser_cookie3库提取Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.BROWSER_COOKIE3
        self._browser_cookie3 = None
    
    def _import_browser_cookie3(self):
        if self._browser_cookie3 is None:
            try:
                import browser_cookie3
                self._browser_cookie3 = browser_cookie3
            except ImportError:
                raise ImportError(
                    "browser_cookie3库未安装，请运行: pip install browser_cookie3"
                )
        return self._browser_cookie3
    
    def extract(self, domain: str = None, browser: str = "chrome") -> CookieExtractionResult:
        try:
            bc = self._import_browser_cookie3()
            
            cookies = {}
            cookie_jar = None
            
            if browser.lower() == "chrome":
                cookie_jar = bc.chrome(domain_name=domain)
            elif browser.lower() == "firefox":
                cookie_jar = bc.firefox(domain_name=domain)
            elif browser.lower() == "edge":
                cookie_jar = bc.edge(domain_name=domain)
            elif browser.lower() == "all":
                cookie_jar = bc.load(domain_name=domain)
            else:
                cookie_jar = bc.chrome(domain_name=domain)
            
            for cookie in cookie_jar:
                cookies[cookie.name] = cookie.value
            
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功使用browser_cookie3从{browser}提取{len(cookies)}个Cookie"
            )
        except ImportError as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="browser_cookie3库未安装",
                error=str(e)
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="browser_cookie3提取失败",
                error=str(e)
            )


class SeleniumExtractor(CookieExtractor):
    """使用Selenium自动化获取Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.SELENIUM
    
    def extract(self, url: str, headless: bool = True, wait_time: int = 30) -> CookieExtractionResult:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--user-agent={self._get_random_user_agent()}")
            
            driver = webdriver.Chrome(options=options)
            
            try:
                driver.get(url)
                time.sleep(2)
                
                WebDriverWait(driver, wait_time).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                selenium_cookies = driver.get_cookies()
                cookies = {}
                for cookie in selenium_cookies:
                    cookies[cookie["name"]] = cookie["value"]
                
                return CookieExtractionResult(
                    success=True,
                    cookies=cookies,
                    method=self.method,
                    message=f"成功使用Selenium获取{len(cookies)}个Cookie"
                )
            finally:
                driver.quit()
                
        except ImportError:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="Selenium库未安装",
                error="请运行: pip install selenium webdriver-manager"
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="Selenium提取失败",
                error=str(e)
            )
    
    def _get_random_user_agent(self) -> str:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        ]
        return random.choice(user_agents)


class PlaywrightExtractor(CookieExtractor):
    """使用Playwright自动化获取Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.PLAYWRIGHT
    
    def extract(self, url: str, headless: bool = True, browser_type: str = "chromium") -> CookieExtractionResult:
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                if browser_type == "chromium":
                    browser = p.chromium.launch(headless=headless)
                elif browser_type == "firefox":
                    browser = p.firefox.launch(headless=headless)
                elif browser_type == "webkit":
                    browser = p.webkit.launch(headless=headless)
                else:
                    browser = p.chromium.launch(headless=headless)
                
                context = browser.new_context(
                    user_agent=self._get_random_user_agent()
                )
                page = context.new_page()
                
                try:
                    page.goto(url, wait_until="networkidle")
                    
                    playwright_cookies = context.cookies()
                    cookies = {}
                    for cookie in playwright_cookies:
                        cookies[cookie["name"]] = cookie["value"]
                    
                    return CookieExtractionResult(
                        success=True,
                        cookies=cookies,
                        method=self.method,
                        message=f"成功使用Playwright获取{len(cookies)}个Cookie"
                    )
                finally:
                    browser.close()
                    
        except ImportError:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="Playwright库未安装",
                error="请运行: pip install playwright && playwright install"
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="Playwright提取失败",
                error=str(e)
            )
    
    def _get_random_user_agent(self) -> str:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        return random.choice(user_agents)


class FileImportExtractor(CookieExtractor):
    """从文件导入Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.FILE_IMPORT
    
    def extract(self, file_path: str, format: str = "json") -> CookieExtractionResult:
        try:
            if not os.path.exists(file_path):
                return CookieExtractionResult(
                    success=False,
                    cookies={},
                    method=self.method,
                    message="文件不存在",
                    error=f"文件路径: {file_path}"
                )
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            cookies = {}
            
            if format.lower() == "json":
                cookies = self._parse_json(content)
            elif format.lower() == "netscape":
                cookies = self._parse_netscape(content)
            elif format.lower() == "header":
                cookies = self._parse_header(content)
            else:
                cookies = self._parse_json(content)
            
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功从文件导入{len(cookies)}个Cookie"
            )
        except json.JSONDecodeError as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="JSON解析失败",
                error=str(e)
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="文件导入失败",
                error=str(e)
            )
    
    def _parse_json(self, content: str) -> Dict[str, str]:
        data = json.loads(content)
        cookies = {}
        
        if isinstance(data, dict):
            if "cookies" in data:
                for cookie in data["cookies"]:
                    if isinstance(cookie, dict) and "name" in cookie and "value" in cookie:
                        cookies[cookie["name"]] = cookie["value"]
            else:
                cookies = data
        elif isinstance(data, list):
            for cookie in data:
                if isinstance(cookie, dict) and "name" in cookie and "value" in cookie:
                    cookies[cookie["name"]] = cookie["value"]
        
        return cookies
    
    def _parse_netscape(self, content: str) -> Dict[str, str]:
        cookies = {}
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("\t")
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]
        return cookies
    
    def _parse_header(self, content: str) -> Dict[str, str]:
        cookies = {}
        for part in content.split(";"):
            part = part.strip()
            if "=" in part:
                name, value = part.split("=", 1)
                cookies[name.strip()] = value.strip()
        return cookies


class EditThisCookieExtractor(CookieExtractor):
    """解析EditThisCookie导出的Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.EDITTHISCOOKIE
    
    def extract(self, json_string: str) -> CookieExtractionResult:
        try:
            data = json.loads(json_string)
            cookies = {}
            
            if isinstance(data, list):
                for cookie in data:
                    if isinstance(cookie, dict) and "name" in cookie and "value" in cookie:
                        cookies[cookie["name"]] = cookie["value"]
            elif isinstance(data, dict):
                if "cookies" in data:
                    for cookie in data["cookies"]:
                        if isinstance(cookie, dict) and "name" in cookie and "value" in cookie:
                            cookies[cookie["name"]] = cookie["value"]
                else:
                    cookies = data
            
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功解析EditThisCookie格式，共{len(cookies)}个Cookie"
            )
        except json.JSONDecodeError as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="JSON解析失败",
                error=str(e)
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="EditThisCookie解析失败",
                error=str(e)
            )


class ManualInputExtractor(CookieExtractor):
    """手动输入Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.MANUAL_INPUT
    
    def extract(self, cookie_string: str, format: str = "header") -> CookieExtractionResult:
        try:
            cookies = {}
            
            if format.lower() == "header":
                cookies = self._parse_header(cookie_string)
            elif format.lower() == "json":
                cookies = json.loads(cookie_string)
            elif format.lower() == "key_value":
                cookies = self._parse_key_value(cookie_string)
            else:
                cookies = self._parse_header(cookie_string)
            
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功解析手动输入的{len(cookies)}个Cookie"
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="手动输入解析失败",
                error=str(e)
            )
    
    def _parse_header(self, content: str) -> Dict[str, str]:
        cookies = {}
        for part in content.split(";"):
            part = part.strip()
            if "=" in part:
                name, value = part.split("=", 1)
                cookies[name.strip()] = value.strip()
        return cookies
    
    def _parse_key_value(self, content: str) -> Dict[str, str]:
        cookies = {}
        for line in content.split("\n"):
            line = line.strip()
            if "=" in line:
                name, value = line.split("=", 1)
                cookies[name.strip()] = value.strip()
        return cookies


class ClipboardExtractor(CookieExtractor):
    """从剪贴板获取Cookie"""
    
    def __init__(self):
        super().__init__()
        self.method = CookieMethod.CLIPBOARD
    
    def extract(self) -> CookieExtractionResult:
        try:
            import pyperclip
            content = pyperclip.paste()
            
            cookies = self._auto_detect_format(content)
            
            return CookieExtractionResult(
                success=True,
                cookies=cookies,
                method=self.method,
                message=f"成功从剪贴板获取{len(cookies)}个Cookie"
            )
        except ImportError:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="pyperclip库未安装",
                error="请运行: pip install pyperclip"
            )
        except Exception as e:
            return CookieExtractionResult(
                success=False,
                cookies={},
                method=self.method,
                message="剪贴板获取失败",
                error=str(e)
            )
    
    def _auto_detect_format(self, content: str) -> Dict[str, str]:
        content = content.strip()
        
        try:
            data = json.loads(content)
            if isinstance(data, (dict, list)):
                cookies = {}
                if isinstance(data, list):
                    for cookie in data:
                        if isinstance(cookie, dict) and "name" in cookie and "value" in cookie:
                            cookies[cookie["name"]] = cookie["value"]
                else:
                    cookies = data
                return cookies
        except json.JSONDecodeError:
            pass
        
        if ";" in content:
            cookies = {}
            for part in content.split(";"):
                part = part.strip()
                if "=" in part:
                    name, value = part.split("=", 1)
                    cookies[name.strip()] = value.strip()
            return cookies
        
        if "\n" in content and "=" in content:
            cookies = {}
            for line in content.split("\n"):
                line = line.strip()
                if "=" in line:
                    name, value = line.split("=", 1)
                    cookies[name.strip()] = value.strip()
            return cookies
        
        return {}


class CookieExtractorFactory:
    """Cookie提取器工厂"""
    
    _extractors = {
        CookieMethod.BROWSER_AUTO: BrowserAutoExtractor,
        CookieMethod.BROWSER_COOKIE3: BrowserCookie3Extractor,
        CookieMethod.SELENIUM: SeleniumExtractor,
        CookieMethod.PLAYWRIGHT: PlaywrightExtractor,
        CookieMethod.FILE_IMPORT: FileImportExtractor,
        CookieMethod.EDITTHISCOOKIE: EditThisCookieExtractor,
        CookieMethod.MANUAL_INPUT: ManualInputExtractor,
        CookieMethod.CLIPBOARD: ClipboardExtractor,
    }
    
    @classmethod
    def get_extractor(cls, method: CookieMethod) -> CookieExtractor:
        extractor_class = cls._extractors.get(method)
        if extractor_class is None:
            raise ValueError(f"不支持的Cookie获取方法: {method}")
        return extractor_class()
    
    @classmethod
    def get_available_methods(cls) -> List[CookieMethodDetail]:
        return [
            CookieMethodDetail(
                method=CookieMethod.BROWSER_COOKIE3,
                name="浏览器自动提取",
                description="使用browser_cookie3库自动从本地浏览器提取Cookie",
                difficulty="简单",
                time_required="10秒",
                pros=["全自动提取", "支持多浏览器", "无需手动操作"],
                cons=["需要关闭浏览器", "可能需要管理员权限", "部分系统可能不兼容"],
                requirements=["pip install browser_cookie3", "浏览器需要关闭"],
                steps=[
                    "安装browser_cookie3库: pip install browser_cookie3",
                    "关闭所有浏览器窗口",
                    "选择要提取的浏览器类型",
                    "点击'提取Cookie'按钮",
                    "等待提取完成"
                ],
                platforms=["Windows", "macOS", "Linux"]
            ),
            CookieMethodDetail(
                method=CookieMethod.MANUAL_INPUT,
                name="手动输入",
                description="手动复制粘贴Cookie字符串",
                difficulty="中等",
                time_required="1-2分钟",
                pros=["最可靠", "无需额外依赖", "跨平台通用"],
                cons=["需要手动操作", "容易出错", "Cookie格式需要正确"],
                requirements=["浏览器开发者工具"],
                steps=[
                    "登录目标网站",
                    "按F12打开开发者工具",
                    "切换到Application/存储标签",
                    "展开Cookies，找到目标域名",
                    "复制Cookie值（格式：name=value; name2=value2）",
                    "粘贴到输入框中"
                ],
                platforms=["所有平台"]
            ),
            CookieMethodDetail(
                method=CookieMethod.FILE_IMPORT,
                name="文件导入",
                description="从JSON/Netscape格式文件导入Cookie",
                difficulty="简单",
                time_required="30秒",
                pros=["批量导入", "可保存复用", "支持多种格式"],
                cons=["需要提前准备文件", "格式需要正确"],
                requirements=["Cookie文件（JSON/Netscape格式）"],
                steps=[
                    "准备Cookie文件（支持JSON、Netscape、Header格式）",
                    "点击'选择文件'按钮",
                    "选择Cookie文件",
                    "选择文件格式",
                    "点击'导入'按钮"
                ],
                platforms=["所有平台"]
            ),
            CookieMethodDetail(
                method=CookieMethod.SELENIUM,
                name="Selenium自动化",
                description="使用Selenium控制浏览器自动获取Cookie",
                difficulty="较难",
                time_required="配置5分钟 + 运行30秒",
                pros=["可模拟登录", "支持复杂交互", "可处理验证码"],
                cons=["需要配置WebDriver", "资源占用大", "可能被检测"],
                requirements=[
                    "pip install selenium webdriver-manager",
                    "对应浏览器WebDriver"
                ],
                steps=[
                    "安装Selenium: pip install selenium",
                    "安装WebDriver管理器: pip install webdriver-manager",
                    "配置浏览器选项",
                    "运行自动化脚本",
                    "等待页面加载完成",
                    "自动获取Cookie"
                ],
                platforms=["Windows", "macOS", "Linux"]
            ),
            CookieMethodDetail(
                method=CookieMethod.PLAYWRIGHT,
                name="Playwright自动化",
                description="使用Playwright新一代自动化工具获取Cookie",
                difficulty="中等",
                time_required="配置3分钟 + 运行20秒",
                pros=["现代化工具", "多浏览器支持", "自动等待", "更难被检测"],
                cons=["需要安装浏览器", "首次配置较慢"],
                requirements=[
                    "pip install playwright",
                    "playwright install（安装浏览器）"
                ],
                steps=[
                    "安装Playwright: pip install playwright",
                    "安装浏览器: playwright install",
                    "配置浏览器类型（Chromium/Firefox/WebKit）",
                    "运行自动化脚本",
                    "等待页面加载完成",
                    "自动获取Cookie"
                ],
                platforms=["Windows", "macOS", "Linux"]
            ),
            CookieMethodDetail(
                method=CookieMethod.EDITTHISCOOKIE,
                name="EditThisCookie导出",
                description="解析浏览器插件EditThisCookie导出的Cookie",
                difficulty="简单",
                time_required="30秒",
                pros=["格式标准", "一键导出", "支持批量"],
                cons=["需要安装浏览器插件", "仅支持Chrome系浏览器"],
                requirements=["Chrome/Edge浏览器", "EditThisCookie插件"],
                steps=[
                    "安装EditThisCookie浏览器插件",
                    "登录目标网站",
                    "点击插件图标",
                    "点击'导出'按钮",
                    "复制导出的JSON数据",
                    "粘贴到输入框中"
                ],
                platforms=["Windows", "macOS", "Linux"]
            ),
            CookieMethodDetail(
                method=CookieMethod.CLIPBOARD,
                name="剪贴板自动识别",
                description="自动从剪贴板识别并解析Cookie",
                difficulty="简单",
                time_required="10秒",
                pros=["快速便捷", "自动识别格式", "无需手动输入"],
                cons=["需要提前复制", "依赖剪贴板库"],
                requirements=["pip install pyperclip"],
                steps=[
                    "安装pyperclip: pip install pyperclip",
                    "复制Cookie内容到剪贴板",
                    "点击'从剪贴板获取'按钮",
                    "系统自动识别格式并解析"
                ],
                platforms=["Windows", "macOS", "Linux"]
            ),
        ]
    
    @classmethod
    def get_method_comparison(cls) -> Dict[str, Any]:
        methods = cls.get_available_methods()
        
        comparison = {
            "by_difficulty": {
                "简单": [],
                "中等": [],
                "较难": []
            },
            "by_time": {},
            "recommendations": []
        }
        
        for method in methods:
            comparison["by_difficulty"][method.difficulty].append({
                "name": method.name,
                "method": method.method.value,
                "time": method.time_required
            })
            
            comparison["by_time"][method.method.value] = method.time_required
        
        comparison["recommendations"] = [
            {
                "scenario": "新手用户",
                "recommended": CookieMethod.MANUAL_INPUT.value,
                "reason": "最可靠，无需额外配置"
            },
            {
                "scenario": "批量操作",
                "recommended": CookieMethod.BROWSER_COOKIE3.value,
                "reason": "全自动提取，效率最高"
            },
            {
                "scenario": "需要登录验证",
                "recommended": CookieMethod.PLAYWRIGHT.value,
                "reason": "可模拟复杂登录流程"
            },
            {
                "scenario": "快速导入",
                "recommended": CookieMethod.FILE_IMPORT.value,
                "reason": "支持批量导入，可保存复用"
            }
        ]
        
        return comparison


def get_cookie_methods() -> List[Dict[str, Any]]:
    """获取所有Cookie获取方法"""
    methods = CookieExtractorFactory.get_available_methods()
    return [
        {
            "method": m.method.value,
            "name": m.name,
            "description": m.description,
            "difficulty": m.difficulty,
            "time_required": m.time_required,
            "pros": m.pros,
            "cons": m.cons,
            "requirements": m.requirements,
            "steps": m.steps,
            "platforms": m.platforms
        }
        for m in methods
    ]


def extract_cookie(method: CookieMethod, **kwargs) -> CookieExtractionResult:
    """提取Cookie的统一接口"""
    extractor = CookieExtractorFactory.get_extractor(method)
    return extractor.extract(**kwargs)
