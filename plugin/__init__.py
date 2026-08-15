"""
 ============================================================
  MODULE/PLUGIN NAME: Plugin
  VERSION: 1.0.0
  MODULE CLASS: Plugin
  DESCRIPTION:
       Plugin Module - Plugin system for TerminalX

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

from .core.plugin_manager import PluginManager

__all__ = [
    'PluginManager',
]
