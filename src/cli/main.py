"""
命令行界面
"""
import asyncio
import argparse
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.engine import SigninEngine
from src.core.config import config
from src.utils.logger import logger, setup_logger


def setup_cli():
    """设置命令行参数"""
    parser = argparse.ArgumentParser(
        description='Auto-SignIn v2 - 自动化签到工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  # 添加账号
  python -m src.cli.main add netease --username "user123" --cookie "MUSIC_U=xxx"
  
  # 执行签到
  python -m src.cli.main signin
  python -m src.cli.main signin --platform netease
  
  # 查看历史
  python -m src.cli.main history
  
  # 查看统计
  python -m src.cli.main stats
  
  # 删除账号
  python -m src.cli.main remove netease --username "user123"
  
  # 启用定时任务
  python -m src.cli.main schedule --enable
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加账号')
    add_parser.add_argument('platform', choices=['netease', 'bilibili', 'csdn', 'taobao', 'jd', 'meituan', 'alipay'], help='平台')
    add_parser.add_argument('--username', '-u', required=True, help='用户名/昵称')
    add_parser.add_argument('--cookie', '-c', required=True, help='Cookie 字符串')
    
    # signin 命令
    signin_parser = subparsers.add_parser('signin', help='执行签到')
    signin_parser.add_argument('--platform', '-p', help='指定平台（可选）')
    signin_parser.add_argument('--all', '-a', action='store_true', help='签到所有账号')
    
    # history 命令
    history_parser = subparsers.add_parser('history', help='查看签到历史')
    history_parser.add_argument('--platform', '-p', help='指定平台')
    history_parser.add_argument('--limit', '-l', type=int, default=10, help='显示数量')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='查看统计数据')
    stats_parser.add_argument('--days', '-d', type=int, default=7, help='统计天数')
    
    # perf 命令（性能统计）
    perf_parser = subparsers.add_parser('perf', help='查看性能统计')
    perf_parser.add_argument('--days', '-d', type=int, default=7, help='统计天数')
    
    # platforms 命令（列出平台）
    platforms_parser = subparsers.add_parser('platforms', help='列出所有支持的平台')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有账号')
    list_parser.add_argument('--platform', '-p', help='指定平台')
    
    # remove 命令
    remove_parser = subparsers.add_parser('remove', help='删除账号')
    remove_parser.add_argument('platform', help='平台')
    remove_parser.add_argument('--username', '-u', required=True, help='用户名')
    
    # schedule 命令
    schedule_parser = subparsers.add_parser('schedule', help='定时任务管理')
    schedule_parser.add_argument('--enable', action='store_true', help='启用定时任务')
    schedule_parser.add_argument('--disable', action='store_true', help='禁用定时任务')
    schedule_parser.add_argument('--time', '-t', help='定时时间（HH:MM 格式）')
    
    # config 命令
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--show', action='store_true', help='显示当前配置')
    config_parser.add_argument('--init', action='store_true', help='初始化配置文件')
    
    return parser


async def run_command(args):
    """执行命令"""
    engine = SigninEngine()
    
    if args.command == 'add':
        engine.add_account(args.platform, args.username, args.cookie)
        logger.info(f"✅ 账号添加成功：{args.platform} - {args.username}")
    
    elif args.command == 'signin':
        if args.platform:
            logger.info(f"开始签到：{args.platform}")
            accounts = engine.list_accounts(args.platform)
            for acc in accounts:
                result = await engine.signin(args.platform, acc)
                print(f"  {'✅' if result['success'] else '❌'} {result['message']}")
        else:
            logger.info("开始批量签到")
            await engine.signin_all()
    
    elif args.command == 'history':
        history = engine.get_history(platform=args.platform, limit=args.limit)
        if not history:
            print("暂无签到记录")
            return
        
        print(f"\n{'='*60}")
        print(f"{'时间':<20} {'平台':<12} {'用户':<15} {'状态':<8} {'详情'}")
        print(f"{'='*60}")
        for record in history:
            status = '✅' if record['success'] else '❌'
            print(f"{record['timestamp']:<20} {record['platform']:<12} {record['username']:<15} {status:<8} {record['message']}")
        print(f"{'='*60}\n")
    
    elif args.command == 'stats':
        stats = engine.get_stats(days=args.days)
        print(f"\n📊 最近 {args.days} 天统计")
        print(f"  总签到次数：{stats['total']}")
        print(f"  成功：{stats['success']}")
        print(f"  失败：{stats['failure']}")
        print(f"  成功率：{stats['success_rate']:.2f}%")
        
        if stats['recent']:
            print(f"\n  按平台统计:")
            for item in stats['recent']:
                print(f"    {item['platform']}: {item['success_count']}/{item['count']}")
        print()
    
    elif args.command == 'perf':
        perf = engine.get_performance_stats(days=args.days)
        print(f"\n⚡ 性能统计（最近 {args.days} 天）")
        print(f"  总签到次数：{perf['total_signins']}")
        print(f"  平均耗时：{perf['avg_duration']:.2f}秒")
        
        if perf.get('platform_stats'):
            print(f"\n  按平台性能:")
            for platform, data in perf['platform_stats'].items():
                print(f"    {platform}: 成功率 {data['success_rate']}, 平均耗时 {data['avg_duration']:.2f}秒")
        print()
    
    elif args.command == 'platforms':
        platforms = engine.get_platforms()
        print(f"\n🎯 支持的平台 ({len(platforms)}个):")
        print(f"{'平台':<15} {'代码':<15} {'需要 Cookie':<12} {'重试次数':<10}")
        print("=" * 60)
        for p in platforms:
            print(f"{p['name']:<15} {p['code']:<15} {'是' if p['cookies_required'] else '否':<12} {p['max_retries']:<10}")
        print("=" * 60)
        print("\n提示：使用 'add <平台代码>' 添加账号，例如：add netease")
        print()
    
    elif args.command == 'list':
        accounts = engine.list_accounts(platform=args.platform)
        if not accounts:
            print("暂无账号")
            return
        
        print(f"\n{'='*60}")
        print(f"{'平台':<15} {'用户名':<20} {'添加时间'}")
        print(f"{'='*60}")
        for acc in accounts:
            print(f"{acc['platform']:<15} {acc['username']:<20} {acc['created_at']}")
        print(f"{'='*60}\n")
    
    elif args.command == 'remove':
        engine.remove_account(args.platform, args.username)
        logger.info(f"✅ 账号已删除：{args.platform} - {args.username}")
    
    elif args.command == 'schedule':
        if args.enable:
            config.set('schedule.enabled', True)
            config.save()
            logger.info("✅ 定时任务已启用")
        elif args.disable:
            config.set('schedule.enabled', False)
            config.save()
            logger.info("✅ 定时任务已禁用")
        if args.time:
            config.set('schedule.time', args.time)
            config.save()
            logger.info(f"✅ 定时时间已设置为：{args.time}")
    
    elif args.command == 'config':
        if args.show:
            import json
            print("\n当前配置:")
            print(json.dumps(config.settings, indent=2, ensure_ascii=False))
            print()
        elif args.init:
            config.save()
            logger.info(f"✅ 配置文件已生成：{config.config_file}")


def main():
    """主函数"""
    parser = setup_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 设置日志
    log_file = Path(__file__).parent.parent.parent / 'data' / 'autosignin.log'
    setup_logger(log_file=str(log_file))
    
    # 执行命令
    asyncio.run(run_command(args))


if __name__ == '__main__':
    main()
