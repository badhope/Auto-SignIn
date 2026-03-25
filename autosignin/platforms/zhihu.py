"""
知乎平台插件
"""

from typing import Dict, Any

import httpx

from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult


@register_platform(
    name="zhihu",
    display_name="知乎",
    version="1.0.0",
    capabilities=["daily_sign", "check_in"],
    required_fields=["cookie"]
)
class ZhihuPlatform(BasePlatform):
    """知乎签到平台"""

    name = "zhihu"
    display_name = "知乎"
    version = "1.0.0"
    base_url = "https://www.zhihu.com"

    async def sign_in(self, account_name: str, cookies: Dict[str, str]) -> SignInResult:
        """执行知乎签到"""
        result = SignInResult(
            platform=self.name,
            account=account_name
        )

        cookie_str = cookies.get("cookie", "")

        if not cookie_str:
            result.success = False
            result.error = "Missing required cookie"
            result.error_type = "AuthError"
            return result

        headers = {
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.zhihu.com/",
            "X-API-VERSION": "3.0.91"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v3/point/increase",
                    headers=headers
                )

                result.status_code = response.status_code

                if response.status_code == 200:
                    data = response.json()
                    if data.get("msg") == "success":
                        result.success = True
                        result.message = f"签到成功，获得 {data.get('score_change', 0)} 积分"
                        result.data = data
                    else:
                        result.success = True
                        result.message = data.get("msg", "签到完成")
                        result.data = data
                elif response.status_code == 401:
                    result.success = False
                    result.error = "Cookie已过期，请重新获取"
                    result.error_type = "AuthError"
                elif response.status_code == 403:
                    result.success = False
                    result.error = "访问被拒绝，可能需要验证"
                    result.error_type = "AuthError"
                else:
                    result.success = False
                    result.error = f"签到失败: HTTP {response.status_code}"
                    result.error_type = "SignInError"

        except httpx.TimeoutException:
            result.success = False
            result.error = "请求超时"
            result.error_type = "TimeoutError"
        except httpx.HTTPError as e:
            result.success = False
            result.error = f"HTTP错误: {str(e)}"
            result.error_type = "NetworkError"
        except Exception as e:
            result.success = False
            result.error = f"签到异常: {str(e)}"
            result.error_type = "UnknownError"

        return result

    async def verify(self, cookies: Dict[str, str]) -> bool:
        """验证登录状态"""
        cookie_str = cookies.get("cookie", "")

        if not cookie_str:
            return False

        headers = {
            "Cookie": cookie_str,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.zhihu.com/"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://www.zhihu.com/api/v4/me",
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("is_login", False)
                return False

        except Exception as e:
            self.logger.warning(f"Verify failed: {e}")
            return False
