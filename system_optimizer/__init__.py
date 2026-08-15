"""
 ============================================================
  MODULE/PLUGIN NAME: SystemOptimizer
  VERSION: 1.0.0
  MODULE CLASS: SystemOptimizer
  DESCRIPTION:
       SystemOpt v1 — Advanced RAM/CPU Optimizer (Godmode Architecture)

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

from .system_optimizer import SystemOptimizer, SystemOptConfig, EventBus
from .plugins import BasePlugin, LoggerPlugin, StatsPlugin, AlertPlugin, ThresholdPlugin
from .exceptions import SystemOptError, ProcessKillError, RAMCleanError, CPUOptError, PagefileError, ConfigError

__all__ = [
    'SystemOptimizer',
    'SystemOptConfig',
    'EventBus',
    'BasePlugin',
    'LoggerPlugin',
    'StatsPlugin',
    'AlertPlugin',
    'ThresholdPlugin',
    'SystemOptError',
    'ProcessKillError',
    'RAMCleanError',
    'CPUOptError',
    'PagefileError',
    'ConfigError',
]
