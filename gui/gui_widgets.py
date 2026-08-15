"""
 ============================================================
  MODULE/PLUGIN NAME: GUIWidgets
  VERSION: 1.0.0
  MODULE CLASS: GUIWidgets
  DESCRIPTION:
       Widget definitions and factories for TerminalX GUI

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


class GUIWidgets:
    """Widget factory and manager"""
    
    def __init__(self):
        self.widget_types: Dict[str, Dict] = {}
        self._register_default_widgets()
        
    def _register_default_widgets(self):
        """Register default widget types"""
        self.widget_types = {
            'label': {
                'properties': ['text', 'color', 'bold'],
                'events': ['click'],
            },
            'button': {
                'properties': ['text', 'color', 'disabled'],
                'events': ['click'],
            },
            'input': {
                'properties': ['placeholder', 'value', 'type'],
                'events': ['change', 'focus', 'blur'],
            },
            'textarea': {
                'properties': ['placeholder', 'value', 'rows'],
                'events': ['change', 'focus', 'blur'],
            },
            'checkbox': {
                'properties': ['checked', 'label'],
                'events': ['change'],
            },
            'select': {
                'properties': ['options', 'selected', 'multiple'],
                'events': ['change'],
            },
            'progress': {
                'properties': ['value', 'total', 'color'],
                'events': ['complete'],
            },
            'list': {
                'properties': ['items', 'selected'],
                'events': ['select'],
            },
            'table': {
                'properties': ['headers', 'rows', 'sortable'],
                'events': ['sort', 'select'],
            },
            'image': {
                'properties': ['src', 'alt', 'width', 'height'],
                'events': ['load', 'error'],
            },
        }
        
    async def create(self, widget_type: str, widget_id: str, **kwargs) -> Optional[Dict]:
        """Create a widget"""
        if widget_type not in self.widget_types:
            return None
            
        widget_def = self.widget_types[widget_type]
        
        widget = {
            'id': widget_id,
            'type': widget_type,
            'properties': {},
            'events': {},
        }
        
        # Set properties
        for prop in widget_def['properties']:
            if prop in kwargs:
                widget['properties'][prop] = kwargs[prop]
                
        # Set event handlers
        for event in widget_def['events']:
            if event in kwargs:
                widget['events'][event] = kwargs[event]
                
        return widget
        
    async def validate(self, widget: Dict) -> bool:
        """Validate widget configuration"""
        widget_type = widget.get('type')
        
        if widget_type not in self.widget_types:
            return False
            
        widget_def = self.widget_types[widget_type]
        
        # Check required properties
        if 'id' not in widget:
            return False
            
        return True
        
    async def get_widget_types(self) -> List[str]:
        """Get available widget types"""
        return list(self.widget_types.keys())
        
    async def get_widget_definition(self, widget_type: str) -> Optional[Dict]:
        """Get widget type definition"""
        return self.widget_types.get(widget_type)
