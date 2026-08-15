"""
 ============================================================
  MODULE/PLUGIN NAME: WiFi
  VERSION: 1.0.0
  MODULE CLASS: WiFi
  DESCRIPTION:
       WiFi Module - WiFi network management

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

from .wifi_manager import WiFiManager
from .wifi_scanner import WiFiScanner

__all__ = [
    'WiFiManager',
    'WiFiScanner',
]
