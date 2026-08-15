"""
 ============================================================
  MODULE/PLUGIN NAME: GUIApps
  VERSION: 1.0.0
  MODULE CLASS: GUIApps
  DESCRIPTION:
       Application templates and presets for TerminalX GUI

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

from typing import Dict, Any, List, Optional


class GUIApps:
    """GUI application templates"""
    
    def __init__(self):
        self.apps: Dict[str, Dict] = {}
        self._register_default_apps()
        
    def _register_default_apps(self):
        """Register default app templates"""
        self.apps = {
            'dashboard': {
                'name': 'Dashboard',
                'description': 'Main dashboard with widgets',
                'windows': [
                    {
                        'id': 'main',
                        'title': 'Dashboard',
                        'width': 1200,
                        'height': 800,
                        'widgets': [
                            {'type': 'label', 'text': 'System Status'},
                            {'type': 'progress', 'id': 'cpu_usage'},
                            {'type': 'progress', 'id': 'memory_usage'},
                        ],
                    },
                ],
            },
            'terminal': {
                'name': 'Terminal',
                'description': 'Terminal emulator',
                'windows': [
                    {
                        'id': 'terminal',
                        'title': 'Terminal',
                        'width': 800,
                        'height': 600,
                        'widgets': [
                            {'type': 'textarea', 'id': 'output', 'rows': 20},
                            {'type': 'input', 'id': 'input', 'placeholder': 'Enter command'},
                        ],
                    },
                ],
            },
            'settings': {
                'name': 'Settings',
                'description': 'Settings editor',
                'windows': [
                    {
                        'id': 'settings',
                        'title': 'Settings',
                        'width': 600,
                        'height': 400,
                        'widgets': [
                            {'type': 'label', 'text': 'General Settings'},
                            {'type': 'checkbox', 'id': 'dark_mode', 'label': 'Dark Mode'},
                            {'type': 'select', 'id': 'language', 'options': ['en', 'pl', 'de']},
                        ],
                    },
                ],
            },
        }
        
    async def register(self, app_id: str, config: Dict[str, Any]):
        """Register an app template"""
        self.apps[app_id] = {
            'id': app_id,
            'name': config.get('name', app_id),
            'description': config.get('description', ''),
            'windows': config.get('windows', []),
            'config': config.get('config', {}),
        }
        
    async def get_app(self, app_id: str) -> Optional[Dict]:
        """Get app template"""
        return self.apps.get(app_id)
        
    async def list_apps(self) -> List[Dict]:
        """List all apps"""
        return list(self.apps.values())
        
    async def launch(self, app_id: str, gui_engine) -> bool:
        """Launch an app"""
        app = await self.get_app(app_id)
        if not app:
            return False
            
        for window_config in app['windows']:
            await gui_engine.create_window(
                window_id=window_config['id'],
                title=window_config['title'],
                width=window_config.get('width', 800),
                height=window_config.get('height', 600),
            )
            
            for widget in window_config.get('widgets', []):
                widget_id = widget.get('id', f"widget_{len(widget)}")
                await gui_engine.add_widget(
                    window_id=window_config['id'],
                    widget_id=widget_id,
                    widget_type=widget['type'],
                    **{k: v for k, v in widget.items() if k not in ['id', 'type']}
                )
                
            await gui_engine.show_window(window_config['id'])
            
        return True
