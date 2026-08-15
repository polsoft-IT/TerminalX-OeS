"""
 ============================================================
  MODULE/PLUGIN NAME: ManPages
  VERSION: 1.0.4
  MODULE CLASS: ManPages
  DESCRIPTION:
       Man Pages Module - Advanced manual page system for TerminalX commands and documentation (36 pages including wifi with 52 PRO commands, lan, ethernet)

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

from .man_engine import ManEngine
from .man_parser import ManParser
from .man_viewer import ManViewer
from .man_cache import ManCache

__all__ = [
    'ManEngine',
    'ManParser',
    'ManViewer',
    'ManCache',
]
