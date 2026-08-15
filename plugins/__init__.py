"""
 ============================================================
  MODULE/PLUGIN NAME: Plugins
  VERSION: 1.0.0
  MODULE CLASS: Plugins
  DESCRIPTION:
       Plugins Module - Alternative plugin management for TerminalX

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

from .plugin_manager import PluginManager
from .plugin_api import PluginAPI
from .plugin_monitor import PluginMonitor
from .plugin_sandbox import PluginSandbox

__all__ = [
    'PluginManager',
    'PluginAPI',
    'PluginMonitor',
    'PluginSandbox',
]