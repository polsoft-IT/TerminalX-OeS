"""
 ============================================================
  MODULE/PLUGIN NAME: PluginCore
  VERSION: 1.0.0
  MODULE CLASS: PluginCore
  DESCRIPTION:
       Plugin Core - Core plugin system components

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

from .plugin_manager import PluginManager, PluginManagerConfig
from .loader import PluginLoader, PluginInfo
from .registry import PluginRegistry, PluginRegistryEntry
from .sandbox import PluginSandbox
from .api import PluginAPI, PluginAPIContext
from .hooks import PluginHooks
from .events import PluginEvents

__all__ = [
    'PluginManager',
    'PluginManagerConfig',
    'PluginLoader',
    'PluginInfo',
    'PluginRegistry',
    'PluginRegistryEntry',
    'PluginSandbox',
    'PluginAPI',
    'PluginAPIContext',
    'PluginHooks',
    'PluginEvents',
]
