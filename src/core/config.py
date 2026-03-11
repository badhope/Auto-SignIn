"""
配置管理系统
支持：环境变量 + YAML 配置文件 + .env 文件
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """配置管理单例"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # 加载 .env 文件
        load_dotenv()
        
        # 配置路径
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_file = self.base_dir / 'config' / 'config.yaml'
        self.accounts_file = self.base_dir / 'config' / 'accounts.yaml'
        self.db_file = self.base_dir / 'data' / 'signin.db'
        
        # 默认配置
        self.settings = {
            'app': {
                'name': 'Auto-SignIn v2',
                'version': '2.0.0',
                'debug': False,
            },
            'schedule': {
                'enabled': False,
                'time': '08:00',  # HH:MM 格式
                'timezone': 'Asia/Shanghai',
            },
            'retry': {
                'max_attempts': 3,
                'delay': 5,  # 秒
            },
            'notification': {
                'enabled': False,
                'email': {
                    'enabled': False,
                    'smtp_server': '',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'to_email': '',
                },
                'telegram': {
                    'enabled': False,
                    'bot_token': '',
                    'chat_id': '',
                },
                'webhook': {
                    'enabled': False,
                    'url': '',
                    'method': 'POST',
                },
            },
            'database': {
                'enabled': True,
                'type': 'sqlite',
                'path': str(self.db_file),
            }
        }
        
        # 加载配置文件
        self._load_config()
        
        # 环境变量覆盖
        self._load_env()
        
        self._initialized = True
    
    def _load_config(self):
        """从 YAML 文件加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f) or {}
                    self._merge_config(file_config)
            except Exception:
                pass
    
    def _load_env(self):
        """从环境变量加载配置"""
        # 调试模式
        if os.getenv('AUTOSIGNIN_DEBUG'):
            self.settings['app']['debug'] = os.getenv('AUTOSIGNIN_DEBUG') == 'true'
        
        # 定时任务
        if os.getenv('AUTOSIGNIN_SCHEDULE'):
            self.settings['schedule']['enabled'] = os.getenv('AUTOSIGNIN_SCHEDULE') == 'true'
        if os.getenv('AUTOSIGNIN_SCHEDULE_TIME'):
            self.settings['schedule']['time'] = os.getenv('AUTOSIGNIN_SCHEDULE_TIME')
        
        # 通知
        if os.getenv('AUTOSIGNIN_NOTIFICATION'):
            self.settings['notification']['enabled'] = os.getenv('AUTOSIGNIN_NOTIFICATION') == 'true'
    
    def _merge_config(self, file_config: Dict[str, Any]):
        """合并配置文件"""
        for key, value in file_config.items():
            if key in self.settings and isinstance(value, dict):
                self.settings[key].update(value)
            else:
                self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.settings
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.settings, f, allow_unicode=True, default_flow_style=False)


# 全局配置实例
config = Config()
