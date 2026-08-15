"""
 ============================================================
  MODULE/PLUGIN NAME: FigletEngine
  VERSION: 1.0.0
  MODULE CLASS: FigletEngine
  DESCRIPTION:
       Full FIGLET engine for Python terminal ASCII art rendering

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

import os
from typing import Dict, List, Optional

# ============================================================
#  Built-in FIGLET fonts (10 styles)
# ============================================================

BUILTIN_FONTS = {
    "block": [
        "██╗  ██╗",
        "██║  ██║",
        "███████║",
        "╚════██║",
        "     ██║",
        "     ╚═╝"
    ],
    "shadow": [
        " ▄█▀",
        "▄██ ",
        "▀██▄",
        " ▀█▄",
        "  ▀█",
        "   ▀"
    ],
    "bubble": [
        "  ___ ",
        " ( _ )",
        " / _ \\",
        "| (_) |",
        " \\___/",
        "      "
    ],
    "outline": [
        "╔═══╗",
        "║╔═╗║",
        "║║ ║║",
        "║╚═╝║",
        "╚═══╝",
        "     "
    ],
    "matrix": [
        "01 01",
        " 01  ",
        "01 01",
        " 01  ",
        "01 01",
        "     "
    ],
    "roman": [
        "  ____ ",
        " / __ \\",
        "| |  | |",
        "| |  | |",
        "| |__| |",
        " \\____/"
    ],
    "mini": [
        " _ ",
        "( )",
        "| |",
        "| |",
        "| |",
        "(_) "
    ],
    "fat": [
        "██████",
        "██    ",
        "█████ ",
        "██    ",
        "██████",
        "      "
    ],
    "thin": [
        " /\\ ",
        "/  \\",
        "\\  /",
        " \\/ ",
        "    ",
        "    "
    ],
    "tech": [
        "┏━┓",
        "┃ ┃",
        "┃ ┃",
        "┃ ┃",
        "┗━┛",
        "   "
    ]
}


class FigletEngine:
    """FIGLET engine for ASCII art rendering"""
    
    def __init__(self):
        self.builtin_fonts = BUILTIN_FONTS
        self.loaded_fonts: Dict[str, Dict[str, List[str]]] = {}
        self.notification_callback = None
        self.stats = {
            'renders': 0,
            'fonts_loaded': 0,
            'builtin_fonts': len(BUILTIN_FONTS),
        }
        
    def set_notification_callback(self, callback):
        """Set callback for figlet notifications"""
        self.notification_callback = callback
        
    def get_builtin_fonts(self) -> List[str]:
        """Get list of built-in font names"""
        return list(self.builtin_fonts.keys())
        
    def get_loaded_fonts(self) -> List[str]:
        """Get list of loaded font names"""
        return list(self.loaded_fonts.keys())
        
    def get_all_fonts(self) -> List[str]:
        """Get all available font names"""
        return list(self.builtin_fonts.keys()) + list(self.loaded_fonts.keys())
        
    def load_figlet_font(self, path: str) -> bool:
        """Load FIGLET font from .flf file"""
        if not os.path.isfile(path):
            if self.notification_callback:
                self.notification_callback(
                    f"Font file not found: {path}",
                    "File does not exist",
                    "error",
                    "medium"
                )
            return False
            
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
                
            # FIGLET FLF format — simplified loader
            header = lines[0]
            if not header.startswith("flf2a"):
                if self.notification_callback:
                    self.notification_callback(
                        f"Invalid FLF format: {path}",
                        "File is not a valid FIGLET font",
                        "error",
                        "medium"
                    )
                return False
                
            hardblank = header[5]
            height = int(header.split()[1])
            
            glyphs = {}
            index = 1
            for ascii_code in range(32, 127):
                if index + height <= len(lines):
                    char_lines = lines[index:index+height]
                    glyphs[chr(ascii_code)] = [l.replace(hardblank, " ") for l in char_lines]
                index += height
                
            name = os.path.basename(path).replace(".flf", "")
            self.loaded_fonts[name] = glyphs
            self.stats['fonts_loaded'] += 1
            
            if self.notification_callback:
                self.notification_callback(
                    f"Font loaded: {name}",
                    f"Successfully loaded {len(glyphs)} glyphs",
                    "success",
                    "low"
                )
                
            return True
            
        except Exception as e:
            if self.notification_callback:
                self.notification_callback(
                    f"Failed to load font: {path}",
                    str(e),
                    "error",
                    "medium"
                )
            return False
            
    def render(self, text: str, font: str = "block") -> str:
        """Render text as FIGLET ASCII art"""
        self.stats['renders'] += 1
        
        if font in self.builtin_fonts:
            glyph = self.builtin_fonts[font]
            out = []
            for line in glyph:
                out.append(" ".join([line for _ in text]))
            return "\n".join(out)
            
        if font in self.loaded_fonts:
            glyphs = self.loaded_fonts[font]
            if not glyphs:
                return f"Font '{font}' has no glyphs"
                
            height = len(next(iter(glyphs.values())))
            out = [""] * height
            
            for ch in text:
                if ch in glyphs:
                    g = glyphs[ch]
                    for i in range(min(height, len(g))):
                        out[i] += g[i]
                else:
                    for i in range(height):
                        out[i] += " "
                        
            return "\n".join(out)
            
        return f"Font not found: {font}"
        
    def render_builtin(self, text: str, font: str = "block") -> str:
        """Render text using built-in font only"""
        if font not in self.builtin_fonts:
            return f"Built-in font not found: {font}"
        return self.render(text, font)
        
    def render_loaded(self, text: str, font: str) -> str:
        """Render text using loaded font only"""
        if font not in self.loaded_fonts:
            return f"Loaded font not found: {font}"
        return self.render(text, font)
        
    def get_stats(self) -> Dict[str, any]:
        """Get figlet engine statistics"""
        return {
            'renders': self.stats['renders'],
            'fonts_loaded': self.stats['fonts_loaded'],
            'builtin_fonts': self.stats['builtin_fonts'],
            'total_fonts': len(self.get_all_fonts()),
        }
        
    def clear_stats(self):
        """Clear statistics"""
        self.stats['renders'] = 0
        self.stats['fonts_loaded'] = 0
        
    def unload_font(self, font: str) -> bool:
        """Unload a loaded font"""
        if font in self.loaded_fonts:
            del self.loaded_fonts[font]
            return True
        return False
        
    def unload_all_fonts(self):
        """Unload all loaded fonts"""
        self.loaded_fonts.clear()


# Global instance
figlet_engine = FigletEngine()
