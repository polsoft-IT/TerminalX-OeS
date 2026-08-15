"""
 ============================================================
  MODULE/PLUGIN NAME: AlertCommands
  VERSION: 1.0.0
  MODULE CLASS: AlertCommands
  DESCRIPTION:
       Alert command handlers for TerminalX alerting system

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
from typing import Dict, Any
from core import AlertLevel, AlertChannel, ANSI


class AlertCommands:
    """Alert command handlers"""
    
    def __init__(self, alert_module):
        self.alert_module = alert_module
    
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute an alert command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown alert command: {command}'
            }
    
    async def cmd_send(self, *args) -> Dict[str, Any]:
        """Send an alert"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: alert send <level> <message> [title]'
            }
        
        level_str = args[0].lower()
        message = ' '.join(args[1:-1]) if len(args) > 2 else ' '.join(args[1:])
        title = args[-1] if len(args) > 2 else None
        
        try:
            level = AlertLevel(level_str)
        except ValueError:
            return {
                'success': False,
                'error': f'Invalid level: {level_str}. Valid: info, warning, error, critical, security'
            }
        
        result = await self.alert_module.alert(
            level=level,
            message=message,
            title=title
        )
        
        return {
            'success': True,
            'output': f'Alert sent: {level.value.upper()} - {message}',
            'result': result
        }
    
    async def cmd_email(self, *args) -> Dict[str, Any]:
        """Configure email alerts"""
        if len(args) < 5:
            return {
                'success': False,
                'error': 'Usage: alert email <host> <port> <user> <password> <sender> [use_tls]'
            }
        
        host = args[0]
        port = int(args[1])
        user = args[2]
        password = args[3]
        sender = args[4]
        use_tls = args[5].lower() == 'true' if len(args) > 5 else True
        
        self.alert_module.configure_email(host, port, user, password, sender, use_tls)
        
        return {
            'success': True,
            'output': f'Email configured: {sender}@{host}:{port}'
        }
    
    async def cmd_sms(self, *args) -> Dict[str, Any]:
        """Configure SMS alerts"""
        if len(args) < 3:
            return {
                'success': False,
                'error': 'Usage: alert sms <provider_url> <api_key> <recipient>'
            }
        
        provider_url = args[0]
        api_key = args[1]
        recipient = args[2]
        
        self.alert_module.configure_sms(provider_url, api_key, recipient)
        
        return {
            'success': True,
            'output': f'SMS configured for recipient: {recipient}'
        }
    
    async def cmd_webhook(self, *args) -> Dict[str, Any]:
        """Manage webhook URLs"""
        if not args:
            # List webhooks
            if not self.alert_module.webhook_urls:
                return {
                    'success': True,
                    'output': 'No webhooks configured'
                }
            return {
                'success': True,
                'output': '\n'.join(f'- {url}' for url in self.alert_module.webhook_urls)
            }
        
        action = args[0].lower()
        
        if action == 'add':
            if len(args) < 2:
                return {
                    'success': False,
                    'error': 'Usage: alert webhook add <url>'
                }
            url = args[1]
            self.alert_module.add_webhook(url)
            return {
                'success': True,
                'output': f'Webhook added: {url}'
            }
        
        elif action == 'remove':
            if len(args) < 2:
                return {
                    'success': False,
                    'error': 'Usage: alert webhook remove <url>'
                }
            url = args[1]
            self.alert_module.remove_webhook(url)
            return {
                'success': True,
                'output': f'Webhook removed: {url}'
            }
        
        else:
            return {
                'success': False,
                'error': 'Usage: alert webhook [add|remove] [url]'
            }
    
    async def cmd_terminal(self, *args) -> Dict[str, Any]:
        """Enable/disable terminal alerts"""
        if not args:
            enabled = self.alert_module.terminal_enabled
            return {
                'success': True,
                'output': f'Terminal alerts: {"enabled" if enabled else "disabled"}'
            }
        
        enabled = args[0].lower() == 'true' or args[0].lower() == 'on' or args[0].lower() == 'enable'
        self.alert_module.terminal_enabled = enabled
        
        return {
            'success': True,
            'output': f'Terminal alerts {"enabled" if enabled else "disabled"}'
        }
    
    async def cmd_desktop(self, *args) -> Dict[str, Any]:
        """Enable/disable desktop notifications"""
        if not args:
            enabled = self.alert_module.desktop_enabled
            return {
                'success': True,
                'output': f'Desktop notifications: {"enabled" if enabled else "disabled"}'
            }
        
        enabled = args[0].lower() == 'true' or args[0].lower() == 'on' or args[0].lower() == 'enable'
        self.alert_module.desktop_enabled = enabled
        
        return {
            'success': True,
            'output': f'Desktop notifications {"enabled" if enabled else "disabled"}'
        }
    
    async def cmd_routing(self, *args) -> Dict[str, Any]:
        """Configure alert routing rules"""
        if not args:
            # Show current routing rules
            output = []
            for level, channels in self.alert_module.routing_rules.items():
                channel_names = [ch.value for ch in channels]
                output.append(f'{level.value}: {", ".join(channel_names)}')
            return {
                'success': True,
                'output': '\n'.join(output)
            }
        
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: alert routing <level> <channel1,channel2,...>'
            }
        
        level_str = args[0].lower()
        channels_str = args[1]
        
        try:
            level = AlertLevel(level_str)
        except ValueError:
            return {
                'success': False,
                'error': f'Invalid level: {level_str}. Valid: info, warning, error, critical, security'
            }
        
        try:
            channels = [AlertChannel(ch.strip().lower()) for ch in channels_str.split(',')]
            self.alert_module.routing_rules[level] = channels
            channel_names = [ch.value for ch in channels]
            return {
                'success': True,
                'output': f'Routing updated: {level.value} -> {", ".join(channel_names)}'
            }
        except ValueError as e:
            return {
                'success': False,
                'error': f'Invalid channel: {e}. Valid: terminal, email, sms, webhook, desktop'
            }
    
    async def cmd_history(self, *args) -> Dict[str, Any]:
        """View alert history"""
        level = None
        limit = None
        
        for arg in args:
            if arg.startswith('--level='):
                level_str = arg.split('=')[1]
                try:
                    level = AlertLevel(level_str.lower())
                except ValueError:
                    return {
                        'success': False,
                        'error': f'Invalid level: {level_str}'
                    }
            elif arg.startswith('--limit='):
                limit = int(arg.split('=')[1])
        
        history = await self.alert_module.get_alert_history(level=level, limit=limit)
        
        if not history:
            return {
                'success': True,
                'output': 'No alerts in history'
            }
        
        output = []
        for alert in history:
            output.append(f"[{alert['level'].upper()}] {alert['timestamp']}")
            output.append(f"  {alert['title']}")
            output.append(f"  {alert['message']}")
            output.append()
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_clear_history(self, *args) -> Dict[str, Any]:
        """Clear alert history"""
        await self.alert_module.clear_history()
        return {
            'success': True,
            'output': 'Alert history cleared'
        }
    
    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Show alert statistics"""
        stats = await self.alert_module.get_stats()
        
        output = []
        output.append(f"Total alerts: {stats['total_alerts']}")
        output.append("\nBy level:")
        for level, count in stats['by_level'].items():
            output.append(f"  {level}: {count}")
        
        output.append("\nChannel stats:")
        for channel, data in stats['channel_stats'].items():
            output.append(f"  {channel}: {data['success']} success, {data['failed']} failed")
        
        output.append("\nEnabled channels:")
        for channel, enabled in stats['enabled_channels'].items():
            if isinstance(enabled, bool):
                status = "enabled" if enabled else "disabled"
            else:
                status = str(enabled)
            output.append(f"  {channel}: {status}")
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_test(self, *args) -> Dict[str, Any]:
        """Send test alerts to all configured channels"""
        result = await self.alert_module.test_alerts()
        
        output = []
        output.append("Test alerts sent to configured channels:")
        for channel, result_data in result['results'].items():
            status = "✓" if result_data.get('success') else "✗"
            output.append(f"  {status} {channel}: {result_data.get('error', 'OK') if not result_data.get('success') else 'OK'}")
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_enable(self, *args) -> Dict[str, Any]:
        """Enable alert module"""
        self.alert_module.enabled = True
        return {
            'success': True,
            'output': 'Alert module enabled'
        }
    
    async def cmd_disable(self, *args) -> Dict[str, Any]:
        """Disable alert module"""
        self.alert_module.enabled = False
        return {
            'success': True,
            'output': 'Alert module disabled'
        }
    
    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Show alert module status"""
        status = {
            'enabled': self.alert_module.enabled,
            'terminal_enabled': self.alert_module.terminal_enabled,
            'desktop_enabled': self.alert_module.desktop_enabled,
            'email_configured': self.alert_module.email_config is not None,
            'sms_configured': self.alert_module.sms_config is not None,
            'webhook_count': len(self.alert_module.webhook_urls),
            'max_retries': self.alert_module.max_retries,
            'retry_delay': self.alert_module.retry_delay
        }
        
        output = []
        output.append(f"Alert module: {'enabled' if status['enabled'] else 'disabled'}")
        output.append(f"Terminal alerts: {'enabled' if status['terminal_enabled'] else 'disabled'}")
        output.append(f"Desktop notifications: {'enabled' if status['desktop_enabled'] else 'disabled'}")
        output.append(f"Email: {'configured' if status['email_configured'] else 'not configured'}")
        output.append(f"SMS: {'configured' if status['sms_configured'] else 'not configured'}")
        output.append(f"Webhooks: {status['webhook_count']} configured")
        output.append(f"Max retries: {status['max_retries']}")
        output.append(f"Retry delay: {status['retry_delay']}s")
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
