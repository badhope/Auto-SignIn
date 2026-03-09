"""
京东签到平台
"""
import httpx
import json
import hashlib
from typing import Optional, Dict
from .base import BasePlatform, SignResult
from src.utils.logger import logger


class JDPlatform(BasePlatform):
    """京东签到"""
    
    PLATFORM_NAME = "京东"
    PLATFORM_CODE = "jd"
    
    def get_cookies_required(self) -> bool:
        return True
    
    async def sign_in_async(self, cookies: str, tokens: Optional[Dict[str, str]] = None) -> SignResult:
        """执行签到"""
        try:
            headers = self.get_headers()
            headers.update({
                'Cookie': cookies,
                'Referer': 'https://www.jd.com/',
                'Origin': 'https://www.jd.com',
                'Content-Type': 'application/x-www-form-urlencoded',
            })
            
            # 生成设备指纹
            fp = hashlib.md5(cookies.encode()).hexdigest()
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # 执行签到
                sign_response = await client.post(
                    'https://api.m.jd.com/client.action',
                    headers=headers,
                    data={
                        'functionId': 'signBeanIndex',
                        'body': json.dumps({
                            'fp': fp,
                            'eid': '',
                            'shshshfpa': '',
                            'referUrl': '-1',
                            'fpAppId': '1'
                        }),
                        'client': 'AppleWebKit',
                        'clientVersion': '537.36'
                    }
                )
                
                sign_response.raise_for_status()
                data = sign_response.json()
                
                if data.get('code') == 0:
                    # 获取京豆数量
                    bean_num = data.get('data', {}).get('beanNum', 0)
                    
                    return SignResult(
                        success=True,
                        message=f"签到成功，获得 {bean_num} 京豆",
                        platform=self.name,
                        username=tokens.get('username', 'unknown') if tokens else 'unknown',
                        points=bean_num,
                        data=data
                    )
                else:
                    error_msg = data.get('errorMessage', '签到失败')
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
