"""
 ============================================================
  MODULE/PLUGIN NAME: Metadata
  VERSION: 1.0.0
  MODULE CLASS: Metadata
  DESCRIPTION:
       Metadata Module - Advanced metadata scanner, editor, creator and remover

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

from .metadata_module import MetadataModule, MetadataScanner, MetadataEditor, MetadataPlugin, MetadataPluginManager

__all__ = [
    'MetadataModule',
    'MetadataScanner',
    'MetadataEditor',
    'MetadataPlugin',
    'MetadataPluginManager',
]
