"""
 ============================================================
  MODULE/PLUGIN NAME: AI
  VERSION: 1.0.0
  MODULE CLASS: AI
  DESCRIPTION:
       AI Module - Artificial Intelligence integration for TerminalX

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

from .ai_core import AICore
from .ai_models import AIModels
from .ai_analyzer import AIAnalyzer
from .ai_sentinel import AISentinel
from .ai_plugins import AIPlugins

__all__ = [
    'AICore',
    'AIModels',
    'AIAnalyzer',
    'AISentinel',
    'AIPlugins',
]
