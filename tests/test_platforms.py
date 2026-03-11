import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.platforms.base import BasePlatform, SignResult


class DummyPlatform(BasePlatform):
    PLATFORM_NAME = "测试平台"
    PLATFORM_CODE = "test"
    
    async def sign_in_async(self, cookies: str, tokens: dict = None) -> SignResult:
        return SignResult(
            success=True,
            message="测试成功",
            platform=self.name,
            username="test_user"
        )


class TestBasePlatform:
    def test_platform_info(self):
        platform = DummyPlatform()
        info = platform.get_platform_info()
        
        assert info['name'] == "测试平台"
        assert info['code'] == "test"
        assert info['cookies_required'] is True
        assert info['max_retries'] == 3
        assert info['timeout'] == 30

    def test_validate_cookies_valid(self):
        platform = DummyPlatform()
        assert platform.validate_cookies("cookie1=value1; cookie2=value2") is True

    def test_validate_cookies_invalid(self):
        platform = DummyPlatform()
        assert platform.validate_cookies("") is False
        assert platform.validate_cookies("short") is False

    def test_get_headers(self):
        platform = DummyPlatform()
        headers = platform.get_headers()
        
        assert 'User-Agent' in headers
        assert 'Accept' in headers
        assert 'Accept-Language' in headers


class TestSignResult:
    def test_sign_result_to_dict(self):
        result = SignResult(
            success=True,
            message="测试消息",
            platform="test_platform",
            username="test_user",
            points=100
        )
        
        data = result.to_dict()
        
        assert data['success'] is True
        assert data['message'] == "测试消息"
        assert data['platform'] == "test_platform"
        assert data['username'] == "test_user"
        assert data['points'] == 100
        assert 'timestamp' in data
        assert 'duration' in data
        assert 'retry_count' in data
