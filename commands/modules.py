"""
 ============================================================
  MODULE/PLUGIN NAME: ModulesCommands
  VERSION: 1.0.0
  MODULE CLASS: ModulesCommands
  DESCRIPTION:
       Module management command handlers for module operations

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


class ModulesCommands:
    """Module command handlers"""
    
    def __init__(self, core_engine):
        self.core = core_engine
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a module command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown module command: {command}',
            }
            
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List all loaded modules"""
        return {
            'success': True,
            'output': list(self.core.subsystems.keys())
        }
        
    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Show module information"""
        if not args:
            return {'success': False, 'error': 'Usage: info <module_name>'}
            
        module = await self.core.get_subsystem(args[0])
        
        if module:
            return {
                'success': True,
                'output': {
                    'name': args[0],
                    'type': type(module).__name__,
                }
            }
        else:
            return {'success': False, 'error': 'Module not found'}
            
    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Show module status"""
        status = {}
        
        for name, module in self.core.subsystems.items():
            status[name] = {
                'loaded': True,
                'type': type(module).__name__,
            }
            
        return {
            'success': True,
            'output': status
        }
