"""
Color - Color utilities for terminal
"""

from typing import Tuple, Optional
import math


class Color:
    """Color utilities with multiple color systems"""
    
    # RGB values for common colors
    COLORS = {
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'yellow': (255, 255, 0),
        'blue': (0, 0, 255),
        'magenta': (255, 0, 255),
        'cyan': (0, 255, 255),
        'white': (255, 255, 255),
        # Extended colors
        'orange': (255, 165, 0),
        'pink': (255, 192, 203),
        'purple': (128, 0, 128),
        'brown': (165, 42, 42),
        'gray': (128, 128, 128),
        'lime': (0, 255, 0),
        'navy': (0, 0, 128),
        'teal': (0, 128, 128),
        'silver': (192, 192, 192),
        'maroon': (128, 0, 0),
        'olive': (128, 128, 0),
        'aqua': (0, 255, 255),
        'fuchsia': (255, 0, 255),
    }
    
    # 256-color palette
    COLOR_256 = {
        # Standard colors (0-7)
        0: (0, 0, 0),      # black
        1: (128, 0, 0),    # red
        2: (0, 128, 0),    # green
        3: (128, 128, 0),  # yellow
        4: (0, 0, 128),    # blue
        5: (128, 0, 128),  # magenta
        6: (0, 128, 128),  # cyan
        7: (192, 192, 192), # white
        # High intensity (8-15)
        8: (128, 128, 128), # bright black
        9: (255, 0, 0),    # bright red
        10: (0, 255, 0),   # bright green
        11: (255, 255, 0), # bright yellow
        12: (0, 0, 255),   # bright blue
        13: (255, 0, 255), # bright magenta
        14: (0, 255, 255), # bright cyan
        15: (255, 255, 255), # bright white
    }
    
    @staticmethod
    def rgb_to_ansi(r: int, g: int, b: int) -> str:
        """Convert RGB to ANSI escape code (True Color / 24-bit)"""
        return f'\033[38;2;{r};{g};{b}m'
        
    @staticmethod
    def rgb_to_ansi_256(r: int, g: int, b: int) -> str:
        """Convert RGB to 256-color ANSI escape code"""
        # Calculate the closest 256-color index
        if r == g == b:
            if r < 8:
                return '\033[38;5;16m'
            if r > 248:
                return '\033[38;5;231m'
            return f'\033[38;5;{232 + round((r - 8) / 10)}m'
        
        return f'\033[38;5;{Color.rgb_to_256_index(r, g, b)}m'
    
    @staticmethod
    def rgb_to_256_index(r: int, g: int, b: int) -> int:
        """Convert RGB to 256-color palette index"""
        # 6x6x6 color cube (16-231)
        if r == g == b:
            if r < 8:
                return 16
            if r > 248:
                return 231
            return 232 + round((r - 8) / 10)
        
        r_idx = min(5, round(r / 51))
        g_idx = min(5, round(g / 51))
        b_idx = min(5, round(b / 51))
        
        return 16 + (36 * r_idx) + (6 * g_idx) + b_idx
    
    @staticmethod
    def rgb_to_ansi_16(r: int, g: int, b: int) -> str:
        """Convert RGB to 16-color ANSI escape code"""
        # Find closest 16-color
        min_dist = float('inf')
        closest_idx = 7
        
        for idx, (cr, cg, cb) in Color.COLOR_256.items():
            if idx < 16:
                dist = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = idx
        
        return f'\033[38;5;{closest_idx}m'
        
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex color"""
        return f'#{r:02x}{g:02x}{b:02x}'
    
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSL (Hue, Saturation, Lightness)"""
        r, g, b = r / 255, g / 255, b / 255
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2
        
        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            
            h /= 6
        
        return (h * 360, s * 100, l * 100)
    
    @staticmethod
    def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL to RGB"""
        h, s, l = h / 360, s / 100, l / 100
        
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
        """Convert RGB to CMYK"""
        r, g, b = r / 255, g / 255, b / 255
        k = 1 - max(r, g, b)
        
        if k == 1:
            return (0, 0, 0, 1)
        
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
        
        return (c, m, y, k)
    
    @staticmethod
    def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> Tuple[int, int, int]:
        """Convert CMYK to RGB"""
        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
        return (r, g, b)
    
    @staticmethod
    def get_color(name: str) -> Tuple[int, int, int]:
        """Get RGB values for a named color"""
        return Color.COLORS.get(name.lower(), (255, 255, 255))
    
    @staticmethod
    def blend_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float = 0.5) -> Tuple[int, int, int]:
        """Blend two RGB colors"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)
    
    @staticmethod
    def adjust_brightness(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Adjust brightness of a color"""
        r = min(255, max(0, int(color[0] * factor)))
        g = min(255, max(0, int(color[1] * factor)))
        b = min(255, max(0, int(color[2] * factor)))
        return (r, g, b)
    
    @staticmethod
    def invert_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Invert a color"""
        return (255 - color[0], 255 - color[1], 255 - color[2])
    
    @staticmethod
    def grayscale(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convert color to grayscale"""
        gray = int(0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])
        return (gray, gray, gray)
    
    @staticmethod
    def is_dark(color: Tuple[int, int, int]) -> bool:
        """Check if color is dark"""
        r, g, b = color
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128
    
    @staticmethod
    def is_light(color: Tuple[int, int, int]) -> bool:
        """Check if color is light"""
        return not Color.is_dark(color)
