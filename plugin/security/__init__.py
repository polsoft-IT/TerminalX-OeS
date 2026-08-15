"""
 ============================================================
  MODULE/PLUGIN NAME: PluginSecurity
  VERSION: 1.0.0
  MODULE CLASS: PluginSecurity
  DESCRIPTION:
       Plugin Security - Security components for plugin system

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

from .verifier import PluginVerifier
from .permissions import PluginPermissions

__all__ = [
    'PluginVerifier',
    'PluginPermissions',
]
