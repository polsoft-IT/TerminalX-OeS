"""
 ============================================================
  MODULE/PLUGIN NAME: EventCommands
  VERSION: 1.0.0
  MODULE CLASS: EventCommands
  DESCRIPTION:
       Event bus command handlers for global event system

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


class EventCommands:
    """Event bus command handlers"""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute an event bus command"""
        handler = getattr(self, f'cmd_{command}', None)

        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown event command: {command}',
            }

    async def cmd_emit(self, *args) -> Dict[str, Any]:
        """Emit an event"""
        if not args:
            return {'success': False, 'error': 'Usage: event emit <event_name> [data]'}

        event_name = args[0]
        data = args[1] if len(args) > 1 else None

        try:
            await self.event_bus.emit(event_name, data)
            return {
                'success': True,
                'output': f'Event emitted: {event_name}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Get event bus status"""
        try:
            status = self.event_bus.diagnose()
            return {
                'success': True,
                'output': status
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_config(self, *args) -> Dict[str, Any]:
        """Show or update configuration"""
        if not args:
            return {
                'success': True,
                'output': self.event_bus.config
            }

        # Simple config update (key=value format)
        if len(args) == 1 and '=' in args[0]:
            key, value = args[0].split('=', 1)

            # Convert value to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)

            self.event_bus.config_set(key, value)
            return {
                'success': True,
                'output': f'Configuration updated: {key} = {value}'
            }

        return {'success': False, 'error': 'Usage: event config [key=value]'}

    async def cmd_flush(self, *args) -> Dict[str, Any]:
        """Flush event queue"""
        try:
            await self.event_bus.flush()
            return {
                'success': True,
                'output': 'Event queue flushed'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_metadata(self, *args) -> Dict[str, Any]:
        """Get event bus metadata"""
        try:
            metadata = self.event_bus.get_metadata()
            return {
                'success': True,
                'output': metadata
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_errors(self, *args) -> Dict[str, Any]:
        """Get error logs"""
        try:
            errors = self.event_bus.get_errors()
            return {
                'success': True,
                'output': {
                    'errors': errors,
                    'count': len(errors)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_autofix(self, *args) -> Dict[str, Any]:
        """Auto-fix event bus issues"""
        try:
            result = self.event_bus.auto_fix()
            return {
                'success': True,
                'output': 'Event bus auto-fix executed'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_export(self, *args) -> Dict[str, Any]:
        """Export event bus state"""
        try:
            state = self.event_bus.export_state()
            return {
                'success': True,
                'output': state
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_api(self, *args) -> Dict[str, Any]:
        """List available API methods"""
        try:
            api = self.event_bus.api_list()
            return {
                'success': True,
                'output': {
                    'api_methods': api,
                    'total': len(api)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
