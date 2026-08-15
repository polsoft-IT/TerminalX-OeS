"""
 ============================================================
  MODULE/PLUGIN NAME: Modules
  VERSION: 1.0.0
  MODULE CLASS: Modules
  DESCRIPTION:
       Modules Module - Module management for TerminalX

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

from libs.module_manager import ModuleManager, ModuleProfile

__all__ = [
    'ModuleManager',
    'ModuleProfile',
]