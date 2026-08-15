"""
 ============================================================
  MODULE/PLUGIN NAME: GUI
  VERSION: 1.0.0
  MODULE CLASS: GUI
  DESCRIPTION:
       GUI Module - Graphical User Interface for TerminalX

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

from .gui_engine import GUIEngine
from .gui_frameworks import GUIFrameworks
from .gui_widgets import GUIWidgets
from .gui_windows import GUIWindows
from .gui_apps import GUIApps

__all__ = [
    'GUIEngine',
    'GUIFrameworks',
    'GUIWidgets',
    'GUIWindows',
    'GUIApps',
]
