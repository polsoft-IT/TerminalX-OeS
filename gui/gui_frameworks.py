"""
 ============================================================
  MODULE/PLUGIN NAME: GUIFrameworks
  VERSION: 1.0.0
  MODULE CLASS: GUIFrameworks
  DESCRIPTION:
       GUI framework adapters for TerminalX GUI operations

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


class GUIFrameworks:
    """GUI framework manager"""
    
    def __init__(self):
        self.frameworks: Dict[str, Dict] = {}
        self.active_framework: Optional[str] = None
        
    async def register(self, name: str, config: Dict[str, Any]):
        """Register a GUI framework"""
        self.frameworks[name] = {
            'name': name,
            'type': config.get('type', 'terminal'),
            'library': config.get('library'),
            'version': config.get('version'),
            'enabled': config.get('enabled', True),
            'config': config.get('config', {}),
        }
        
    async def activate(self, name: str) -> bool:
        """Activate a framework"""
        if name in self.frameworks and self.frameworks[name]['enabled']:
            self.active_framework = name
            return True
        return False
        
    async def get_active(self) -> Optional[Dict]:
        """Get active framework"""
        if self.active_framework:
            return self.frameworks.get(self.active_framework)
        return None
        
    async def list_frameworks(self) -> List[Dict]:
        """List all frameworks"""
        return list(self.frameworks.values())
        
    async def get_framework(self, name: str) -> Optional[Dict]:
        """Get specific framework"""
        return self.frameworks.get(name)
        
    async def check_availability(self, name: str) -> bool:
        """Check if framework is available"""
        framework = self.frameworks.get(name)
        if not framework:
            return False
            
        library = framework.get('library')
        if not library:
            return True
            
        try:
            __import__(library)
            return True
        except ImportError:
            return False
