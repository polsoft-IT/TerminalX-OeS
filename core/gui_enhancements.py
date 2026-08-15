"""
GUI Engine GODMODE — Enhanced GUI with framebuffer and window management
"""

import time
import threading
import asyncio
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum


class WidgetType(Enum):
    """Widget types"""
    LABEL = "label"
    BUTTON = "button"
    TEXTBOX = "textbox"
    PROGRESS = "progress"
    LIST = "list"


class Framebuffer:
    """Framebuffer for GUI rendering"""
    
    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.buffer = [[" "] * width for _ in range(height)]
        self.cursor_x = 0
        self.cursor_y = 0
        
    def clear(self):
        """Clear the framebuffer"""
        for y in range(self.h):
            for x in range(self.w):
                self.buffer[y][x] = " "
                
    def draw_text(self, x: int, y: int, text: str):
        """Draw text at position"""
        for i, ch in enumerate(text):
            if 0 <= x + i < self.w and 0 <= y < self.h:
                self.buffer[y][x + i] = ch
                
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, char: str = "-"):
        """Draw a line"""
        if x1 == x2:  # Vertical
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= y < self.h and 0 <= x1 < self.w:
                    self.buffer[y][x1] = char
        elif y1 == y2:  # Horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= y1 < self.h and 0 <= x < self.w:
                    self.buffer[y1][x] = char
                    
    def draw_box(self, x: int, y: int, w: int, h: int, char: str = "#"):
        """Draw a box"""
        self.draw_line(x, y, x + w - 1, y, char)
        self.draw_line(x, y + h - 1, x + w - 1, y + h - 1, char)
        self.draw_line(x, y, x, y + h - 1, char)
        self.draw_line(x + w - 1, y, x + w - 1, y + h - 1, char)
        
    def render(self):
        """Render the framebuffer to console"""
        print("\033[H", end="")  # Move cursor to top
        for row in self.buffer:
            print("".join(row))
            
    def get_buffer(self) -> List[List[str]]:
        """Get the current buffer"""
        return [row.copy() for row in self.buffer]


class Widget:
    """Base widget class"""
    
    def __init__(self, x: int, y: int, widget_type: WidgetType):
        self.x = x
        self.y = y
        self.widget_type = widget_type
        self.visible = True
        self.enabled = True
        
    def draw(self, fb: Framebuffer, wx: int, wy: int):
        """Draw widget on framebuffer"""
        pass
        
    def handle_event(self, event: Dict[str, Any]) -> bool:
        """Handle widget event"""
        return False


class Label(Widget):
    """Label widget"""
    
    def __init__(self, x: int, y: int, text: str):
        super().__init__(x, y, WidgetType.LABEL)
        self.text = text
        
    def draw(self, fb: Framebuffer, wx: int, wy: int):
        if self.visible:
            fb.draw_text(wx + self.x, wy + self.y, self.text)
            
    def set_text(self, text: str):
        """Set label text"""
        self.text = text


class Button(Widget):
    """Button widget"""
    
    def __init__(self, x: int, y: int, text: str, callback: Callable = None):
        super().__init__(x, y, WidgetType.BUTTON)
        self.text = text
        self.callback = callback
        self.pressed = False
        
    def draw(self, fb: Framebuffer, wx: int, wy: int):
        if self.visible:
            prefix = "[" if not self.pressed else "<"
            suffix = "]" if not self.pressed else ">"
            fb.draw_text(wx + self.x, wy + self.y, f"{prefix}{self.text}{suffix}")
            
    def click(self):
        """Handle button click"""
        if self.enabled and self.callback:
            self.callback()
            
    def handle_event(self, event: Dict[str, Any]) -> bool:
        if event.get('type') == 'click':
            self.click()
            return True
        return False


class TextBox(Widget):
    """Text box widget"""
    
    def __init__(self, x: int, y: int, width: int, text: str = ""):
        super().__init__(x, y, WidgetType.TEXTBOX)
        self.width = width
        self.text = text
        self.cursor = len(text)
        
    def draw(self, fb: Framebuffer, wx: int, wy: int):
        if self.visible:
            display_text = self.text[:self.width]
            fb.draw_text(wx + self.x, wy + self.y, display_text.ljust(self.width))
            
    def set_text(self, text: str):
        """Set text box content"""
        self.text = text
        self.cursor = len(text)
        
    def append(self, char: str):
        """Append character"""
        if len(self.text) < self.width:
            self.text += char
            self.cursor += 1
            
    def backspace(self):
        """Remove last character"""
        if self.text:
            self.text = self.text[:-1]
            self.cursor -= 1


class ProgressBar(Widget):
    """Progress bar widget"""
    
    def __init__(self, x: int, y: int, width: int, value: float = 0.0):
        super().__init__(x, y, WidgetType.PROGRESS)
        self.width = width
        self.value = value  # 0.0 to 1.0
        
    def draw(self, fb: Framebuffer, wx: int, wy: int):
        if self.visible:
            filled = int(self.value * self.width)
            bar = "=" * filled + "-" * (self.width - filled)
            fb.draw_text(wx + self.x, wy + self.y, f"[{bar}]")
            
    def set_value(self, value: float):
        """Set progress value (0.0 to 1.0)"""
        self.value = max(0.0, min(1.0, value))


class Window:
    """Window class with widgets"""
    
    def __init__(self, x: int, y: int, w: int, h: int, title: str = "Window"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.widgets: List[Widget] = []
        self.focus = None
        self.z = 0  # Z-order
        self.visible = True
        self.draggable = True
        self.resizable = False
        
    def add_widget(self, widget: Widget):
        """Add widget to window"""
        self.widgets.append(widget)
        if self.focus is None:
            self.focus = widget
            
    def remove_widget(self, widget: Widget):
        """Remove widget from window"""
        if widget in self.widgets:
            self.widgets.remove(widget)
            if self.focus == widget:
                self.focus = self.widgets[0] if self.widgets else None
                
    def draw(self, fb: Framebuffer):
        """Draw window on framebuffer"""
        if not self.visible:
            return
            
        # Draw border
        fb.draw_text(self.x, self.y, "+" + "-" * (self.w - 2) + "+")
        for i in range(1, self.h - 1):
            fb.draw_text(self.x, self.y + i, "|" + " " * (self.w - 2) + "|")
        fb.draw_text(self.x, self.y + self.h - 1, "+" + "-" * (self.w - 2) + "+")
        
        # Draw title
        title_text = f"[{self.title}]"
        fb.draw_text(self.x + 2, self.y, title_text[:self.w - 4])
        
        # Draw widgets
        for widget in self.widgets:
            widget.draw(fb, self.x, self.y)
            
    def handle_event(self, event: Dict[str, Any]) -> bool:
        """Handle window event"""
        for widget in self.widgets:
            if widget.handle_event(event):
                return True
        return False
        
    def set_focus(self, widget: Widget):
        """Set focus to widget"""
        if widget in self.widgets:
            self.focus = widget


class GUIManager:
    """GUI Manager with window management and event loop"""
    
    def __init__(self, fb: Framebuffer, multitask_engine, ipc_bus):
        self.fb = fb
        self.windows: List[Window] = []
        self.focus = None
        self.engine = multitask_engine
        self.bus = ipc_bus
        self.running = False
        self.notification_callback = None
        self.stats = {
            'frames_rendered': 0,
            'events_processed': 0,
            'windows_created': 0,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for GUI notifications"""
        self.notification_callback = callback
        
    def add_window(self, win: Window):
        """Add window to manager"""
        win.z = len(self.windows)
        self.windows.append(win)
        self.focus = win
        self.stats['windows_created'] += 1
        
    def remove_window(self, win: Window):
        """Remove window from manager"""
        if win in self.windows:
            self.windows.remove(win)
            if self.focus == win:
                self.focus = self.windows[-1] if self.windows else None
                
    def draw(self):
        """Draw all windows"""
        self.fb.clear()
        for win in sorted(self.windows, key=lambda w: w.z):
            win.draw(self.fb)
        self.fb.render()
        self.stats['frames_rendered'] += 1
        
    def event_loop(self):
        """Main GUI event loop"""
        while self.running:
            # Receive IPC messages
            msg = self.bus.recv("gui", timeout=0.01)
            if msg:
                self.handle_ipc(msg)
                self.stats['events_processed'] += 1
                
            # Update GUI with task results
            for name, task in self.engine.results.items():
                if task and task.result is not None:
                    self.handle_task(name, task.result)
                    
            self.draw()
            time.sleep(0.05)
            
    def handle_ipc(self, msg: Any):
        """Handle IPC message"""
        # Example: update label with message
        for win in self.windows:
            for widget in win.widgets:
                if isinstance(widget, Label):
                    widget.set_text(str(msg))
                    
    def handle_task(self, name: str, result: Any):
        """Handle task result"""
        # Example: display task results
        for win in self.windows:
            for widget in win.widgets:
                if isinstance(widget, Label) and widget.text.startswith(name):
                    widget.set_text(f"{name}: {result}")
                    
    def start(self):
        """Start GUI manager"""
        self.running = True
        thread = threading.Thread(target=self.event_loop, daemon=True)
        thread.start()
        
    def stop(self):
        """Stop GUI manager"""
        self.running = False
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get GUI statistics"""
        return {
            'running': self.running,
            'frames_rendered': self.stats['frames_rendered'],
            'events_processed': self.stats['events_processed'],
            'windows_created': self.stats['windows_created'],
            'active_windows': len(self.windows),
            'framebuffer_size': f"{self.fb.w}x{self.fb.h}",
        }
        
    async def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            'frames_rendered': 0,
            'events_processed': 0,
            'windows_created': 0,
        }
