import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import Config


class TestConfig:
    def test_config_singleton(self):
        config1 = Config()
        config2 = Config()
        assert config1 is config2

    def test_config_get_default(self):
        config = Config()
        assert config.get('app.name') == 'Auto-SignIn v2'
        assert config.get('app.version') == '2.0.0'
        assert config.get('schedule.enabled') is False

    def test_config_set_and_get(self):
        config = Config()
        config.set('test.key', 'test_value')
        assert config.get('test.key') == 'test_value'

    def test_config_nested_get(self):
        config = Config()
        assert config.get('notification.email.enabled') is False
        assert config.get('database.type') == 'sqlite'

    def test_config_default_value(self):
        config = Config()
        assert config.get('nonexistent.key', 'default') == 'default'
