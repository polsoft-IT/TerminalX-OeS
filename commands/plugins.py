"""
 ============================================================
  MODULE/PLUGIN NAME: PluginsCommands
  VERSION: 1.0.0
  MODULE CLASS: PluginsCommands
  DESCRIPTION:
       Plugin management command handlers for plugin operations

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


class PluginsCommands:
    """Plugin command handlers"""
    
    def __init__(self, ai_plugins):
        self.plugins = ai_plugins
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a plugin command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown plugin command: {command}',
            }
            
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List all loaded plugins"""
        plugins = await self.plugins.list_plugins()
        
        return {
            'success': True,
            'output': plugins
        }
        
    async def cmd_load(self, *args) -> Dict[str, Any]:
        """Load a plugin"""
        if not args:
            return {'success': False, 'error': 'Usage: load <plugin_name>'}
            
        success = await self.plugins.load(args[0])
        
        return {
            'success': success,
            'output': f'Loaded plugin {args[0]}' if success else 'Failed to load plugin'
        }
        
    async def cmd_unload(self, *args) -> Dict[str, Any]:
        """Unload a plugin"""
        if not args:
            return {'success': False, 'error': 'Usage: unload <plugin_name>'}
            
        success = await self.plugins.unload(args[0])
        
        return {
            'success': success,
            'output': f'Unloaded plugin {args[0]}' if success else 'Failed to unload plugin'
        }
        
    async def cmd_reload(self, *args) -> Dict[str, Any]:
        """Reload a plugin"""
        if not args:
            return {'success': False, 'error': 'Usage: reload <plugin_name>'}

        success = await self.plugins.reload(args[0])

        return {
            'success': success,
            'output': f'Reloaded plugin {args[0]}' if success else 'Failed to reload plugin'
        }

    async def cmd_hooks(self, *args) -> Dict[str, Any]:
        """List hooks (redirects to plugin command)"""
        return {
            'success': False,
            'error': 'Hooks command is available in the GODMODE plugin system. Use "plugin hooks" instead.'
        }

    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Show plugin status (redirects to plugin command)"""
        return {
            'success': False,
            'error': 'Status command is available in the GODMODE plugin system. Use "plugin status" instead.'
        }
