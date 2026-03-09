"""
美团签到平台
"""
import httpx
import json
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.logger import logger


class MeituanPlatform(BasePlatform):
    """美团签到"""
    
    PLATFORM_NAME = "美团"
    PLATFORM_CODE = "meituan"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://www.meituan.com/',
                'Origin': 'https://www.meituan.com',
                'Content-Type': 'application/json',
            })
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 执行签到
                sign_response = await client.post(
                    'https://i.meituan.com/pointtask/getPoint',
                    headers=headers,
                    json={}
                )
                
                sign_response.raise_for_status()
                data = sign_response.json()
                
                if data.get('code') == 0 or data.get('success'):
                    # 获取积分
                    point = data.get('data', {}).get('point', 0)
                    
                    return SignResult(
                        success=True,
                        message=f"签到成功，获得 {point} 积分",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        points=point,
                        data=data
                    )
                else:
                    error_msg = data.get('msg', '签到失败')
                    # 检查是否已签到
                    if '已签到' in error_msg or '已经签到' in error_msg:
                        return SignResult(
                            success=True,
                            message="今日已签到",
                            platform=self.name,
                            username=tokens.get('username', 'unknown') if tokens else 'unknown',
                            data=data
                        )
                    
                    return SignResult(
                        success=False,
                        message=error_msg,
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        data=data
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
        except json.JSONDecodeError:
            logger.error("JSON 解析失败")
            return SignResult(
                success=False,
                message="响应格式错误",
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
