"""
CSDN 签到平台
"""
import httpx
import json
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.logger import logger


class CSDNPlatform(BasePlatform):
    """CSDN 签到"""
    
    PLATFORM_NAME = "CSDN"
    PLATFORM_CODE = "csdn"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://blog.csdn.net/',
                'Origin': 'https://blog.csdn.net',
            })
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 获取 CSRF token
                token_response = await client.get('https://blog.csdn.net/')
                if token_response.status_code != 200:
                    return SignResult(
                        success=False,
                        message="获取 CSRF token 失败",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown'
                    )
                
                # 执行签到
                sign_response = await client.post(
                    'https://blog.csdn.net/vip_interactive',
                    headers=headers,
                    data={'cmd': 'sign_in'}
                )
                
                sign_response.raise_for_status()
                
                # CSDN 签到响应可能是 HTML 或 JSON
                try:
                    data = sign_response.json()
                    if data.get('code') == 200:
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
                    # HTML 响应，检查是否包含成功关键词
                    if '签到成功' in sign_response.text or '已签到' in sign_response.text:
                        return SignResult(
                            success=True,
                            message="签到成功",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown'
                        )
                    else:
                        return SignResult(
                            success=False,
                            message="签到失败（可能已签到）",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown',
                            data={'raw_response': sign_response.text[:200]}
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
