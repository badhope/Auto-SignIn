"""
平台签到基础接口 v2
增强版：添加重试机制、性能监控、详细日志
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import random


@dataclass
class SignResult:
    """签到结果"""
    success: bool
    message: str
    platform: str
    username: str
    points: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    duration: float = 0.0  # 执行耗时（秒）
    retry_count: int = 0  # 重试次数
    
    def to_dict(self) -> Dict[str, Any]:
        """转为字典"""
        return {
            'success': self.success,
            'message': self.message,
            'platform': self.platform,
            'username': self.username,
            'points': self.points,
            'data': self.data,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'duration': self.duration,
            'retry_count': self.retry_count
        }


class BasePlatform(ABC):
    """平台基类 v2"""
    
    PLATFORM_NAME: str = ""
    PLATFORM_CODE: str = ""
    
    def __init__(self):
        self.name = self.PLATFORM_NAME
        self.code = self.PLATFORM_CODE or self.__class__.__name__.lower()
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 2  # 重试间隔（秒）
        self.timeout = 30  # 请求超时（秒）
    
    @abstractmethod
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """
        异步签到方法
        
        Args:
            cookies: Cookie 字符串
            tokens: 其他认证信息
        
        Returns:
            SignResult: 签到结果
        """
        pass
    
    async def sign_in_with_retry(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """
        带重试的签到方法
        
        Args:
            cookies: Cookie 字符串
            tokens: 其他认证信息
        
        Returns:
            SignResult: 签到结果
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # 添加随机延迟防止请求过快
                if attempt > 0:
                    delay = self.retry_delay * attempt + random.uniform(0.5, 1.5)
                    await asyncio.sleep(delay)
                
                # 执行签到
                start_time = datetime.now()
                result = await self.sign_in_async(cookies, tokens)
                end_time = datetime.now()
                
                # 记录执行时间
                result.duration = (end_time - start_time).total_seconds()
                result.retry_count = attempt
                
                return result
                
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    continue
                else:
                    # 所有重试都失败
                    return SignResult(
                        success=False,
                        message=f"签到失败：{str(e)} (重试{attempt}次)",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        retry_count=attempt
                    )
        
        # 不应该到达这里
        return SignResult(
            success=False,
            message=f"签到异常：{str(last_error)}",
            platform=self.name,
            username=tokens.get('username', 'unknown') if tokens else 'unknown'
        )
    
    def get_cookies_required(self) -> bool:
        """是否需要 Cookie"""
        return True
    
    def get_headers(self) -> Dict[str, str]:
        """获取默认请求头"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    
    def validate_cookies(self, cookies: str) -> bool:
        """验证 Cookie 格式"""
        return bool(cookies) and len(cookies) > 10
    
    def get_platform_info(self) -> Dict[str, Any]:
        """获取平台信息"""
        return {
            'name': self.name,
            'code': self.code,
            'cookies_required': self.get_cookies_required(),
            'max_retries': self.max_retries,
            'timeout': self.timeout
        }
