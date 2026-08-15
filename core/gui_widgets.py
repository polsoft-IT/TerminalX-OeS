"""
High-Quality, Fast, Stable GUI Widgets Library
AUTHOR: Sebastian Januchowski
COMPANY: polsoft.ITS™ Dev
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, List, Any


class FastLabel(tk.Label):
    """Ultra-fast label with no flicker."""
    
    def update_text(self, text: str):
        """Update label text without flicker"""
        self.config(text=text)
        self.update_idletasks()


class FastButton(tk.Button):
    """Instant-response button."""
    
    def __init__(self, master, text: str, command: Callable, **kw):
        super().__init__(master, text=text, command=command, **kw)
        self.config(cursor="hand2")


class InputBox(ttk.Entry):
    """Entry with validation + callback."""
    
    def __init__(self, master, on_change: Optional[Callable] = None, **kw):
        super().__init__(master, **kw)
        self.on_change = on_change
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace_add("write", self._changed)

    def _changed(self, *args):
        """Handle text change"""
        if self.on_change:
            self.on_change(self.var.get())

    def get_value(self) -> str:
        """Get current value"""
        return self.var.get()
    
    def set_value(self, value: str):
        """Set value"""
        self.var.set(value)


class ListView(tk.Frame):
    """Fast list with scrollbar."""
    
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.listbox = tk.Listbox(self, font=("Consolas", 14))
        self.scroll = tk.Scrollbar(self, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def add(self, text: str):
        """Add item to list"""
        self.listbox.insert(tk.END, text)

    def add_multiple(self, items: List[str]):
        """Add multiple items to list"""
        for item in items:
            self.listbox.insert(tk.END, item)

    def clear(self):
        """Clear all items"""
        self.listbox.delete(0, tk.END)

    def get_selected(self) -> Optional[str]:
        """Get selected item"""
        try:
            return self.listbox.get(self.listbox.curselection())
        except:
            return None
    
    def get_all(self) -> List[str]:
        """Get all items"""
        return self.listbox.get(0, tk.END)
    
    def remove_selected(self):
        """Remove selected item"""
        try:
            selection = self.listbox.curselection()
            if selection:
                self.listbox.delete(selection)
        except:
            pass


class ToggleSwitch(tk.Frame):
    """ON/OFF switch."""
    
    def __init__(self, master, initial: bool = False, on_toggle: Optional[Callable] = None, **kw):
        super().__init__(master, **kw)
        self.state = initial
        self.on_toggle = on_toggle
        self.btn = tk.Button(self, text=self._label(), width=6,
                             command=self.toggle, bg=self._color())
        self.btn.pack()

    def _label(self) -> str:
        """Get current label"""
        return "ON" if self.state else "OFF"

    def _color(self) -> str:
        """Get current color"""
        return "#44cc44" if self.state else "#cc4444"

    def toggle(self):
        """Toggle switch state"""
        self.state = not self.state
        self.btn.config(text=self._label(), bg=self._color())
        if self.on_toggle:
            self.on_toggle(self.state)

    def get(self) -> bool:
        """Get current state"""
        return self.state
    
    def set(self, state: bool):
        """Set state"""
        self.state = state
        self.btn.config(text=self._label(), bg=self._color())


class StatusBar(tk.Label):
    """Lightweight status bar."""
    
    def __init__(self, master, **kw):
        super().__init__(master, bd=1, relief="sunken", anchor="w", **kw)

    def set(self, text: str):
        """Set status text"""
        self.config(text=text)
        self.update_idletasks()
    
    def clear(self):
        """Clear status"""
        self.config(text="")


class TerminalBox(tk.Text):
    """Fast terminal-like output."""
    
    def __init__(self, master, **kw):
        super().__init__(master, font=("Consolas", 12), **kw)
        self.config(state="disabled")

    def write(self, text: str):
        """Write text to terminal"""
        self.config(state="normal")
        self.insert(tk.END, text + "\n")
        self.config(state="disabled")
        self.see(tk.END)
    
    def write_line(self, text: str, color: str = None):
        """Write colored line"""
        self.config(state="normal")
        if color:
            self.insert(tk.END, text + "\n", color)
        else:
            self.insert(tk.END, text + "\n")
        self.config(state="disabled")
        self.see(tk.END)
    
    def clear(self):
        """Clear terminal"""
        self.config(state="normal")
        self.delete(1.0, tk.END)
        self.config(state="disabled")


class ProgressMeter(ttk.Progressbar):
    """Smooth progress bar."""
    
    def set(self, value: float):
        """Set progress value"""
        self["value"] = value
        self.update_idletasks()
    
    def increment(self, amount: float = 1):
        """Increment progress"""
        current = self["value"]
        self["value"] = current + amount
        self.update_idletasks()
    
    def reset(self):
        """Reset progress"""
        self["value"] = 0
        self.update_idletasks()


class Separator(ttk.Separator):
    """Lightweight separator."""
    pass


class GUIWidgetsLibrary:
    """GUI widgets library manager"""
    
    def __init__(self):
        self.widgets = {
            'FastLabel': FastLabel,
            'FastButton': FastButton,
            'InputBox': InputBox,
            'ListView': ListView,
            'ToggleSwitch': ToggleSwitch,
            'StatusBar': StatusBar,
            'TerminalBox': TerminalBox,
            'ProgressMeter': ProgressMeter,
            'Separator': Separator,
        }
        self.notification_callback = None
        self.stats = {
            'widgets_created': 0,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for GUI notifications"""
        self.notification_callback = callback
        
    def create_widget(self, widget_type: str, master, **kwargs):
        """Create widget by type"""
        if widget_type not in self.widgets:
            if self.notification_callback:
                self.notification_callback(
                    f"Unknown widget type: {widget_type}",
                    "Widget creation failed",
                    "error",
                    "medium"
                )
            return None
        
        widget_class = self.widgets[widget_type]
        widget = widget_class(master, **kwargs)
        self.stats['widgets_created'] += 1
        return widget
    
    def get_available_widgets(self) -> List[str]:
        """Get list of available widgets"""
        return list(self.widgets.keys())
    
    def get_stats(self) -> dict:
        """Get GUI widgets statistics"""
        return {
            'widgets_created': self.stats['widgets_created'],
            'available_widgets': len(self.widgets),
        }
    
    def clear_stats(self):
        """Clear statistics"""
        self.stats['widgets_created'] = 0


# Global instance
gui_widgets_library = GUIWidgetsLibrary()
