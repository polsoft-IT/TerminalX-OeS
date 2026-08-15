"""
 ============================================================
  MODULE/PLUGIN NAME: SystemOptCommands
  VERSION: 2.0.0
  MODULE CLASS: SystemOptCommands
  DESCRIPTION:
       System Optimization command handlers for system optimization operations with v2 Windows API features

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


class SystemOptCommands:
    """System optimization command handlers"""

    def __init__(self, system_optimizer):
        self.optimizer = system_optimizer

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a system optimization command"""
        handler = getattr(self, f'cmd_{command}', None)

        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown system optimization command: {command}',
            }

    async def cmd_clean_ram(self, *args) -> Dict[str, Any]:
        """Clean RAM (legacy method - use clean_python_ram for v2)"""
        try:
            result = self.optimizer.clean_ram()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_clean_python_ram(self, *args) -> Dict[str, Any]:
        """Enhanced Python RAM cleaner (v2)"""
        try:
            result = self.optimizer.clean_python_ram()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_flush_pagefile(self, *args) -> Dict[str, Any]:
        """Real pagefile flush using NT API (v2)"""
        try:
            result = self.optimizer.flush_pagefile()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_trim_working_sets(self, *args) -> Dict[str, Any]:
        """Working set trim using Win32 API (v2)"""
        try:
            result = self.optimizer.trim_working_sets()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_flush_system_cache(self, *args) -> Dict[str, Any]:
        """System cache flush using NT API (v2)"""
        try:
            result = self.optimizer.flush_system_cache()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_optimize_cpu(self, *args) -> Dict[str, Any]:
        """Optimize CPU"""
        try:
            result = self.optimizer.optimize_cpu()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_clean_pagefile(self, *args) -> Dict[str, Any]:
        """Clean pagefile"""
        try:
            result = self.optimizer.clean_pagefile()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_scan(self, *args) -> Dict[str, Any]:
        """Scan processes"""
        auto_kill = '--kill' in args or '-k' in args
        try:
            result = self.optimizer.scan_processes(auto_kill=auto_kill)
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Get system information"""
        try:
            result = self.optimizer.get_system_info()
            return {
                'success': True,
                'output': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Get optimizer statistics"""
        try:
            result = self.optimizer.get_stats()
            return {
                'success': True,
                'output': result
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
                'output': {
                    'ram_threshold_mb': self.optimizer.config.ram_threshold_mb,
                    'cpu_threshold_percent': self.optimizer.config.cpu_threshold_percent,
                    'scan_interval': self.optimizer.config.scan_interval,
                    'enable_pagefile_clean': self.optimizer.config.enable_pagefile_clean,
                    'enable_pagefile_flush': self.optimizer.config.enable_pagefile_flush,  # v2
                    'enable_workingset_trim': self.optimizer.config.enable_workingset_trim,  # v2
                    'enable_system_cache_flush': self.optimizer.config.enable_system_cache_flush,  # v2
                    'enable_priority_opt': self.optimizer.config.enable_priority_opt,
                    'enable_auto_kill': self.optimizer.config.enable_auto_kill,
                    'enable_cache_flush': self.optimizer.config.enable_cache_flush,
                    'daemon_enabled': self.optimizer.config.daemon_enabled,
                }
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

            if hasattr(self.optimizer.config, key):
                setattr(self.optimizer.config, key, value)
                return {
                    'success': True,
                    'output': f'Configuration updated: {key} = {value}'
                }
            else:
                return {
                    'success': False,
                    'error': f'Unknown configuration key: {key}'
                }

        return {'success': False, 'error': 'Usage: sysopt config [key=value]'}

    async def cmd_daemon(self, *args) -> Dict[str, Any]:
        """Control daemon"""
        if not args:
            return {
                'success': True,
                'output': {
                    'running': self.optimizer.running,
                    'daemon_enabled': self.optimizer.config.daemon_enabled
                }
            }

        subcommand = args[0]

        if subcommand == 'start':
            if self.optimizer.running:
                return {'success': False, 'error': 'Daemon already running'}
            
            self.optimizer.config.daemon_enabled = True
            await self.optimizer.start_daemon()
            return {'success': True, 'output': 'Daemon started'}

        elif subcommand == 'stop':
            if not self.optimizer.running:
                return {'success': False, 'error': 'Daemon not running'}
            
            await self.optimizer.stop_daemon()
            self.optimizer.config.daemon_enabled = False
            return {'success': True, 'output': 'Daemon stopped'}

        elif subcommand == 'status':
            return {
                'success': True,
                'output': {
                    'running': self.optimizer.running,
                    'daemon_enabled': self.optimizer.config.daemon_enabled,
                    'scan_interval': self.optimizer.config.scan_interval
                }
            }

        else:
            return {'success': False, 'error': f'Unknown daemon subcommand: {subcommand}'}

    async def cmd_plugins(self, *args) -> Dict[str, Any]:
        """List plugins"""
        plugins = []
        for plugin in self.optimizer.plugins:
            plugins.append({
                'name': plugin.name,
                'type': type(plugin).__name__
            })

        return {
            'success': True,
            'output': {
                'plugins': plugins,
                'total': len(plugins)
            }
        }

    async def cmd_reset_stats(self, *args) -> Dict[str, Any]:
        """Reset statistics"""
        self.optimizer.reset_stats()
        return {
            'success': True,
            'output': 'Statistics reset'
        }
