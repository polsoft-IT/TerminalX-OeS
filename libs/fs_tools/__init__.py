"""
 ============================================================
  MODULE/PLUGIN NAME: FSTools
  VERSION: 1.0.0
  MODULE CLASS: FSTools
  DESCRIPTION:
       Filesystem Tools library - File scanning and watching utilities

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

from .scanner import Scanner
from .watcher import Watcher

__all__ = [
    'Scanner',
    'Watcher',
]