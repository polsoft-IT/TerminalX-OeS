"""
 ============================================================
  MODULE/PLUGIN NAME: ProcessMonitor
  VERSION: 1.0.0
  MODULE CLASS: ProcessMonitor
  DESCRIPTION:
       Process Monitor Module - Process monitoring and management

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

from .process_monitor import ProcessMonitor
from .process_analyzer import ProcessAnalyzer
from .process_hooks import ProcessHooks

__all__ = [
    'ProcessMonitor',
    'ProcessAnalyzer',
    'ProcessHooks',
]
