"""
 ============================================================
  MODULE/PLUGIN NAME: UnicodeLibrary
  VERSION: 1.0.0
  MODULE CLASS: UnicodeLibrary
  DESCRIPTION:
       Full Unicode library with 10k+ characters for terminal support

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

import unicodedata
from typing import List, Dict, Optional

# ============================================================
#  FULL UNICODE — BMP + extensions
# ============================================================

# Collect all Unicode characters BMP + extensions
UNICODE_ALL: List[str] = []
UNICODE_ALL.extend([chr(i) for i in range(0x0000, 0x2FFF)])
UNICODE_ALL.extend([chr(i) for i in range(0x3000, 0xD7FF)])
UNICODE_ALL.extend([chr(i) for i in range(0xE000, 0xFFFF)])

PAGE_SIZE = 300


class UnicodeLibrary:
    """Unicode library manager with search and pagination"""
    
    def __init__(self):
        self.unicode_all = UNICODE_ALL
        self.page_size = PAGE_SIZE
        self.notification_callback = None
        self.stats = {
            'total_chars': len(UNICODE_ALL),
            'searches': 0,
            'page_views': 0,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for unicode notifications"""
        self.notification_callback = callback
        
    def get_all(self) -> List[str]:
        """Get all unicode characters"""
        return self.unicode_all.copy()
        
    def get_page(self, page: int) -> List[str]:
        """Get unicode page (pagination)"""
        self.stats['page_views'] += 1
        start = page * self.page_size
        end = start + self.page_size
        return self.unicode_all[start:end]
        
    def get_page_count(self) -> int:
        """Get total number of pages"""
        return (len(self.unicode_all) + self.page_size - 1) // self.page_size
        
    def find_by_name(self, keyword: str) -> List[str]:
        """Find unicode characters by name"""
        self.stats['searches'] += 1
        keyword = keyword.lower()
        found = []
        
        for ch in self.unicode_all:
            try:
                name = unicodedata.name(ch, "").lower()
                if keyword in name:
                    found.append(ch)
            except (ValueError, TypeError):
                continue
                
        return found
        
    def find_by_block(self, block_name: str) -> List[str]:
        """Find unicode characters by block name"""
        self.stats['searches'] += 1
        block_name = block_name.lower()
        found = []
        
        for ch in self.unicode_all:
            try:
                name = unicodedata.name(ch, "").lower()
                if block_name in name:
                    found.append(ch)
            except (ValueError, TypeError):
                continue
                
        return found
        
    def get_char_info(self, char: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a character"""
        if len(char) != 1:
            return None
            
        try:
            return {
                'char': char,
                'name': unicodedata.name(char, "UNKNOWN"),
                'category': unicodedata.category(char),
                'combining': unicodedata.combining(char),
                'east_asian_width': unicodedata.east_asian_width(char),
                'mirrored': unicodedata.mirrored(char),
                'numeric': unicodedata.numeric(char, None),
                'decimal': unicodedata.decimal(char, None),
                'digit': unicodedata.digit(char, None),
            }
        except (ValueError, TypeError):
            return None
            
    def get_category(self, category: str) -> List[str]:
        """Get all characters in a specific Unicode category"""
        found = []
        for ch in self.unicode_all:
            try:
                if unicodedata.category(ch) == category:
                    found.append(ch)
            except (ValueError, TypeError):
                continue
        return found
        
    def get_categories(self) -> List[str]:
        """Get all Unicode categories present"""
        categories = set()
        for ch in self.unicode_all:
            try:
                categories.add(unicodedata.category(ch))
            except (ValueError, TypeError):
                continue
        return sorted(list(categories))
        
    def random(self, count: int = 1) -> List[str]:
        """Get random unicode characters"""
        import random
        return random.sample(self.unicode_all, min(count, len(self.unicode_all)))
        
    def get_stats(self) -> Dict[str, any]:
        """Get unicode library statistics"""
        return {
            'total_chars': self.stats['total_chars'],
            'searches': self.stats['searches'],
            'page_views': self.stats['page_views'],
            'page_size': self.page_size,
            'total_pages': self.get_page_count(),
            'categories': len(self.get_categories()),
        }
        
    def clear_stats(self):
        """Clear statistics"""
        self.stats['searches'] = 0
        self.stats['page_views'] = 0


# Global instance
unicode_library = UnicodeLibrary()
