"""
V2EX 平台插件
"""

from typing import Dict, Any

import httpx

from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult


@register_platform(
    name="v2ex",
    display_name="V2EX",
    version="1.0.0",
    capabilities=["daily_sign", "check_in", "daily_bonus"],
    required_fields=["cookie"]
)
class V2EXPlatform(BasePlatform):
    """V2EX 签到平台"""

    name = "v2ex"
    display_name = "V2EX"
    version = "1.0.0"
    base_url = "https://www.v2ex.com"

    async def sign_in(self, account_name: str, cookies: Dict[str, str]) -> SignInResult:
        """执行 V2EX 签到"""
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
            "Referer": "https://www.v2ex.com/",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/mission/daily",
                    headers=headers
                )

                result.status_code = response.status_code

                if response.status_code == 200:
                    html_content = response.text

                    if "每日登录奖励已领取" in html_content or "每日签到已领取" in html_content:
                        result.success = True
                        result.message = "今日已签到"
                    elif "领取" in html_content or "sign" in html_content.lower():
                        result.success = True
                        result.message = "签到成功"
                    else:
                        result.success = True
                        result.message = "签到完成"
                elif response.status_code == 401:
                    result.success = False
                    result.error = "Cookie已过期，请重新获取"
                    result.error_type = "AuthError"
                elif response.status_code == 403:
                    result.success = False
                    result.error = "访问被拒绝"
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
            "Referer": "https://www.v2ex.com/"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://www.v2ex.com/settings",
                    headers=headers
                )

                return response.status_code == 200 and "用户名" in response.text

        except Exception:
            return False
