"""
 ============================================================
  MODULE/PLUGIN NAME: Defender
  VERSION: 1.0.0
  MODULE CLASS: Defender
  DESCRIPTION:
       Defender - Malware protection and scanning

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

from .defender import Defender

__all__ = ['Defender']
