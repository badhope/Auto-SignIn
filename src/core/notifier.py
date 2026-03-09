"""
通知系统
支持：邮件、Telegram、Webhook
"""
import smtplib
import httpx
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from src.utils.logger import logger


class Notifier:
    """通知发送器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', False)
    
    async def send(self, title: str, message: str, data: Dict[str, Any] = None):
        """
        发送通知
        
        Args:
            title: 通知标题
            message: 通知内容
            data: 附加数据
        """
        if not self.enabled:
            logger.info("通知功能未启用")
            return
        
        # 邮件通知
        if self.config.get('email', {}).get('enabled'):
            await self._send_email(title, message, data)
        
        # Telegram 通知
        if self.config.get('telegram', {}).get('enabled'):
            await self._send_telegram(title, message, data)
        
        # Webhook 通知
        if self.config.get('webhook', {}).get('enabled'):
            await self._send_webhook(title, message, data)
    
    async def _send_email(self, title: str, message: str, data: Dict[str, Any] = None):
        """发送邮件通知"""
        try:
            email_config = self.config['email']
            
            msg = MIMEMultipart()
            msg['From'] = email_config['username']
            msg['To'] = email_config['to_email']
            msg['Subject'] = f"[Auto-SignIn] {title}"
            
            body = f"{message}\n\n"
            if data:
                body += f"\n详细信息:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件通知已发送：{title}")
        except Exception as e:
            logger.error(f"邮件发送失败：{e}")
    
    async def _send_telegram(self, title: str, message: str, data: Dict[str, Any] = None):
        """发送 Telegram 通知"""
        try:
            tg_config = self.config['telegram']
            url = f"https://api.telegram.org/bot{tg_config['bot_token']}/sendMessage"
            
            text = f"*{title}*\n\n{message}"
            if data:
                text += f"\n\n详细信息:\n```{json.dumps(data, indent=2, ensure_ascii=False)}```"
            
            payload = {
                'chat_id': tg_config['chat_id'],
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10)
                response.raise_for_status()
            
            logger.info(f"Telegram 通知已发送：{title}")
        except Exception as e:
            logger.error(f"Telegram 发送失败：{e}")
    
    async def _send_webhook(self, title: str, message: str, data: Dict[str, Any] = None):
        """发送 Webhook 通知"""
        try:
            webhook_config = self.config['webhook']
            
            payload = {
                'title': title,
                'message': message,
                'data': data or {}
            }
            
            async with httpx.AsyncClient() as client:
                if webhook_config.get('method', 'POST').upper() == 'POST':
                    response = await client.post(
                        webhook_config['url'],
                        json=payload,
                        timeout=10
                    )
                else:
                    response = await client.get(
                        webhook_config['url'],
                        params=payload,
                        timeout=10
                    )
                response.raise_for_status()
            
            logger.info(f"Webhook 通知已发送：{title}")
        except Exception as e:
            logger.error(f"Webhook 发送失败：{e}")
