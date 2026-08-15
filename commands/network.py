"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkCommands
  VERSION: 1.0.0
  MODULE CLASS: NetworkCommands
  DESCRIPTION:
       Network command handlers for network operations

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


class NetworkCommands:
    """Network command handlers"""
    
    def __init__(self, network_core, network_manager):
        self.core = network_core
        self.manager = network_manager
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a network command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown network command: {command}',
            }
            
    async def cmd_interfaces(self, *args) -> Dict[str, Any]:
        """List network interfaces"""
        interfaces = await self.core.get_interfaces()
        
        return {
            'success': True,
            'output': interfaces
        }
        
    async def cmd_ping(self, *args) -> Dict[str, Any]:
        """Ping a host"""
        if not args:
            return {'success': False, 'error': 'Usage: ping <host>'}
            
        result = await self.core.ping(args[0])
        
        return {
            'success': True,
            'output': result
        }
        
    async def cmd_resolve(self, *args) -> Dict[str, Any]:
        """Resolve hostname"""
        if not args:
            return {'success': False, 'error': 'Usage: resolve <hostname>'}
            
        ip = await self.core.resolve(args[0])
        
        return {
            'success': True,
            'output': ip if ip else 'Resolution failed'
        }
        
    async def cmd_connect(self, *args) -> Dict[str, Any]:
        """Connect to a host"""
        if len(args) < 3:
            return {'success': False, 'error': 'Usage: connect <id> <host> <port>'}
            
        connection_id = args[0]
        host = args[1]
        port = int(args[2])
        
        success = await self.manager.connect(connection_id, host, port)
        
        return {
            'success': success,
            'output': f'Connected to {host}:{port}' if success else 'Connection failed'
        }
        
    async def cmd_disconnect(self, *args) -> Dict[str, Any]:
        """Disconnect from a host"""
        if not args:
            return {'success': False, 'error': 'Usage: disconnect <connection_id>'}
            
        success = await self.manager.disconnect(args[0])
        
        return {
            'success': success,
            'output': 'Disconnected' if success else 'Disconnect failed'
        }
        
    async def cmd_connections(self, *args) -> Dict[str, Any]:
        """List active connections"""
        connections = await self.manager.list_connections()
        
        return {
            'success': True,
            'output': connections
        }
        
    async def cmd_scan_ports(self, *args) -> Dict[str, Any]:
        """Scan ports on a host"""
        if len(args) < 2:
            return {'success': False, 'error': 'Usage: scan_ports <host> <ports>'}
            
        host = args[0]
        ports = [int(p) for p in args[1].split(',')]
        
        results = await self.core.scan_ports(host, ports)
        
        return {
            'success': True,
            'output': results
        }
        
    async def cmd_wifi(self, *args) -> Dict[str, Any]:
        """WiFi commands"""
        if not args:
            return {'success': False, 'error': 'Usage: wifi <scan|connect|info|disconnect>'}
            
        subcommand = args[0]
        
        if subcommand == 'scan':
            return await self.cmd_wifi_scan(*args[1:])
        elif subcommand == 'connect':
            return await self.cmd_wifi_connect(*args[1:])
        elif subcommand == 'info':
            return await self.cmd_wifi_info(*args[1:])
        elif subcommand == 'disconnect':
            return await self.cmd_wifi_disconnect(*args[1:])
        else:
            return {'success': False, 'error': f'Unknown wifi subcommand: {subcommand}'}
            
    async def cmd_wifi_scan(self, *args) -> Dict[str, Any]:
        """Scan for WiFi networks"""
        try:
            # Use Windows netsh to scan for WiFi networks
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': f'WiFi scan failed: {result.stderr}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'WiFi scan error: {str(e)}'
            }
            
    async def cmd_wifi_connect(self, *args) -> Dict[str, Any]:
        """Connect to WiFi network"""
        if len(args) < 2:
            return {'success': False, 'error': 'Usage: wifi connect <ssid> <password>'}
            
        ssid = args[0]
        password = args[1]
        
        try:
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'connect', f'name={ssid}', 
                                  f'password={password}'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': f'Connected to {ssid}'
                }
            else:
                return {
                    'success': False,
                    'error': f'WiFi connection failed: {result.stderr}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'WiFi connection error: {str(e)}'
            }
            
    async def cmd_wifi_info(self, *args) -> Dict[str, Any]:
        """Show WiFi connection info"""
        try:
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': f'WiFi info failed: {result.stderr}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'WiFi info error: {str(e)}'
            }
            
    async def cmd_wifi_disconnect(self, *args) -> Dict[str, Any]:
        """Disconnect from WiFi"""
        try:
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'disconnect'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': 'Disconnected from WiFi'
                }
            else:
                return {
                    'success': False,
                    'error': f'WiFi disconnect failed: {result.stderr}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'WiFi disconnect error: {str(e)}'
            }
            
    async def cmd_wlan(self, *args) -> Dict[str, Any]:
        """WLAN commands (alias for wifi)"""
        return await self.cmd_wifi(*args)
        
    async def cmd_lan(self, *args) -> Dict[str, Any]:
        """LAN information"""
        try:
            import subprocess
            result = subprocess.run(['ipconfig', '/all'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': f'LAN info failed: {result.stderr}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'LAN info error: {str(e)}'
            }
            
    async def cmd_ethernet(self, *args) -> Dict[str, Any]:
        """Ethernet information (alias for lan)"""
        return await self.cmd_lan(*args)
