"""
 ============================================================
  MODULE/PLUGIN NAME: Core
  VERSION: 1.0.0
  MODULE CLASS: Core
  DESCRIPTION:
       Core module - provides base infrastructure for TerminalX

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

import sys
import os

# Add parent directory to path when running directly
if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

# Handle both relative and absolute imports
try:
    from .core_engine import CoreEngine
    from .event_bus import EventBus
    from .config import Config
    from .logger import Logger
    from .runtime import Runtime
    from .scheduler import Scheduler
    from .cache_engine import CacheEngine
    from .cloud_engine import CloudEngine
    from .hooks import Hooks
    from .ansi import ANSI, ANSIColorsEngine, ansi_colors_engine
    from .color import Color
    from .ui_renderer import UIRenderer
    from .notification import NotificationSystem, Notification, NotificationType, NotificationPriority
    from .alert import AlertModule, AlertLevel, AlertChannel, alert_module
    from .multitask_engine import MultiTaskEngine, Task, TaskPriority, TaskStatus, MessageBus, Pipe, SharedBlock
    from .gui_enhancements import Framebuffer, Widget, Label, Button, TextBox, ProgressBar, Window, GUIManager, WidgetType
    from .emoji import EmojiLibrary, emoji_library, EMOJI, ALL_EMOJI
    from .unicode import UnicodeLibrary, unicode_library, UNICODE_ALL
    from .figlet import FigletEngine, figlet_engine
    from .animations import AnimationsEngine, animations_engine
    from .gui_widgets import GUIWidgetsLibrary, gui_widgets_library
    from .alias_engine import AliasEngine
except ImportError:
    # Fallback to absolute imports when running directly
    from core.core_engine import CoreEngine
    from core.event_bus import EventBus
    from core.config import Config
    from core.logger import Logger
    from core.runtime import Runtime
    from core.scheduler import Scheduler
    from core.cache_engine import CacheEngine
    from core.cloud_engine import CloudEngine
    from core.hooks import Hooks
    from core.ansi import ANSI, ANSIColorsEngine, ansi_colors_engine
    from core.color import Color
    from core.ui_renderer import UIRenderer
    from core.notification import NotificationSystem, Notification, NotificationType, NotificationPriority
    from core.alert import AlertModule, AlertLevel, AlertChannel, alert_module
    from core.multitask_engine import MultiTaskEngine, Task, TaskPriority, TaskStatus, MessageBus, Pipe, SharedBlock
    from core.gui_enhancements import Framebuffer, Widget, Label, Button, TextBox, ProgressBar, Window, GUIManager, WidgetType
    from core.emoji import EmojiLibrary, emoji_library, EMOJI, ALL_EMOJI
    from core.unicode import UnicodeLibrary, unicode_library, UNICODE_ALL
    from core.figlet import FigletEngine, figlet_engine
    from core.animations import AnimationsEngine, animations_engine
    from core.gui_widgets import GUIWidgetsLibrary, gui_widgets_library
    from core.alias_engine import AliasEngine

__all__ = [
    'CoreEngine',
    'EventBus',
    'Config',
    'Logger',
    'Runtime',
    'Scheduler',
    'CacheEngine',
    'CloudEngine',
    'Hooks',
    'ANSI',
    'ANSIColorsEngine',
    'ansi_colors_engine',
    'Color',
    'UIRenderer',
    'NotificationSystem',
    'Notification',
    'NotificationType',
    'NotificationPriority',
    'AlertModule',
    'AlertLevel',
    'AlertChannel',
    'alert_module',
    'MultiTaskEngine',
    'Task',
    'TaskPriority',
    'TaskStatus',
    'MessageBus',
    'Pipe',
    'SharedBlock',
    'Framebuffer',
    'Widget',
    'Label',
    'Button',
    'TextBox',
    'ProgressBar',
    'Window',
    'GUIManager',
    'WidgetType',
    'EmojiLibrary',
    'emoji_library',
    'EMOJI',
    'ALL_EMOJI',
    'UnicodeLibrary',
    'unicode_library',
    'UNICODE_ALL',
    'FigletEngine',
    'figlet_engine',
    'AnimationsEngine',
    'animations_engine',
    'GUIWidgetsLibrary',
    'gui_widgets_library',
    'AliasEngine',
]

# Allow running this module directly for testing
if __name__ == '__main__':
    import sys
    import os
    
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Test imports
    print("Testing core module imports...")
    print(f"CoreEngine: {CoreEngine}")
    print(f"EventBus: {EventBus}")
    print(f"Config: {Config}")
    print(f"Logger: {Logger}")
    print(f"Runtime: {Runtime}")
    print(f"Scheduler: {Scheduler}")
    print(f"CacheEngine: {CacheEngine}")
    print(f"CloudEngine: {CloudEngine}")
    print(f"Hooks: {Hooks}")
    print(f"ANSI: {ANSI}")
    print(f"Color: {Color}")
    print(f"UIRenderer: {UIRenderer}")
    
    # Test ANSI colors
    print("\nTesting ANSI colors:")
    print(ANSI.info("Info message"))
    print(ANSI.success("Success message"))
    print(ANSI.warning("Warning message"))
    print(ANSI.error("Error message"))
    
    print("\nCore module test completed successfully!")
