"""
 ============================================================
  MODULE: AlertModule
  VERSION: 2.0.0
  MODULE CLASS: AlertModule
  DESCRIPTION:
       Full alerting system: email, SMS, webhook, terminal, desktop.
       Integrates with security module, geolocation, IDS/IPS.
       Async support with proper error handling and retry logic.

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

import asyncio
import json
import smtplib
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from enum import Enum

try:
    import aiohttp
except ImportError:
    aiohttp = None  # HTTP notifications disabled until 'pip install aiohttp'


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SECURITY = "security"


class AlertChannel(Enum):
    """Available alert channels"""
    TERMINAL = "terminal"
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    DESKTOP = "desktop"


class AlertModule:
    """Enhanced alerting system with multiple channels and async support"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.enabled = True
        
        # Channel configurations
        self.email_config: Optional[Dict[str, Any]] = None
        self.sms_config: Optional[Dict[str, Any]] = None
        self.webhook_urls: List[str] = []
        self.terminal_enabled = True
        self.desktop_enabled = False
        
        # Alert routing rules
        self.routing_rules: Dict[AlertLevel, List[AlertChannel]] = {
            AlertLevel.INFO: [AlertChannel.TERMINAL],
            AlertLevel.WARNING: [AlertChannel.TERMINAL, AlertChannel.EMAIL],
            AlertLevel.ERROR: [AlertChannel.TERMINAL, AlertChannel.EMAIL, AlertChannel.WEBHOOK],
            AlertLevel.CRITICAL: [AlertChannel.TERMINAL, AlertChannel.EMAIL, AlertChannel.SMS, AlertChannel.WEBHOOK],
            AlertLevel.SECURITY: [AlertChannel.TERMINAL, AlertChannel.EMAIL, AlertChannel.SMS, AlertChannel.WEBHOOK]
        }
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        
        # Rate limiting
        self.rate_limits: Dict[str, Dict[str, Any]] = {
            'email': {'max_per_minute': 10, 'count': 0, 'reset_time': None},
            'sms': {'max_per_minute': 5, 'count': 0, 'reset_time': None},
            'webhook': {'max_per_minute': 20, 'count': 0, 'reset_time': None}
        }
        
        # Alert history
        self.alert_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
        # Callbacks
        self.alert_callbacks: List[Callable] = []
        
        # Notification system integration
        self.notification_system = None
        
    async def initialize(self, config: Optional[Dict[str, Any]] = None):
        """Initialize alert module with configuration"""
        if config:
            self.enabled = config.get('enabled', True)
            self.terminal_enabled = config.get('terminal_enabled', True)
            self.desktop_enabled = config.get('desktop_enabled', False)
            self.max_retries = config.get('max_retries', 3)
            self.retry_delay = config.get('retry_delay', 5)
            
            # Load email config
            if 'email' in config:
                self.email_config = config['email']
            
            # Load SMS config
            if 'sms' in config:
                self.sms_config = config['sms']
            
            # Load webhooks
            if 'webhooks' in config:
                self.webhook_urls = config['webhooks']
            
            # Load custom routing rules
            if 'routing_rules' in config:
                self._load_routing_rules(config['routing_rules'])
        
        self.logger.info("AlertModule initialized")
    
    def set_notification_system(self, notification_system):
        """Set reference to notification system for integration"""
        self.notification_system = notification_system
    
    def _load_routing_rules(self, rules: Dict[str, List[str]]):
        """Load custom routing rules from config"""
        for level_str, channels in rules.items():
            try:
                level = AlertLevel(level_str)
                channel_list = [AlertChannel(ch) for ch in channels]
                self.routing_rules[level] = channel_list
            except ValueError:
                self.logger.warning(f"Invalid routing rule: {level_str}")
    
    def add_webhook(self, url: str):
        """Add webhook URL for alerts"""
        if url not in self.webhook_urls:
            self.webhook_urls.append(url)
            self.logger.info(f"Added webhook: {url}")
    
    def remove_webhook(self, url: str):
        """Remove webhook URL"""
        if url in self.webhook_urls:
            self.webhook_urls.remove(url)
            self.logger.info(f"Removed webhook: {url}")
    
    def configure_email(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        sender: str,
        use_tls: bool = True
    ):
        """Configure email settings"""
        self.email_config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "sender": sender,
            "use_tls": use_tls
        }
        self.logger.info("Email configured")
    
    def configure_sms(self, provider_url: str, api_key: str, recipient: str):
        """Configure SMS settings"""
        self.sms_config = {
            "provider": provider_url,
            "api_key": api_key,
            "recipient": recipient
        }
        self.logger.info("SMS configured")
    
    def add_alert_callback(self, callback: Callable):
        """Add callback for alert events"""
        self.alert_callbacks.append(callback)
    
    def remove_alert_callback(self, callback: Callable):
        """Remove alert callback"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)
    
    async def alert(
        self,
        level: AlertLevel,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        channels: Optional[List[AlertChannel]] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send alert through configured channels"""
        if not self.enabled:
            return {'success': False, 'error': 'Alert module disabled'}
        
        # Create alert payload
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "title": title or f"ALERT-{level.value.upper()}",
            "message": message,
            "data": data or {}
        }
        
        # Determine channels to use
        if channels is None:
            channels = self.routing_rules.get(level, [AlertChannel.TERMINAL])
        
        # Add to history
        self._add_to_history(payload)
        
        # Send to notification system if available
        if self.notification_system:
            try:
                from core import NotificationType, NotificationPriority
                notif_type = self._map_alert_level_to_type(level)
                notif_priority = self._map_alert_level_to_priority(level)
                await self.notification_system.create(
                    title=payload['title'],
                    message=message,
                    notification_type=notif_type,
                    priority=notif_priority,
                    metadata=data
                )
            except Exception as e:
                self.logger.error(f"Failed to create notification: {e}")
        
        # Dispatch to channels
        results = {}
        tasks = []
        
        for channel in channels:
            if channel == AlertChannel.TERMINAL and self.terminal_enabled:
                tasks.append(self._terminal(payload))
            elif channel == AlertChannel.EMAIL and self.email_config:
                tasks.append(self._email(payload))
            elif channel == AlertChannel.SMS and self.sms_config:
                tasks.append(self._sms(payload))
            elif channel == AlertChannel.WEBHOOK and self.webhook_urls:
                tasks.append(self._webhook(payload))
            elif channel == AlertChannel.DESKTOP and self.desktop_enabled:
                tasks.append(self._desktop(payload))
        
        if tasks:
            channel_results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(channel_results):
                channel_name = channels[i].value
                if isinstance(result, Exception):
                    results[channel_name] = {'success': False, 'error': str(result)}
                else:
                    results[channel_name] = result
        
        # Call callbacks
        for callback in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(payload, results)
                else:
                    callback(payload, results)
            except Exception as e:
                self.logger.error(f"Alert callback error: {e}")
        
        payload['results'] = results
        return payload
    
    def _add_to_history(self, payload: Dict[str, Any]):
        """Add alert to history"""
        self.alert_history.append(payload)
        if len(self.alert_history) > self.max_history:
            self.alert_history.pop(0)
    
    def _map_alert_level_to_type(self, level: AlertLevel):
        """Map alert level to notification type"""
        from core import NotificationType
        mapping = {
            AlertLevel.INFO: NotificationType.INFO,
            AlertLevel.WARNING: NotificationType.WARNING,
            AlertLevel.ERROR: NotificationType.ERROR,
            AlertLevel.CRITICAL: NotificationType.ERROR,
            AlertLevel.SECURITY: NotificationType.SECURITY
        }
        return mapping.get(level, NotificationType.INFO)
    
    def _map_alert_level_to_priority(self, level: AlertLevel):
        """Map alert level to notification priority"""
        from core import NotificationPriority
        mapping = {
            AlertLevel.INFO: NotificationPriority.LOW,
            AlertLevel.WARNING: NotificationPriority.MEDIUM,
            AlertLevel.ERROR: NotificationPriority.HIGH,
            AlertLevel.CRITICAL: NotificationPriority.CRITICAL,
            AlertLevel.SECURITY: NotificationPriority.CRITICAL
        }
        return mapping.get(level, NotificationPriority.MEDIUM)
    
    async def _terminal(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert to terminal"""
        try:
            from core import ANSI
            
            level_colors = {
                'info': ANSI.CYAN,
                'warning': ANSI.YELLOW,
                'error': ANSI.RED,
                'critical': ANSI.BOLD + ANSI.RED,
                'security': ANSI.BOLD + ANSI.MAGENTA
            }
            
            color = level_colors.get(payload['level'], ANSI.WHITE)
            print(f"{color}[{payload['level'].upper()}] {payload['timestamp']}{ANSI.RESET}")
            print(f"{color}{payload['title']}{ANSI.RESET}")
            print(payload["message"])
            
            if payload["data"]:
                print(f"{ANSI.DIM}{json.dumps(payload['data'], indent=2)}{ANSI.RESET}")
            
            print()
            
            return {'success': True, 'channel': 'terminal'}
        except Exception as e:
            self.logger.error(f"Terminal alert failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _email(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert via email"""
        if not self._check_rate_limit('email'):
            return {'success': False, 'error': 'Rate limit exceeded'}
        
        for attempt in range(self.max_retries):
            try:
                msg = MIMEMultipart()
                msg['From'] = self.email_config["sender"]
                msg['To'] = self.email_config["user"]
                msg['Subject'] = f"{payload['title']} - {payload['level'].upper()}"
                
                body = f"""
Alert Details:
-------------
Level: {payload['level'].upper()}
Time: {payload['timestamp']}
Title: {payload['title']}

Message:
{payload['message']}

Data:
{json.dumps(payload['data'], indent=2)}
"""
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Run SMTP in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    self._send_email_sync,
                    msg
                )
                
                self._increment_rate_limit('email')
                return {'success': True, 'channel': 'email'}
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    self.logger.error(f"Email alert failed after {self.max_retries} attempts: {e}")
                    return {'success': False, 'error': str(e)}
        
        return {'success': False, 'error': 'Max retries exceeded'}
    
    def _send_email_sync(self, msg: MIMEMultipart):
        """Synchronous email sending"""
        server = smtplib.SMTP(self.email_config["host"], self.email_config["port"])
        if self.email_config.get("use_tls", True):
            server.starttls()
        server.login(self.email_config["user"], self.email_config["password"])
        server.sendmail(self.email_config["sender"], self.email_config["user"], msg.as_string())
        server.quit()
    
    async def _sms(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert via SMS"""
        if not self._check_rate_limit('sms'):
            return {'success': False, 'error': 'Rate limit exceeded'}
        
        for attempt in range(self.max_retries):
            try:
                if aiohttp is None:
                    raise RuntimeError("aiohttp not installed - SMS alerts unavailable (pip install aiohttp)")
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {self.sms_config['api_key']}",
                        "Content-Type": "application/json"
                    }

                    sms_data = {
                        "recipient": self.sms_config["recipient"],
                        "message": f"[{payload['level'].upper()}] {payload['title']}: {payload['message'][:100]}"
                    }

                    async with session.post(
                        self.sms_config["provider"],
                        headers=headers,
                        json=sms_data,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status == 200:
                            self._increment_rate_limit('sms')
                            return {'success': True, 'channel': 'sms'}
                        else:
                            error_text = await response.text()
                            raise Exception(f"SMS API error: {response.status} - {error_text}")

            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    self.logger.error(f"SMS alert failed after {self.max_retries} attempts: {e}")
                    return {'success': False, 'error': str(e)}

        return {'success': False, 'error': 'Max retries exceeded'}

    async def _webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send alert via webhook"""
        if not self._check_rate_limit('webhook'):
            return {'success': False, 'error': 'Rate limit exceeded'}

        results = []

        for url in self.webhook_urls:
            for attempt in range(self.max_retries):
                try:
                    if aiohttp is None:
                        raise RuntimeError("aiohttp not installed - webhook alerts unavailable (pip install aiohttp)")
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url,
                            json=payload,
                            timeout=aiohttp.ClientTimeout(total=30)
                        ) as response:
                            if response.status < 400:
                                results.append({'url': url, 'success': True})
                                break
                            else:
                                error_text = await response.text()
                                raise Exception(f"Webhook error: {response.status} - {error_text}")
                                
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(self.retry_delay)
                    else:
                        results.append({'url': url, 'success': False, 'error': str(e)})
        
        self._increment_rate_limit('webhook')
        
        return {
            'success': all(r.get('success', False) for r in results),
            'channel': 'webhook',
            'results': results
        }
    
    async def _desktop(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send desktop notification"""
        try:
            # Try different desktop notification libraries
            try:
                from plyer import notification
                notification.notify(
                    title=payload['title'],
                    message=payload['message'],
                    app_name='TerminalX',
                    timeout=10
                )
                return {'success': True, 'channel': 'desktop'}
            except ImportError:
                # Fallback to platform-specific methods
                import platform
                system = platform.system()
                
                if system == 'Windows':
                    import subprocess
                    subprocess.run([
                        'powershell',
                        '-Command',
                        f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('{payload['message']}', '{payload['title']}')"
                    ])
                    return {'success': True, 'channel': 'desktop'}
                elif system == 'Darwin':  # macOS
                    import subprocess
                    subprocess.run([
                        'osascript',
                        '-e',
                        f'display notification "{payload["message"]}" with title "{payload["title"]}"'
                    ])
                    return {'success': True, 'channel': 'desktop'}
                elif system == 'Linux':
                    import subprocess
                    subprocess.run([
                        'notify-send',
                        payload['title'],
                        payload['message']
                    ])
                    return {'success': True, 'channel': 'desktop'}
                else:
                    return {'success': False, 'error': 'Unsupported platform'}
                    
        except Exception as e:
            self.logger.error(f"Desktop notification failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _check_rate_limit(self, channel: str) -> bool:
        """Check if rate limit allows sending"""
        limit = self.rate_limits.get(channel)
        if not limit:
            return True
        
        now = datetime.now()
        
        # Reset counter if time window passed
        if limit['reset_time'] is None or (now - limit['reset_time']).total_seconds() >= 60:
            limit['count'] = 0
            limit['reset_time'] = now
        
        return limit['count'] < limit['max_per_minute']
    
    def _increment_rate_limit(self, channel: str):
        """Increment rate limit counter"""
        limit = self.rate_limits.get(channel)
        if limit:
            limit['count'] += 1
    
    async def get_alert_history(
        self,
        level: Optional[AlertLevel] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get alert history with optional filtering"""
        history = self.alert_history
        
        if level:
            history = [a for a in history if a['level'] == level.value]
        
        if limit:
            history = history[-limit:]
        
        return history
    
    async def clear_history(self):
        """Clear alert history"""
        self.alert_history.clear()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get alert statistics"""
        total = len(self.alert_history)
        
        level_counts = {}
        for alert in self.alert_history:
            level = alert['level']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        channel_success = {}
        for alert in self.alert_history:
            if 'results' in alert:
                for channel, result in alert['results'].items():
                    if channel not in channel_success:
                        channel_success[channel] = {'success': 0, 'failed': 0}
                    if result.get('success'):
                        channel_success[channel]['success'] += 1
                    else:
                        channel_success[channel]['failed'] += 1
        
        return {
            'total_alerts': total,
            'by_level': level_counts,
            'channel_stats': channel_success,
            'enabled_channels': {
                'terminal': self.terminal_enabled,
                'email': self.email_config is not None,
                'sms': self.sms_config is not None,
                'webhook': len(self.webhook_urls),
                'desktop': self.desktop_enabled
            }
        }
    
    async def test_alerts(self) -> Dict[str, Any]:
        """Send test alerts to all configured channels"""
        test_payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "info",
            "title": "TEST ALERT",
            "message": "This is a test alert from TerminalX AlertModule",
            "data": {"test": True}
        }
        
        results = {}
        
        if self.terminal_enabled:
            results['terminal'] = await self._terminal(test_payload)
        
        if self.email_config:
            results['email'] = await self._email(test_payload)
        
        if self.sms_config:
            results['sms'] = await self._sms(test_payload)
        
        if self.webhook_urls:
            results['webhook'] = await self._webhook(test_payload)
        
        if self.desktop_enabled:
            results['desktop'] = await self._desktop(test_payload)
        
        return {
            'success': True,
            'message': 'Test alerts sent',
            'results': results
        }


# Global instance
alert_module = AlertModule()
