"""
签到引擎核心
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.utils.logger import logger
from src.core.database import Database
from src.core.notifier import Notifier
from src.core.config import config


class SigninEngine:
    """签到引擎"""
    
    def __init__(self):
        self.config = config
        self.db = Database(self.config.get('database.path'))
        self.notifier = Notifier(self.config.get('notification'))
        self.platforms = {}
        self._register_platforms()
    
    def _register_platforms(self):
        """注册所有平台"""
        from src.platforms.netease import NeteasePlatform
        from src.platforms.bilibili import BilibiliPlatform
        from src.platforms.csdn import CSDNPlatform
        from src.platforms.taobao import TaobaoPlatform
        from src.platforms.jd import JDPlatform
        from src.platforms.meituan import MeituanPlatform
        from src.platforms.alipay import AlipayPlatform
        
        self.platforms = {
            'netease': NeteasePlatform(),
            'bilibili': BilibiliPlatform(),
            'csdn': CSDNPlatform(),
            'taobao': TaobaoPlatform(),
            'jd': JDPlatform(),
            'meituan': MeituanPlatform(),
            'alipay': AlipayPlatform(),
        }
        logger.info(f"已注册 {len(self.platforms)} 个平台：{', '.join(self.platforms.keys())}")
    
    async def signin(self, platform_code: str, account: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个账号签到
        
        Args:
            platform_code: 平台代码
            account: 账号信息
        
        Returns:
            签到结果
        """
        platform = self.platforms.get(platform_code)
        if not platform:
            logger.error(f"平台 {platform_code} 未注册")
            return {
                'success': False,
                'message': f'平台 {platform_code} 不存在',
                'platform': platform_code,
                'username': account.get('username', 'unknown')
            }
        
        logger.info(f"开始签到：{platform.PLATFORM_NAME} - {account.get('username')}")
        
        # 验证 Cookie
        if not platform.validate_cookies(account.get('cookies', '')):
            logger.warning(f"Cookie 格式无效：{platform.PLATFORM_NAME}")
            return {
                'success': False,
                'message': 'Cookie 格式无效',
                'platform': platform_code,
                'username': account.get('username', 'unknown')
            }
        
        # 执行签到（带重试）
        result = await platform.sign_in_with_retry(
            cookies=account.get('cookies'),
            tokens=account.get('tokens')
        )
        
        # 记录到数据库
        self.db.add_signin_record(
            platform=platform_code,
            username=result.username,
            success=result.success,
            message=result.message,
            points=result.points
        )
        
        # 发送通知
        if self.notifier.enabled:
            title = f"{platform.PLATFORM_NAME} 签到{'成功' if result.success else '失败'}"
            await self.notifier.send(
                title=title,
                message=result.message,
                data=result.to_dict()
            )
        
        logger.info(f"签到完成：{platform.PLATFORM_NAME} - {result.message}")
        return result.to_dict()
    
    async def signin_all(self, platform_code: str = None):
        """
        执行所有账号签到
        
        Args:
            platform_code: 指定平台（可选）
        """
        logger.info("开始执行批量签到")
        
        # 获取所有账号
        accounts = self.db.get_accounts(platform=platform_code)
        
        if not accounts:
            logger.warning("没有找到任何账号")
            return
        
        # 按平台分组
        platform_accounts = {}
        for account in accounts:
            platform = account['platform']
            if platform not in platform_accounts:
                platform_accounts[platform] = []
            platform_accounts[platform].append(account)
        
        # 并发执行签到
        tasks = []
        for platform, accs in platform_accounts.items():
            for acc in accs:
                task = self.signin(platform, acc)
                tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计结果
        total = len(results)
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
        failure_count = total - success_count
        total_duration = sum(r.get('duration', 0) for r in results if isinstance(r, dict))
        
        logger.info(f"批量签到完成：成功 {success_count}/{total}，失败 {failure_count}，耗时 {total_duration:.2f}秒")
        
        # 发送汇总通知
        if self.notifier.enabled and total > 0:
            await self.notifier.send(
                title="签到汇总",
                message=f"今日签到完成：成功 {success_count}/{total} 个账号，总耗时 {total_duration:.2f}秒",
                data={
                    'success': success_count,
                    'failure': failure_count,
                    'total': total,
                    'duration': total_duration,
                    'success_rate': f"{(success_count/total*100):.1f}%" if total > 0 else "0%"
                }
            )
    
    def add_account(self, platform: str, username: str, cookies: str, tokens: Dict = None):
        """添加账号"""
        self.db.add_account(platform, username, cookies, tokens)
        logger.info(f"账号已添加：{platform} - {username}")
    
    def remove_account(self, platform: str, username: str):
        """删除账号"""
        self.db.delete_account(platform, username)
        logger.info(f"账号已删除：{platform} - {username}")
    
    def list_accounts(self, platform: str = None) -> List[Dict]:
        """列出所有账号"""
        return self.db.get_accounts(platform=platform)
    
    def get_history(self, platform: str = None, limit: int = 10) -> List[Dict]:
        """获取签到历史"""
        return self.db.get_history(platform=platform, limit=limit)
    
    def get_stats(self, days: int = 7) -> Dict:
        """获取统计数据"""
        return self.db.get_stats(days=days)
    
    def get_platforms(self) -> List[Dict]:
        """获取所有已注册平台信息"""
        return [p.get_platform_info() for p in self.platforms.values()]
    
    def get_performance_stats(self, days: int = 7) -> Dict:
        """获取性能统计"""
        history = self.db.get_history(limit=1000)
        if not history:
            return {'avg_duration': 0, 'total_signins': 0}
        
        # 计算平均耗时
        durations = [h.get('duration', 0) for h in history if h.get('duration')]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 按平台统计
        platform_stats = {}
        for record in history:
            platform = record['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {'total': 0, 'success': 0, 'duration': 0}
            platform_stats[platform]['total'] += 1
            if record['success']:
                platform_stats[platform]['success'] += 1
            platform_stats[platform]['duration'] += record.get('duration', 0)
        
        return {
            'avg_duration': round(avg_duration, 2),
            'total_signins': len(history),
            'platform_stats': {
                k: {
                    'total': v['total'],
                    'success_rate': f"{(v['success']/v['total']*100):.1f}%" if v['total'] > 0 else "0%",
                    'avg_duration': round(v['duration']/v['total'], 2) if v['total'] > 0 else 0
                }
                for k, v in platform_stats.items()
            }
        }
