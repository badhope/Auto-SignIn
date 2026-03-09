"""
支付宝签到平台
"""
import httpx
import json
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.logger import logger


class AlipayPlatform(BasePlatform):
    """支付宝签到"""
    
    PLATFORM_NAME = "支付宝"
    PLATFORM_CODE = "alipay"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://www.alipay.com/',
                'Origin': 'https://www.alipay.com',
            })
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 执行签到
                sign_response = await client.get(
                    'https://activity.alipay.com/portal-sign/signin/list',
                    headers=headers
                )
                
                sign_response.raise_for_status()
                
                # 支付宝响应可能是 HTML 或 JSON
                try:
                    data = sign_response.json()
                    if data.get('success') or data.get('code') == 'SUCCESS':
                        return SignResult(
                            success=True,
                            message="签到成功",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown',
                            data=data
                        )
                    else:
                        return SignResult(
                            success=False,
                            message=data.get('msg', '签到失败'),
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown',
                            data=data
                        )
                except json.JSONDecodeError:
                    # HTML 响应，检查状态码
                    if sign_response.status_code == 200:
                        return SignResult(
                            success=True,
                            message="签到成功",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown'
                        )
                    else:
                        return SignResult(
                            success=False,
                            message=f"签到失败 (HTTP {sign_response.status_code})",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown'
                        )
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP 错误：{e.response.status_code}")
            return SignResult(
                success=False,
                message=f"HTTP 错误 {e.response.status_code}",
                platform=self.name,
                username=tokens.get('username', 'unknown') if tokens else 'unknown'
            )
        except httpx.RequestError as e:
            logger.error(f"网络错误：{str(e)}")
            return SignResult(
                success=False,
                message=f"网络错误 - {str(e)}",
                platform=self.name,
                username=tokens.get('username', 'unknown') if tokens else 'unknown'
            )
        except Exception as e:
            logger.error(f"签到异常：{str(e)}", exc_info=True)
            return SignResult(
                success=False,
                message=f"签到异常：{str(e)}",
                platform=self.name,
                username=tokens.get('username', 'unknown') if tokens else 'unknown'
            )
