"""
 ============================================================
  MODULE/PLUGIN NAME: AIPlugins
  VERSION: 1.0.0
  MODULE CLASS: AIPlugins
  DESCRIPTION:
       Plugin system for AI extensions and custom AI modules

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

import importlib
import importlib.util
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class PluginStatus(Enum):
    """Plugin status"""
    LOADED = "loaded"
    UNLOADED = "unloaded"
    ERROR = "error"
    DISABLED = "disabled"


class AIPlugins:
    """AI plugin manager"""
    
    def __init__(self):
        self.plugins: Dict[str, Dict] = {}
        self.plugin_dir: Optional[str] = None
        self.hooks: Dict[str, List[str]] = {}
        self.notification_callback = None
        self.plugin_stats = {
            'total_loaded': 0,
            'total_errors': 0,
            'hooks_executed': 0,
        }
        
    async def initialize(self, plugin_dir: str = None):
        """Initialize plugin manager"""
        self.plugin_dir = plugin_dir or os.path.join(
            os.path.dirname(__file__), '..', 'plugins', 'ai'
        )
        
        # Create plugin directory if it doesn't exist
        os.makedirs(self.plugin_dir, exist_ok=True)
        
    def set_notification_callback(self, callback):
        """Set callback for plugin notifications"""
        self.notification_callback = callback
        
    async def load(self, name: str) -> Dict[str, Any]:
        """Load a plugin"""
        try:
            module_path = os.path.join(self.plugin_dir, f'{name}.py')
            
            if not os.path.exists(module_path):
                return {
                    'success': False,
                    'error': f'Plugin file not found: {module_path}'
                }
                
            spec = importlib.util.spec_from_file_location(name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin class
            plugin_class = getattr(module, 'Plugin', None)
            if not plugin_class:
                return {
                    'success': False,
                    'error': 'Plugin class not found'
                }
                
            # Initialize plugin
            plugin = plugin_class()
            await plugin.initialize()
            
            # Store plugin info
            self.plugins[name] = {
                'instance': plugin,
                'name': name,
                'version': getattr(plugin, 'version', '1.0.0'),
                'description': getattr(plugin, 'description', ''),
                'author': getattr(plugin, 'author', 'Unknown'),
                'status': PluginStatus.LOADED.value,
                'loaded_at': datetime.now().isoformat(),
            }
            
            # Register hooks
            if hasattr(plugin, 'hooks'):
                for hook in plugin.hooks:
                    if hook not in self.hooks:
                        self.hooks[hook] = []
                    self.hooks[hook].append(name)
            
            self.plugin_stats['total_loaded'] += 1
            
            # Send notification
            if self.notification_callback:
                await self.notification_callback(
                    f"Plugin loaded: {name}",
                    f"Version: {self.plugins[name]['version']}",
                    'system',
                    'low'
                )
            
            return {
                'success': True,
                'plugin': self.plugins[name]
            }
            
        except Exception as e:
            self.plugin_stats['total_errors'] += 1
            return {
                'success': False,
                'error': str(e)
            }
            
    async def unload(self, name: str) -> Dict[str, Any]:
        """Unload a plugin"""
        if name not in self.plugins:
            return {
                'success': False,
                'error': 'Plugin not found'
            }
            
        try:
            plugin_info = self.plugins[name]
            plugin = plugin_info['instance']
            
            if hasattr(plugin, 'shutdown'):
                await plugin.shutdown()
            
            # Remove from hooks
            for hook, plugins in self.hooks.items():
                if name in plugins:
                    plugins.remove(name)
                    
            del self.plugins[name]
            self.plugin_stats['total_loaded'] -= 1
            
            return {
                'success': True,
                'message': f'Plugin {name} unloaded'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
    async def reload(self, name: str) -> Dict[str, Any]:
        """Reload a plugin"""
        unload_result = await self.unload(name)
        if not unload_result['success']:
            return unload_result
        return await self.load(name)
        
    async def get_plugin(self, name: str) -> Optional[Dict]:
        """Get a plugin"""
        return self.plugins.get(name)
        
    async def list_plugins(self) -> List[Dict]:
        """List loaded plugins"""
        return [
            {
                'name': info['name'],
                'version': info['version'],
                'description': info['description'],
                'author': info['author'],
                'status': info['status'],
                'loaded_at': info['loaded_at'],
            }
            for info in self.plugins.values()
        ]
        
    async def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute hook on all plugins"""
        results = []
        self.plugin_stats['hooks_executed'] += 1
        
        if hook_name not in self.hooks:
            return results
            
        for plugin_name in self.hooks[hook_name]:
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]['instance']
                if hasattr(plugin, hook_name):
                    try:
                        method = getattr(plugin, hook_name)
                        if asyncio.iscoroutinefunction(method):
                            result = await method(*args, **kwargs)
                        else:
                            result = method(*args, **kwargs)
                        results.append({
                            'plugin': plugin_name,
                            'result': result,
                        })
                    except Exception as e:
                        results.append({
                            'plugin': plugin_name,
                            'error': str(e),
                        })
                        
        return results
        
    async def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directory"""
        if not self.plugin_dir or not os.path.exists(self.plugin_dir):
            return []
            
        plugins = []
        for file in os.listdir(self.plugin_dir):
            if file.endswith('.py') and not file.startswith('_'):
                plugins.append(file[:-3])  # Remove .py extension
                
        return plugins
        
    async def load_all(self) -> Dict[str, Any]:
        """Load all available plugins"""
        available = await self.discover_plugins()
        results = {
            'success': [],
            'failed': [],
        }
        
        for plugin_name in available:
            result = await self.load(plugin_name)
            if result['success']:
                results['success'].append(plugin_name)
            else:
                results['failed'].append({
                    'name': plugin_name,
                    'error': result.get('error', 'Unknown error')
                })
                
        return results
        
    async def get_hooks(self) -> Dict[str, List[str]]:
        """Get all registered hooks"""
        return self.hooks.copy()
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get plugin statistics"""
        return {
            'total_loaded': self.plugin_stats['total_loaded'],
            'total_errors': self.plugin_stats['total_errors'],
            'hooks_executed': self.plugin_stats['hooks_executed'],
            'available_plugins': len(await self.discover_plugins()),
            'registered_hooks': len(self.hooks),
        }
