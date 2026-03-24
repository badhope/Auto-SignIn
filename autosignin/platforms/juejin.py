"""
掘金平台插件
"""

from typing import Dict, Any

import httpx

from autosignin.platforms.base import BasePlatform, register_platform
from autosignin.models.signin import SignInResult


@register_platform(
    name="juejin",
    display_name="掘金",
    version="1.0.0",
    capabilities=["daily_sign", "check_in", "get_ore"],
    required_fields=["cookie"]
)
class JuejinPlatform(BasePlatform):
    """掘金签到平台"""

    name = "juejin"
    display_name = "掘金"
    version = "1.0.0"
    base_url = "https://api.juejin.cn"

    async def sign_in(self, account_name: str, cookies: Dict[str, str]) -> SignInResult:
        """执行掘金签到"""
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
            "Referer": "https://juejin.cn/",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/growth_api/v1/check_in",
                    headers=headers,
                    json={}
                )

                result.status_code = response.status_code

                if response.status_code == 200:
                    data = response.json()
                    if data.get("err_no") == 0:
                        result.success = True
                        result.message = f"签到成功"
                        result.data = data.get("data", {})
                        if result.data:
                            result.message += f", 获得 {result.data.get('dice_point', 0)} 矿石"
                    else:
                        result.success = False
                        result.error = data.get("err_msg", "签到失败")
                        result.error_type = "SignInError"
                elif response.status_code == 401:
                    result.success = False
                    result.error = "Cookie已过期，请重新获取"
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
            "Referer": "https://juejin.cn/"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://api.juejin.cn/user_api/v1/user/get_info",
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("err_no") == 0
                return False

        except Exception:
            return False
