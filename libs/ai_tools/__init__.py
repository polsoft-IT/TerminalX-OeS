"""
 ============================================================
  MODULE/PLUGIN NAME: AITools
  VERSION: 1.0.0
  MODULE CLASS: AITools
  DESCRIPTION:
       AI Tools library - AI-powered analysis and processing tools

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

from .analyzer import AIAnalyzer
from .tokenizer import Tokenizer
from .vectorizer import Vectorizer

__all__ = [
    'AIAnalyzer',
    'Tokenizer',
    'Vectorizer',
]