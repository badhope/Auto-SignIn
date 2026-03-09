"""
网易云音乐签到平台
"""
import httpx
import json
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.netease_crypto import NeteaseCrypto
from src.utils.logger import logger


class NeteasePlatform(BasePlatform):
    """网易云音乐签到"""
    
    PLATFORM_NAME = "网易云音乐"
    PLATFORM_CODE = "netease"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://music.163.com/',
                'Origin': 'https://music.163.com',
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            # 加密参数
            params = {"type": 0}  # 0=移动端签到，1=PC 端签到
            encrypted_data = NeteaseCrypto.encrypt_params(params)
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    'https://music.163.com/weapi/point/dailyTask',
                    headers=headers,
                    data=encrypted_data
                )
                
                response.raise_for_status()
                
                # 解析响应
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    logger.error(f"JSON 解析失败：{response.text[:100]}")
                    return SignResult(
                        success=False,
                        message=f"API 返回格式错误",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        data={'raw_response': response.text}
                    )
                
                # 判断结果
                if data.get('code') == 200:
                    return SignResult(
                        success=True,
                        message="签到成功",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        points=data.get('point', 0),
                        data=data
                    )
                else:
                    error_msg = data.get('msg', f'签到失败 (code={data.get("code")})')
                    logger.warning(f"签到失败：{error_msg}")
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
        except Exception as e:
            logger.error(f"签到异常：{str(e)}", exc_info=True)
            return SignResult(
                success=False,
                message=f"签到异常：{str(e)}",
                platform=self.name,
                username=tokens.get('username', 'unknown') if tokens else 'unknown'
            )
