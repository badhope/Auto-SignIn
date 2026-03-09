"""
数据库管理
使用 SQLite 存储签到历史
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class Database:
    """数据库管理类"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._init_db()
    
    def connect(self):
        """连接数据库"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def _init_db(self):
        """初始化数据库表"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 签到历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signin_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                username TEXT,
                success BOOLEAN NOT NULL,
                message TEXT,
                points INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error TEXT
            )
        ''')
        
        # 账号表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                username TEXT NOT NULL,
                cookies TEXT,
                tokens TEXT,
                enabled BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(platform, username)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_platform ON signin_history(platform)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_timestamp ON signin_history(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_accounts_platform ON accounts(platform)')
        
        conn.commit()
    
    def add_signin_record(self, platform: str, username: str, success: bool, 
                          message: str = None, points: int = None, error: str = None):
        """添加签到记录"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO signin_history (platform, username, success, message, points, error)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (platform, username, success, message, points, error))
        conn.commit()
        return cursor.lastrowid
    
    def get_history(self, platform: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取签到历史"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if platform:
            cursor.execute('''
                SELECT * FROM signin_history 
                WHERE platform = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (platform, limit))
        else:
            cursor.execute('''
                SELECT * FROM signin_history 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def add_account(self, platform: str, username: str, cookies: str = None, tokens: str = None):
        """添加账号"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO accounts (platform, username, cookies, tokens, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (platform, username, cookies, tokens))
        conn.commit()
    
    def get_accounts(self, platform: str = None, enabled: bool = True) -> List[Dict[str, Any]]:
        """获取账号列表"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if platform:
            cursor.execute('''
                SELECT * FROM accounts 
                WHERE platform = ? AND enabled = ?
            ''', (platform, enabled))
        else:
            cursor.execute('''
                SELECT * FROM accounts 
                WHERE enabled = ?
            ''', (enabled,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def delete_account(self, platform: str, username: str):
        """删除账号"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM accounts 
            WHERE platform = ? AND username = ?
        ''', (platform, username))
        conn.commit()
    
    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """获取统计数据"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 总签到次数
        cursor.execute('SELECT COUNT(*) as total FROM signin_history')
        total = cursor.fetchone()['total']
        
        # 成功次数
        cursor.execute('SELECT COUNT(*) as success FROM signin_history WHERE success = 1')
        success = cursor.fetchone()['success']
        
        # 最近 7 天签到情况 - 使用参数化查询避免 SQL 注入
        cursor.execute('''
            SELECT platform, COUNT(*) as count, 
                   SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
            FROM signin_history 
            WHERE timestamp >= datetime('now', ? || ' days')
            GROUP BY platform
        ''', (f'-{days}',))
        recent = cursor.fetchall()
        
        return {
            'total': total,
            'success': success,
            'failure': total - success,
            'success_rate': (success / total * 100) if total > 0 else 0,
            'recent': [dict(row) for row in recent]
        }
