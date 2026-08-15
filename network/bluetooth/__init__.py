"""
 ============================================================
  MODULE/PLUGIN NAME: Bluetooth
  VERSION: 1.0.0
  MODULE CLASS: Bluetooth
  DESCRIPTION:
       Bluetooth Module - Bluetooth device management

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

from .bluetooth_manager import BluetoothManager
from .bluetooth_scanner import BluetoothScanner

__all__ = [
    'BluetoothManager',
    'BluetoothScanner',
]
