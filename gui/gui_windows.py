"""
 ============================================================
  MODULE/PLUGIN NAME: GUIWindows
  VERSION: 1.0.0
  MODULE CLASS: GUIWindows
  DESCRIPTION:
       Window management for TerminalX GUI operations

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


class GUIWindows:
    """Window manager"""
    
    def __init__(self):
        self.windows: Dict[str, Dict] = {}
        self.active_window: Optional[str] = None
        self.z_order: List[str] = []
        
    async def create(self, window_id: str, title: str, 
                    width: int = 800, height: int = 600,
                    x: int = 0, y: int = 0) -> Dict:
        """Create a window"""
        window = {
            'id': window_id,
            'title': title,
            'width': width,
            'height': height,
            'x': x,
            'y': y,
            'visible': False,
            'minimized': False,
            'maximized': False,
            'resizable': True,
            'closable': True,
            'widgets': [],
            'layout': 'vertical',
        }
        
        self.windows[window_id] = window
        self.z_order.append(window_id)
        
        return window
        
    async def show(self, window_id: str) -> bool:
        """Show a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['visible'] = True
        self.windows[window_id]['minimized'] = False
        
        # Bring to front
        if window_id in self.z_order:
            self.z_order.remove(window_id)
        self.z_order.append(window_id)
        
        self.active_window = window_id
        return True
        
    async def hide(self, window_id: str) -> bool:
        """Hide a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['visible'] = False
        
        if self.active_window == window_id:
            self.active_window = None
            
        return True
        
    async def close(self, window_id: str) -> bool:
        """Close a window"""
        if window_id not in self.windows:
            return False
            
        if not self.windows[window_id]['closable']:
            return False
            
        del self.windows[window_id]
        
        if window_id in self.z_order:
            self.z_order.remove(window_id)
            
        if self.active_window == window_id:
            self.active_window = self.z_order[-1] if self.z_order else None
            
        return True
        
    async def minimize(self, window_id: str) -> bool:
        """Minimize a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['minimized'] = True
        return True
        
    async def maximize(self, window_id: str) -> bool:
        """Maximize a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['maximized'] = True
        return True
        
    async def restore(self, window_id: str) -> bool:
        """Restore a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['minimized'] = False
        self.windows[window_id]['maximized'] = False
        return True
        
    async def move(self, window_id: str, x: int, y: int) -> bool:
        """Move a window"""
        if window_id not in self.windows:
            return False
            
        self.windows[window_id]['x'] = x
        self.windows[window_id]['y'] = y
        return True
        
    async def resize(self, window_id: str, width: int, height: int) -> bool:
        """Resize a window"""
        if window_id not in self.windows:
            return False
            
        if not self.windows[window_id]['resizable']:
            return False
            
        self.windows[window_id]['width'] = width
        self.windows[window_id]['height'] = height
        return True
        
    async def focus(self, window_id: str) -> bool:
        """Focus a window"""
        if window_id not in self.windows:
            return False
            
        if window_id in self.z_order:
            self.z_order.remove(window_id)
        self.z_order.append(window_id)
        
        self.active_window = window_id
        return True
        
    async def get_active(self) -> Optional[Dict]:
        """Get active window"""
        if self.active_window:
            return self.windows.get(self.active_window)
        return None
        
    async def get_window(self, window_id: str) -> Optional[Dict]:
        """Get window by ID"""
        return self.windows.get(window_id)
        
    async def list_windows(self) -> List[Dict]:
        """List all windows in z-order"""
        return [
            self.windows[wid] 
            for wid in self.z_order 
            if wid in self.windows
        ]
