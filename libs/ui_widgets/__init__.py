"""
 ============================================================
  MODULE/PLUGIN NAME: UIWidgets
  VERSION: 1.0.0
  MODULE CLASS: UIWidgets
  DESCRIPTION:
       UI Widgets library - Reusable UI components for terminal interfaces

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

from .box import Box
from .layout import Layout
from .table import Table

__all__ = [
    'Box',
    'Layout',
    'Table',
]