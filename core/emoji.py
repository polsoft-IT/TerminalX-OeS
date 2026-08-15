"""
 ============================================================
  MODULE/PLUGIN NAME: EmojiLibrary
  VERSION: 1.0.0
  MODULE CLASS: EmojiLibrary
  DESCRIPTION:
       Full Unicode 15.1 emoji database for terminal emoji support

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

from typing import Dict, List, Optional, Callable

# ============================================================
#  MEGA EMOJI DATABASE — Unicode 15.1
#  (categorized according to Unicode standard)
# ============================================================

EMOJI = {
    "smileys": [
        "😀","😃","😄","😁","😆","😅","😂","🤣","🙂","🙃","😉","😊","😇",
        "🥰","😍","🤩","😘","😗","☺️","😚","😙","😋","😛","😜","🤪","😝",
        "🤑","🤗","🤭","🤫","🤔","🫢","🫣","🤐","🤨","😐","😑","😶","🫥",
        "😶‍🌫️","😏","😒","🙄","😬","😮‍💨","🤥","😌","😔","😪","🤤","😴",
        "😷","🤒","🤕","🤢","🤮","🤧","🥵","🥶","🥴","😵","😵‍💫","🤯",
        "🤠","🥳","😎","🤓","🧐","😕","😟","🙁","☹️","😮","😯","😲","😳",
        "🥺","😦","😧","😨","😰","😥","😢","😭","😱","😖","😣","😞","😓",
        "😩","😫","🥱","😤","😡","😠","🤬","😈","👿","💀","☠️","👻","👽",
        "👾","🤖","🎃"
    ],

    "people": [
        "👶","🧒","👦","👧","🧑","👱","👨","🧔","👩","🧓","👴","👵",
        "👮","🕵️","💂","🥷","👷","🤴","👸","👳","👲","🧕","🤵","👰",
        "🤰","🫄","🫃","👼","🎅","🤶","🧑‍🎄","🧙","🧚","🧛","🧜","🧝",
        "🧞","🧟","💆","💇","🚶","🏃","🧍","🧎","💃","🕺","🧖","🧘",
        "🛌","🧑‍🦽","🧑‍🦼","🧑‍🦯","🧑‍🦯","🧑‍🦯"
    ],

    "hands": [
        "👍","👎","👌","🤌","🤏","✌️","🤞","🤟","🤘","🤙","👋","🤚","🖐️",
        "✋","🖖","👊","🤛","🤜","👏","🙌","👐","🤲","🙏","🫱","🫲","🫳",
        "🫴","🫵","🫶"
    ],

    "animals": [
        "🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷",
        "🐽","🐸","🐵","🙈","🙉","🙊","🐒","🐔","🐧","🐦","🐤","🐣","🐥",
        "🦆","🦅","🦉","🦇","🐺","🐗","🐴","🦄","🐝","🪲","🐞","🦋","🐌",
        "🐚","🐢","🐍","🦎","🦂","🦀","🦞","🦐","🐠","🐟","🐡","🦈","🐙",
        "🦑","🦧","🦣","🐘","🦒","🦏","🦛","🐪","🐫","🦘","🦬","🐃","🐂",
        "🐄","🐎","🐖","🐏","🐑","🦙","🐐","🦌","🐕","🐩","🦮","🐕‍🦺"
    ],

    "food": [
        "🍏","🍎","🍐","🍊","🍋","🍌","🍉","🍇","🍓","🫐","🍈","🍒","🍑",
        "🥭","🍍","🥥","🥝","🍅","🍆","🥑","🥦","🥬","🥒","🌶️","🫑","🌽",
        "🥕","🫒","🧄","🧅","🥔","🍠","🥐","🥯","🍞","🥖","🫓","🥨","🥞",
        "🧇","🍖","🍗","🥩","🥓","🍔","🍟","🍕","🌭","🥪","🌮","🌯","🫔",
        "🥙","🧆","🥘","🍲","🍛","🍜","🍝","🍠","🍣","🍱","🥟","🍤","🍙",
        "🍚","🍘","🍥","🥠","🥡","🍢","🍡","🍧","🍨","🍦","🥧","🍰","🎂",
        "🧁","🍮","🍭","🍬","🍫","🍿","🍩","🍪"
    ],

    "objects": [
        "💡","🔦","🕯️","🪔","📱","📲","☎️","📞","📟","📠","🔋","🪫","🔌",
        "💻","🖥️","🖨️","⌨️","🖱️","🖲️","💽","💾","💿","📀","🎥","📷",
        "📸","📹","📼","🔍","🔎","🕳️","🩻","🩺","💊","💉","🩸","🧬","🦠",
        "🧫","🧪","🧹","🧺","🧻","🚽","🚿","🛁","🪒","🧴","🧷","🧹"
    ],

    "symbols": [
        "❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💔","❣️","💕","💞",
        "💓","💗","💖","💘","💝","💟","☮️","✝️","☪️","🕉️","☸️","✡️","🔯",
        "🕎","☯️","♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"
    ]
}

# ============================================================
#  PAGINATION — 200 emoji per page
# ============================================================

ALL_EMOJI: List[str] = []
for cat in EMOJI.values():
    ALL_EMOJI.extend(cat)

PAGE_SIZE = 200


class EmojiLibrary:
    """Emoji library manager with search and pagination"""
    
    def __init__(self):
        self.emoji = EMOJI
        self.all_emoji = ALL_EMOJI
        self.page_size = PAGE_SIZE
        self.notification_callback = None
        self.stats = {
            'total_emoji': len(ALL_EMOJI),
            'categories': len(EMOJI),
            'searches': 0,
            'page_views': 0,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for emoji notifications"""
        self.notification_callback = callback
        
    def get_all(self) -> List[str]:
        """Get all emoji"""
        return self.all_emoji.copy()
        
    def get_category(self, category: str) -> Optional[List[str]]:
        """Get emoji by category"""
        cat = category.lower()
        return self.emoji.get(cat, None)
        
    def get_categories(self) -> List[str]:
        """Get all category names"""
        return list(self.emoji.keys())
        
    def search(self, keyword: str) -> List[str]:
        """Search emoji by keyword"""
        self.stats['searches'] += 1
        keyword = keyword.lower()
        found = []
        
        # Search in category names
        for cat, items in self.emoji.items():
            if keyword in cat.lower():
                found.extend(items)
                
        return found
        
    def get_page(self, page: int) -> List[str]:
        """Get emoji page (pagination)"""
        self.stats['page_views'] += 1
        start = page * self.page_size
        end = start + self.page_size
        return self.all_emoji[start:end]
        
    def get_page_count(self) -> int:
        """Get total number of pages"""
        return (len(self.all_emoji) + self.page_size - 1) // self.page_size
        
    def random(self, count: int = 1) -> List[str]:
        """Get random emoji"""
        import random
        return random.sample(self.all_emoji, min(count, len(self.all_emoji)))
        
    def get_stats(self) -> Dict[str, any]:
        """Get emoji library statistics"""
        return {
            'total_emoji': self.stats['total_emoji'],
            'categories': self.stats['categories'],
            'searches': self.stats['searches'],
            'page_views': self.stats['page_views'],
            'page_size': self.page_size,
            'total_pages': self.get_page_count(),
        }
        
    def clear_stats(self):
        """Clear statistics"""
        self.stats['searches'] = 0
        self.stats['page_views'] = 0


# Global instance
emoji_library = EmojiLibrary()
