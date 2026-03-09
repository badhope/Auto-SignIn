"""
哔哩哔哩签到平台
"""
import httpx
import json
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.logger import logger


class BilibiliPlatform(BasePlatform):
    """哔哩哔哩签到"""
    
    PLATFORM_NAME = "哔哩哔哩"
    PLATFORM_CODE = "bilibili"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://www.bilibili.com/',
            })
            
            async with httpx.AsyncClient(timeout=30) as client:
                # 先获取 CSRF token
                token_response = await client.get('https://www.bilibili.com/')
                csrf_token = None
                if 'bili_jct' in cookies:
                    csrf_token = cookies.split('bili_jct=')[1].split(';')[0]
                
                if not csrf_token:
                    return SignResult(
                        success=False,
                        message="未找到 CSRF token",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown'
                    )
                
                # 执行签到
                sign_response = await client.post(
                    'https://api.bilibili.com/x/web-interface/nav/signin',
                    headers=headers,
                    data={'csrf': csrf_token}
                )
                
                data = sign_response.json()
                
                if data.get('code') == 0:
                    # 获取关注列表
                    follow_response = await client.get(
                        'https://api.bilibili.com/x/relation/followings',
                        headers=headers
                    )
                    follow_data = follow_response.json()
                    
                    return SignResult(
                        success=True,
                        message="签到成功",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        data={
                            'signin': data,
                            'followings': follow_data
                        }
                    )
                else:
                    return SignResult(
                        success=False,
                        message=data.get('message', '签到失败'),
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        data=data
                    )
        
        except Exception as e:
            logger.error(f"签到异常：{str(e)}", exc_info=True)
            return SignResult(
                success=False,
                message=f"签到异常：{str(e)}",
                platform=self.name,
                username=tokens.get('username', 'unknown') if tokens else 'unknown'
            )
