"""
 ============================================================
  MODULE/PLUGIN NAME: ANSI
  VERSION: 1.0.0
  MODULE CLASS: ANSI
  DESCRIPTION:
       ANSI escape codes for terminal formatting with RGB colors, gradients, and special effects

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

import random
from typing import List, Tuple


class ANSI:
    """ANSI escape codes with advanced color effects"""
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Styles
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Cursor
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[2K'
    HOME = '\033[H'
    UP = '\033[A'
    DOWN = '\033[B'
    RIGHT = '\033[C'
    LEFT = '\033[D'
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Generate RGB color code"""
        return f"\033[38;2;{r};{g};{b}m"
    
    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """Generate RGB background color code"""
        return f"\033[48;2;{r};{g};{b}m"
    
    @staticmethod
    def colorize(text: str, r: int, g: int, b: int) -> str:
        """Apply RGB color to text"""
        return ANSI.rgb(r, g, b) + text + ANSI.RESET
    
    @staticmethod
    def bg_colorize(text: str, r: int, g: int, b: int) -> str:
        """Apply RGB background color to text"""
        return ANSI.bg_rgb(r, g, b) + text + ANSI.RESET
        
    @staticmethod
    def color(text: str, color: str) -> str:
        """Apply color to text"""
        return f"{color}{text}{ANSI.RESET}"
        
    @staticmethod
    def bold(text: str) -> str:
        """Make text bold"""
        return f"{ANSI.BOLD}{text}{ANSI.RESET}"
        
    @staticmethod
    def underline(text: str) -> str:
        """Underline text"""
        return f"{ANSI.UNDERLINE}{text}{ANSI.RESET}"
        
    # Status colors with effects
    @staticmethod
    def info(text: str) -> str:
        """Info message (blue + bold)"""
        return f"{ANSI.BOLD}{ANSI.BLUE}{text}{ANSI.RESET}"
        
    @staticmethod
    def success(text: str) -> str:
        """Success message (green + bold)"""
        return f"{ANSI.BOLD}{ANSI.GREEN}{text}{ANSI.RESET}"
        
    @staticmethod
    def warning(text: str) -> str:
        """Warning message (yellow + bold)"""
        return f"{ANSI.BOLD}{ANSI.YELLOW}{text}{ANSI.RESET}"
        
    @staticmethod
    def error(text: str) -> str:
        """Error message (red + bold + blink)"""
        return f"{ANSI.BOLD}{ANSI.BLINK}{ANSI.RED}{text}{ANSI.RESET}"
        
    # Color effects
    @staticmethod
    def glow(text: str, color: str) -> str:
        """Glow effect (bold + dim cycle)"""
        return f"{ANSI.BOLD}{color}{text}{ANSI.RESET}"
        
    @staticmethod
    def highlight(text: str, color: str) -> str:
        """Highlight effect (background + bold)"""
        bg_map = {
            ANSI.RED: ANSI.BG_RED,
            ANSI.GREEN: ANSI.BG_GREEN,
            ANSI.YELLOW: ANSI.BG_YELLOW,
            ANSI.BLUE: ANSI.BG_BLUE,
            ANSI.MAGENTA: ANSI.BG_MAGENTA,
            ANSI.CYAN: ANSI.BG_CYAN,
            ANSI.WHITE: ANSI.BG_WHITE,
        }
        bg = bg_map.get(color, ANSI.BG_WHITE)
        return f"{ANSI.BOLD}{bg}{ANSI.BLACK}{text}{ANSI.RESET}"
        
    @staticmethod
    def strike(text: str) -> str:
        """Strikethrough effect (using reverse)"""
        return f"{ANSI.REVERSE}{text}{ANSI.RESET}"
        
    @staticmethod
    def box(text: str, color: str) -> str:
        """Box effect (underline + bold)"""
        return f"{ANSI.BOLD}{ANSI.UNDERLINE}{color}{text}{ANSI.RESET}"
    
    # Gradient effects
    @staticmethod
    def gradient_horizontal(text: str) -> str:
        """Horizontal gradient (red to blue)"""
        out = ""
        step = 255 // max(1, len(text))
        for i, ch in enumerate(text):
            out += ANSI.rgb(i * step, 0, 255 - i * step) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def gradient_vertical(text: str) -> str:
        """Vertical gradient (blue to cyan)"""
        out = ""
        for i, ch in enumerate(text):
            out += ANSI.rgb(0, i * 10 % 255, 255) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def gradient_diagonal(text: str) -> str:
        """Diagonal gradient (RGB cycle)"""
        out = ""
        for i, ch in enumerate(text):
            out += ANSI.rgb((i * 5) % 255, (i * 10) % 255, (i * 15) % 255) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def gradient_custom(text: str, start_rgb: Tuple[int, int, int], end_rgb: Tuple[int, int, int]) -> str:
        """Custom gradient between two RGB colors"""
        out = ""
        for i, ch in enumerate(text):
            if len(text) > 1:
                ratio = i / (len(text) - 1)
            else:
                ratio = 0
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    # Special effects
    @staticmethod
    def neon(text: str) -> str:
        """Neon effect (random bright colors)"""
        out = ""
        for ch in text:
            r = random.randint(150, 255)
            g = random.randint(0, 50)
            b = random.randint(200, 255)
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def rainbow(text: str) -> str:
        """Rainbow effect (7 colors)"""
        colors = [
            (255, 0, 0), (255, 127, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)
        ]
        out = ""
        for i, ch in enumerate(text):
            r, g, b = colors[i % len(colors)]
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def fire(text: str) -> str:
        """Fire effect (red/orange/yellow)"""
        out = ""
        for ch in text:
            r = random.randint(200, 255)
            g = random.randint(50, 100)
            b = random.randint(0, 20)
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def matrix(text: str) -> str:
        """Matrix effect (green)"""
        out = ""
        for ch in text:
            r = 0
            g = random.randint(150, 255)
            b = 0
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def ocean(text: str) -> str:
        """Ocean effect (blue/cyan)"""
        out = ""
        for ch in text:
            r = random.randint(0, 50)
            g = random.randint(100, 200)
            b = random.randint(200, 255)
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def sunset(text: str) -> str:
        """Sunset effect (purple/pink/orange)"""
        out = ""
        for ch in text:
            r = random.randint(200, 255)
            g = random.randint(50, 150)
            b = random.randint(150, 255)
            out += ANSI.rgb(r, g, b) + ch
        return out + ANSI.RESET
    
    @staticmethod
    def blue_gradient_banner(text: str) -> str:
        """Centered blue gradient banner effect"""
        try:
            gradient_text = ANSI.gradient_custom(text, (0, 100, 255), (0, 180, 255))
            return f"{ANSI.BOLD}{gradient_text}{ANSI.RESET}"
        except UnicodeEncodeError:
            return f"{ANSI.BOLD}{ANSI.CYAN}{text}{ANSI.RESET}"


class ANSIColorsEngine:
    """Advanced ANSI colors engine with statistics"""
    
    def __init__(self):
        self.stats = {
            'renders': 0,
            'gradients': 0,
            'effects': 0,
        }
        self.notification_callback = None
        
    def set_notification_callback(self, callback):
        """Set callback for ANSI notifications"""
        self.notification_callback = callback
        
    def rgb(self, r: int, g: int, b: int) -> str:
        """Generate RGB color code"""
        return ANSI.rgb(r, g, b)
        
    def colorize(self, text: str, r: int, g: int, b: int) -> str:
        """Apply RGB color to text"""
        self.stats['renders'] += 1
        return ANSI.colorize(text, r, g, b)
        
    def gradient_horizontal(self, text: str) -> str:
        """Horizontal gradient"""
        self.stats['gradients'] += 1
        return ANSI.gradient_horizontal(text)
        
    def gradient_vertical(self, text: str) -> str:
        """Vertical gradient"""
        self.stats['gradients'] += 1
        return ANSI.gradient_vertical(text)
        
    def gradient_diagonal(self, text: str) -> str:
        """Diagonal gradient"""
        self.stats['gradients'] += 1
        return ANSI.gradient_diagonal(text)
        
    def gradient_custom(self, text: str, start_rgb: Tuple[int, int, int], end_rgb: Tuple[int, int, int]) -> str:
        """Custom gradient"""
        self.stats['gradients'] += 1
        return ANSI.gradient_custom(text, start_rgb, end_rgb)
        
    def neon(self, text: str) -> str:
        """Neon effect"""
        self.stats['effects'] += 1
        return ANSI.neon(text)
        
    def rainbow(self, text: str) -> str:
        """Rainbow effect"""
        self.stats['effects'] += 1
        return ANSI.rainbow(text)
        
    def fire(self, text: str) -> str:
        """Fire effect"""
        self.stats['effects'] += 1
        return ANSI.fire(text)
        
    def matrix(self, text: str) -> str:
        """Matrix effect"""
        self.stats['effects'] += 1
        return ANSI.matrix(text)
        
    def ocean(self, text: str) -> str:
        """Ocean effect"""
        self.stats['effects'] += 1
        return ANSI.ocean(text)
        
    def sunset(self, text: str) -> str:
        """Sunset effect"""
        self.stats['effects'] += 1
        return ANSI.sunset(text)
        
    def blue_gradient_banner(self, text: str) -> str:
        """Blue gradient banner effect"""
        self.stats['effects'] += 1
        try:
            return ANSI.blue_gradient_banner(text)
        except UnicodeEncodeError:
            return f"{ANSI.BOLD}{ANSI.CYAN}{text}{ANSI.RESET}"
        
    def get_stats(self) -> dict:
        """Get ANSI engine statistics"""
        return self.stats.copy()
        
    def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            'renders': 0,
            'gradients': 0,
            'effects': 0,
        }


# Global instance
ansi_colors_engine = ANSIColorsEngine()
