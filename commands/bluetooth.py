"""
 ============================================================
  MODULE/PLUGIN NAME: BluetoothCommands
  VERSION: 1.0.0
  MODULE CLASS: BluetoothCommands
  DESCRIPTION:
       Bluetooth command handlers for device management

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


class BluetoothCommands:
    """Bluetooth command handlers"""

    def __init__(self, bluetooth_manager, bluetooth_scanner):
        self.manager = bluetooth_manager
        self.scanner = bluetooth_scanner

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a bluetooth command"""
        handler = getattr(self, f'cmd_{command}', None)

        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown bluetooth command: {command}',
            }

    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Get Bluetooth status"""
        try:
            status = await self.manager.get_status()
            return {
                'success': True,
                'output': status
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_power_on(self, *args) -> Dict[str, Any]:
        """Power on Bluetooth"""
        try:
            result = await self.manager.power_on()
            if result:
                return {
                    'success': True,
                    'output': 'Bluetooth powered on'
                }
            return {
                'success': False,
                'error': 'Failed to power on Bluetooth'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_power_off(self, *args) -> Dict[str, Any]:
        """Power off Bluetooth"""
        try:
            result = await self.manager.power_off()
            if result:
                return {
                    'success': True,
                    'output': 'Bluetooth powered off'
                }
            return {
                'success': False,
                'error': 'Failed to power off Bluetooth'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_discoverable(self, *args) -> Dict[str, Any]:
        """Set discoverable mode"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth discoverable <on|off>'}

        mode = args[0].lower()
        if mode not in ['on', 'off', 'true', 'false']:
            return {'success': False, 'error': 'Usage: bluetooth discoverable <on|off>'}

        discoverable = mode in ['on', 'true']
        try:
            result = await self.manager.set_discoverable(discoverable)
            if result:
                return {
                    'success': True,
                    'output': f'Discoverable mode set to {mode}'
                }
            return {
                'success': False,
                'error': 'Failed to set discoverable mode'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_scan(self, *args) -> Dict[str, Any]:
        """Scan for Bluetooth devices"""
        duration = 10.0
        if args:
            try:
                duration = float(args[0])
            except ValueError:
                return {'success': False, 'error': 'Duration must be a number'}

        try:
            results = await self.scanner.scan(duration=duration)
            return {
                'success': True,
                'output': {
                    'devices': results,
                    'count': len(results)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_pair(self, *args) -> Dict[str, Any]:
        """Pair with a device"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth pair <address> [pin]'}

        address = args[0]
        pin = args[1] if len(args) > 1 else None

        try:
            result = await self.manager.pair(address, pin)
            if result:
                return {
                    'success': True,
                    'output': f'Paired with {address}'
                }
            return {
                'success': False,
                'error': 'Failed to pair with device'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_unpair(self, *args) -> Dict[str, Any]:
        """Unpair a device"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth unpair <address>'}

        address = args[0]

        try:
            result = await self.manager.unpair(address)
            if result:
                return {
                    'success': True,
                    'output': f'Unpaired {address}'
                }
            return {
                'success': False,
                'error': 'Failed to unpair device'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_connect(self, *args) -> Dict[str, Any]:
        """Connect to a device"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth connect <address>'}

        address = args[0]

        try:
            result = await self.manager.connect(address)
            if result:
                return {
                    'success': True,
                    'output': f'Connected to {address}'
                }
            return {
                'success': False,
                'error': 'Failed to connect to device'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_disconnect(self, *args) -> Dict[str, Any]:
        """Disconnect from a device"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth disconnect <address>'}

        address = args[0]

        try:
            result = await self.manager.disconnect(address)
            if result:
                return {
                    'success': True,
                    'output': f'Disconnected from {address}'
                }
            return {
                'success': False,
                'error': 'Failed to disconnect from device'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_paired(self, *args) -> Dict[str, Any]:
        """List paired devices"""
        try:
            devices = await self.manager.get_paired_devices()
            return {
                'success': True,
                'output': {
                    'devices': devices,
                    'count': len(devices)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_connected(self, *args) -> Dict[str, Any]:
        """List connected devices"""
        try:
            devices = await self.manager.get_connected_devices()
            return {
                'success': True,
                'output': {
                    'devices': devices,
                    'count': len(devices)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_results(self, *args) -> Dict[str, Any]:
        """Get scan results"""
        try:
            results = await self.scanner.get_results()
            return {
                'success': True,
                'output': {
                    'devices': results,
                    'count': len(results)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_sort_rssi(self, *args) -> Dict[str, Any]:
        """Sort scan results by signal strength"""
        try:
            results = await self.scanner.sort_by_rssi()
            return {
                'success': True,
                'output': {
                    'devices': results,
                    'count': len(results)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_filter_paired(self, *args) -> Dict[str, Any]:
        """Filter scan results by paired status"""
        if not args:
            return {'success': False, 'error': 'Usage: bluetooth filter_paired <true|false>'}

        paired = args[0].lower() in ['true', 'on', 'yes', '1']

        try:
            results = await self.scanner.filter_by_paired(paired)
            return {
                'success': True,
                'output': {
                    'devices': results,
                    'count': len(results)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
