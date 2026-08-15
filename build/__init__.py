"""
 ============================================================
  MODULE/PLUGIN NAME: Build
  VERSION: 1.0.0
  MODULE CLASS: Build
  DESCRIPTION:
       Build system module for TerminalX

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

from .build_module import BuildModule
from .build_engine import ParallelBuildEngine, BuildStatus
from .dependency_installer import DependencyInstaller, DepType
from .plugin_build import PluginBuildSystem, PluginStatus

__all__ = [
    'BuildModule',
    'ParallelBuildEngine',
    'BuildStatus',
    'DependencyInstaller',
    'DepType',
    'PluginBuildSystem',
    'PluginStatus'
]
