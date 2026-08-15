"""
 ============================================================
  MODULE/PLUGIN NAME: GeoCommands
  VERSION: 4.0.0
  MODULE CLASS: GeoCommands
  DESCRIPTION:
       Geolocation command handlers with GPS daemon, map engine, and fusion engine support

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


class GeoCommands:
    """Geolocation command handlers"""

    def __init__(self, geo_engine):
        self.geo = geo_engine

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a geo command"""
        # If no command provided, treat first arg as query for locate
        if not command and args:
            return await self.cmd_locate(args[0], *args[1:])
        
        # If no command and no args, show help
        if not command:
            return {
                'success': False,
                'error': 'Usage: geo <command> [args...]. Available commands: locate, ip, reverse, batch, providers, stats, cache, plugins, config, gps, map, fusion'
            }
        
        # Try exact match first
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        
        # Try case-insensitive match
        handler = getattr(self, f'cmd_{command.lower()}', None)
        if handler:
            return await handler(*args)
        
        # If command looks like an IP address, treat it as a query
        import re
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if re.match(ip_pattern, command):
            return await self.cmd_locate(command, *args)
        
        return {
            'success': False,
            'error': f'Unknown geo command: {command}. Available: locate, ip, reverse, batch, providers, stats, cache, plugins, config, gps, map, fusion',
        }

    async def cmd_locate(self, *args) -> Dict[str, Any]:
        """Locate an IP address or location"""
        if not args:
            return {'success': False, 'error': 'Usage: geo locate <query>'}

        query = args[0]
        provider = args[1] if len(args) > 1 else None

        try:
            result = await self.geo.locate(query, provider)

            return {
                'success': True,
                'output': {
                    'query': query,
                    'location': result.to_dict(),
                    'formatted': str(result)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_ip(self, *args) -> Dict[str, Any]:
        """Locate an IP address (alias for locate)"""
        return await self.cmd_locate(*args)
    
    async def cmd_IP(self, *args) -> Dict[str, Any]:
        """Locate an IP address (uppercase alias)"""
        return await self.cmd_locate(*args)

    async def cmd_reverse(self, *args) -> Dict[str, Any]:
        """Reverse geocode coordinates"""
        if len(args) < 2:
            return {'success': False, 'error': 'Usage: geo reverse <lat> <lon>'}

        try:
            lat = float(args[0])
            lon = float(args[1])

            result = await self.geo.reverse_geocode(lat, lon)

            return {
                'success': True,
                'output': {
                    'coordinates': {'lat': lat, 'lon': lon},
                    'location': result.to_dict(),
                    'formatted': str(result)
                }
            }
        except ValueError:
            return {'success': False, 'error': 'Invalid coordinates'}
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_batch(self, *args) -> Dict[str, Any]:
        """Locate multiple queries in parallel"""
        if not args:
            return {'success': False, 'error': 'Usage: geo batch <query1> <query2> ...'}

        queries = list(args)

        try:
            results = await self.geo.batch_locate(queries)

            return {
                'success': True,
                'output': {
                    'queries': queries,
                    'results': {k: v.to_dict() if v else None for k, v in results.items()}
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def cmd_providers(self, *args) -> Dict[str, Any]:
        """List available providers"""
        providers = []
        for name, provider in self.geo.providers.items():
            providers.append({
                'name': name,
                'priority': provider.priority,
                'available': await provider.is_available()
            })

        return {
            'success': True,
            'output': {
                'providers': providers,
                'default': self.geo.config.get('default_provider')
            }
        }

    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Show geo engine statistics"""
        stats = self.geo.get_stats()

        return {
            'success': True,
            'output': stats
        }

    async def cmd_cache(self, *args) -> Dict[str, Any]:
        """Cache commands"""
        if not args:
            return {'success': False, 'error': 'Usage: geo cache <clear|size|info>'}

        subcommand = args[0]

        if subcommand == 'clear':
            for plugin in self.geo.plugins:
                if plugin.name == 'cache':
                    plugin.clear_cache()
                    return {'success': True, 'output': 'Cache cleared'}
            return {'success': False, 'error': 'Cache plugin not found'}

        elif subcommand == 'size':
            for plugin in self.geo.plugins:
                if plugin.name == 'cache':
                    size = plugin.get_cache_size()
                    return {'success': True, 'output': f'Cache size: {size} entries'}
            return {'success': False, 'error': 'Cache plugin not found'}

        elif subcommand == 'info':
            for plugin in self.geo.plugins:
                if plugin.name == 'cache':
                    return {'success': True, 'output': f'Cache plugin active, TTL: {plugin.ttl}s'}
            return {'success': False, 'error': 'Cache plugin not found'}

        else:
            return {'success': False, 'error': f'Unknown cache subcommand: {subcommand}'}

    async def cmd_plugins(self, *args) -> Dict[str, Any]:
        """List active plugins"""
        plugins = []
        for plugin in self.geo.plugins:
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

    async def cmd_config(self, *args) -> Dict[str, Any]:
        """Show or update configuration"""
        if not args:
            return {
                'success': True,
                'output': self.geo.config
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

            self.geo.configure(**{key: value})
            return {
                'success': True,
                'output': f'Configuration updated: {key} = {value}'
            }

        return {'success': False, 'error': 'Usage: geo config [key=value]'}
    
    # ============================================================
    # GPS DAEMON COMMANDS
    # ============================================================
    
    async def cmd_gps(self, *args) -> Dict[str, Any]:
        """GPS daemon commands"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: geo gps <status|start|stop|enable|disable>'
            }
        
        subcommand = args[0]
        
        if subcommand == 'status':
            status = self.geo.get_gps_status()
            if status.get('success'):
                return {
                    'success': True,
                    'output': f"GPS Status: {status.get('message', 'No status')}"
                }
            return status
        
        elif subcommand == 'start':
            started = await self.geo.start_gps()
            if started:
                return {
                    'success': True,
                    'output': 'GPS daemon started'
                }
            return {
                'success': False,
                'error': 'Failed to start GPS daemon (not enabled)'
            }
        
        elif subcommand == 'stop':
            stopped = self.geo.stop_gps()
            if stopped:
                return {
                    'success': True,
                    'output': 'GPS daemon stopped'
                }
            return {
                'success': False,
                'error': 'Failed to stop GPS daemon (not running)'
            }
        
        elif subcommand == 'enable':
            self.geo.enable_gps()
            return {
                'success': True,
                'output': 'GPS daemon enabled with mock provider'
            }
        
        elif subcommand == 'disable':
            self.geo.disable_gps()
            return {
                'success': True,
                'output': 'GPS daemon disabled'
            }
        
        else:
            return {
                'success': False,
                'error': f'Unknown GPS subcommand: {subcommand}. Available: status, start, stop, enable, disable'
            }
    
    # ============================================================
    # MAP ENGINE COMMANDS
    # ============================================================
    
    async def cmd_map(self, *args) -> Dict[str, Any]:
        """Map engine commands"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: geo map <status|enable|disable|render>'
            }
        
        subcommand = args[0]
        
        if subcommand == 'status':
            status = self.geo.get_map_status()
            if status.get('success'):
                return {
                    'success': True,
                    'output': f"Map Status: enabled={status.get('enabled')}, points={status.get('points')}, paths={status.get('paths')}, heat={status.get('heat')}"
                }
            return status
        
        elif subcommand == 'enable':
            renderer = args[1] if len(args) > 1 else 'osm'
            api_key = args[2] if len(args) > 2 else None
            enabled = self.geo.enable_map(renderer, api_key)
            if enabled:
                return {
                    'success': True,
                    'output': f'Map engine enabled with {renderer} renderer'
                }
            return {
                'success': False,
                'error': 'Failed to enable map engine'
            }
        
        elif subcommand == 'disable':
            disabled = self.geo.disable_map()
            if disabled:
                return {
                    'success': True,
                    'output': 'Map engine disabled'
                }
            return {
                'success': False,
                'error': 'Failed to disable map engine'
            }
        
        elif subcommand == 'render':
            if not self.geo.map_engine:
                return {
                    'success': False,
                    'error': 'Map engine not enabled'
                }
            
            try:
                lat = float(args[1]) if len(args) > 1 else 52.0
                lon = float(args[2]) if len(args) > 2 else 21.0
                zoom = int(args[3]) if len(args) > 3 else 15
                size = int(args[4]) if len(args) > 4 else 512
                
                result = await self.geo.map_engine.render(lat, lon, zoom, size)
                return {
                    'success': True,
                    'output': f'Map rendered at {lat}, {lon} (zoom={zoom}, size={size})'
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to render map: {e}'
                }
        
        else:
            return {
                'success': False,
                'error': 'Usage: geo map <status|enable|disable|render>'
            }
    
    # ============================================================
    # FUSION ENGINE COMMANDS
    # ============================================================
    
    async def cmd_fusion(self, *args) -> Dict[str, Any]:
        """Fusion engine commands"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: geo fusion <status|enable|disable>'
            }
        
        subcommand = args[0]
        
        if subcommand == 'status':
            status = self.geo.get_fusion_status()
            if status.get('success'):
                return {
                    'success': True,
                    'output': f"Fusion Status: enabled={status.get('enabled')}, plugins={status.get('plugins')}, weights={status.get('weights')}"
                }
            return status
        
        elif subcommand == 'enable':
            enabled = self.geo.enable_fusion()
            if enabled:
                return {
                    'success': True,
                    'output': 'Fusion engine enabled'
                }
            return {
                'success': False,
                'error': 'Failed to enable fusion engine'
            }
        
        elif subcommand == 'disable':
            disabled = self.geo.disable_fusion()
            if disabled:
                return {
                    'success': True,
                    'output': 'Fusion engine disabled'
                }
            return {
                'success': False,
                'error': 'Failed to disable fusion engine'
            }
        
        else:
            return {
                'success': False,
                'error': 'Usage: geo fusion <status|enable|disable>'
            }
