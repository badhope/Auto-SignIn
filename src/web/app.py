"""
Web 控制界面
提供直观的 Web 界面进行配置管理、状态监控和操作控制
"""
import asyncio
from flask import Flask, render_template_string, jsonify, request
from src.core.engine import SigninEngine
from src.core.config import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-SignIn 控制台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 {
            color: #333;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
        }
        .stat {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .stat-value { font-size: 2.5em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn-danger { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .btn-success { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th { background: #f8f9fa; font-weight: 600; }
        .platform-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            background: #667eea;
            color: white;
        }
        .status-success { color: #28a745; }
        .status-failure { color: #dc3545; }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .tab-nav {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .tab-btn {
            padding: 10px 20px;
            border: none;
            background: #f0f0f0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .tab-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Auto-SignIn 控制台</h1>
        
        <div class="card">
            <h2>📊 统计概览</h2>
            <div class="grid" id="stats">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🚀 快速操作</h2>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button class="btn btn-success" onclick="runSignin()">执行签到</button>
                <button class="btn" onclick="refreshData()">刷新数据</button>
            </div>
        </div>
        
        <div class="card">
            <h2>📋 账号管理</h2>
            <div id="accounts">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📜 签到历史</h2>
            <div id="history">
                <div class="loading">加载中...</div>
            </div>
        </div>
        
        <div class="card">
            <h2>⚙️ 配置管理</h2>
            <div class="tab-nav">
                <button class="tab-btn active" onclick="showTab('schedule')">定时任务</button>
                <button class="tab-btn" onclick="showTab('notification')">通知设置</button>
            </div>
            <div id="schedule" class="tab-content active">
                <p><strong>定时任务：</strong> <span id="schedule-status">加载中...</span></p>
                <p><strong>执行时间：</strong> <span id="schedule-time">加载中...</span></p>
            </div>
            <div id="notification" class="tab-content">
                <p><strong>通知状态：</strong> <span id="notif-status">加载中...</span></p>
            </div>
        </div>
    </div>
    
    <script>
        let currentTab = 'schedule';
        
        function showTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tab).classList.add('active');
        }
        
        async function apiCall(endpoint, options = {}) {
            try {
                const response = await fetch('/api' + endpoint, {
                    ...options,
                    headers: { 'Content-Type': 'application/json' }
                });
                return await response.json();
            } catch (e) {
                console.error(e);
                return { error: e.message };
            }
        }
        
        async function refreshData() {
            const [stats, accounts, history, config] = await Promise.all([
                apiCall('/stats'),
                apiCall('/accounts'),
                apiCall('/history'),
                apiCall('/config')
            ]);
            
            document.getElementById('stats').innerHTML = `
                <div class="stat">
                    <div class="stat-value">${stats.total || 0}</div>
                    <div class="stat-label">总签到次数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.success || 0}</div>
                    <div class="stat-label">成功次数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.failure || 0}</div>
                    <div class="stat-label">失败次数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${stats.success_rate ? stats.success_rate.toFixed(1) : 0}%</div>
                    <div class="stat-label">成功率</div>
                </div>
            `;
            
            if (accounts.length === 0) {
                document.getElementById('accounts').innerHTML = '<p>暂无账号</p>';
            } else {
                document.getElementById('accounts').innerHTML = `
                    <table>
                        <thead>
                            <tr><th>平台</th><th>用户名</th><th>添加时间</th><th>操作</th></tr>
                        </thead>
                        <tbody>
                            ${accounts.map(a => `
                                <tr>
                                    <td><span class="platform-tag">${a.platform}</span></td>
                                    <td>${a.username}</td>
                                    <td>${a.created_at || '-'}</td>
                                    <td><button class="btn btn-danger" onclick="removeAccount('${a.platform}', '${a.username}')">删除</button></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
            }
            
            if (history.length === 0) {
                document.getElementById('history').innerHTML = '<p>暂无签到记录</p>';
            } else {
                document.getElementById('history').innerHTML = `
                    <table>
                        <thead>
                            <tr><th>时间</th><th>平台</th><th>用户名</th><th>状态</th><th>详情</th></tr>
                        </thead>
                        <tbody>
                            ${history.map(h => `
                                <tr>
                                    <td>${h.timestamp || '-'}</td>
                                    <td><span class="platform-tag">${h.platform}</span></td>
                                    <td>${h.username || '-'}</td>
                                    <td class="${h.success ? 'status-success' : 'status-failure'}">${h.success ? '✅ 成功' : '❌ 失败'}</td>
                                    <td>${h.message || '-'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
            }
            
            document.getElementById('schedule-status').textContent = config.schedule?.enabled ? '✅ 已启用' : '❌ 已禁用';
            document.getElementById('schedule-time').textContent = config.schedule?.time || '08:00';
            document.getElementById('notif-status').textContent = config.notification?.enabled ? '✅ 已启用' : '❌ 已禁用';
        }
        
        async function runSignin() {
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = '签到中...';
            
            const result = await apiCall('/signin', { method: 'POST' });
            
            btn.disabled = false;
            btn.textContent = '执行签到';
            
            alert(result.success ? '签到完成！' : '签到失败：' + result.message);
            refreshData();
        }
        
        async function removeAccount(platform, username) {
            if (!confirm(`确定删除 ${platform} - ${username}?`)) return;
            
            const result = await apiCall('/accounts/' + platform + '/' + encodeURIComponent(username), {
                method: 'DELETE'
            });
            
            alert(result.success ? '删除成功' : '删除失败');
            refreshData();
        }
        
        refreshData();
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/stats')
def get_stats():
    try:
        engine = SigninEngine()
        stats = engine.get_stats(days=7)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/accounts')
def get_accounts():
    try:
        engine = SigninEngine()
        accounts = engine.list_accounts()
        return jsonify(accounts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    try:
        engine = SigninEngine()
        history = engine.get_history(limit=20)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/config')
def get_config():
    return jsonify({
        'schedule': {
            'enabled': config.get('schedule.enabled'),
            'time': config.get('schedule.time')
        },
        'notification': {
            'enabled': config.get('notification.enabled')
        }
    })


@app.route('/api/signin', methods=['POST'])
def run_signin():
    try:
        engine = SigninEngine()
        result = asyncio.run(engine.signin_all())
        return jsonify({'success': True, 'message': '签到完成'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/accounts/<platform>/<username>', methods=['DELETE'])
def delete_account(platform, username):
    try:
        engine = SigninEngine()
        engine.remove_account(platform, username)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def run_web(host='0.0.0.0', port=8080):
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    run_web()
