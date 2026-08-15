"""
UI Renderer - User interface rendering
"""

from typing import List, Dict, Any
from .ansi import ANSI


class UIRenderer:
    """UI renderer for terminal interface"""
    
    def __init__(self):
        self.width = 80
        self.height = 24
        
    def render_header(self, title: str, subtitle: str = "") -> str:
        """Render header"""
        header = f"\n{ANSI.BOLD}{ANSI.CYAN}{title}{ANSI.RESET}"
        if subtitle:
            header += f"\n{ANSI.DIM}{subtitle}{ANSI.RESET}"
        header += "\n"
        return header
        
    def render_separator(self, char: str = "=") -> str:
        """Render separator line"""
        return char * self.width + "\n"
        
    def render_menu(self, items: List[Dict[str, Any]]) -> str:
        """Render menu items"""
        output = ""
        for i, item in enumerate(items, 1):
            label = item.get('label', '')
            description = item.get('description', '')
            output += f"{ANSI.GREEN}{i}.{ANSI.RESET} {ANSI.BOLD}{label}{ANSI.RESET}"
            if description:
                output += f" - {ANSI.DIM}{description}{ANSI.RESET}"
            output += "\n"
        return output
        
    def render_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Render table"""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
                
        output = ""
        
        # Header
        header = " | ".join(
            h.ljust(w) for h, w in zip(headers, col_widths)
        )
        output += f"{ANSI.BOLD}{header}{ANSI.RESET}\n"
        output += "-+-".join("-" * w for w in col_widths) + "\n"
        
        # Rows
        for row in rows:
            output += " | ".join(
                str(cell).ljust(w) for cell, w in zip(row, col_widths)
            ) + "\n"
            
        return output
        
    def render_progress(self, current: int, total: int, width: int = 50) -> str:
        """Render progress bar"""
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent:.1%}"
        
    def render_status(self, status: str, message: str) -> str:
        """Render status message"""
        colors = {
            'success': ANSI.GREEN,
            'error': ANSI.RED,
            'warning': ANSI.YELLOW,
            'info': ANSI.BLUE,
        }
        color = colors.get(status.lower(), ANSI.WHITE)
        return f"{color}[{status.upper()}]{ANSI.RESET} {message}"
