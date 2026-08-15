"""
 ============================================================
  MODULE/PLUGIN NAME: Report
  VERSION: 1.0.0
  MODULE CLASS: Report
  DESCRIPTION:
       Report Module - Advanced report engine with plugin system for TerminalX

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

from .report_engine import (
    ReportEngine,
    Report,
    ReportSection,
    ReportEngineConfig,
    PluginRegistry,
    PluginContext,
    ReportPlugin,
    TemplatePlugin,
    OutputPlugin,
    FilterPlugin,
    PostProcessPlugin,
    create_default_engine,
)

__all__ = [
    'ReportEngine',
    'Report',
    'ReportSection',
    'ReportEngineConfig',
    'PluginRegistry',
    'PluginContext',
    'ReportPlugin',
    'TemplatePlugin',
    'OutputPlugin',
    'FilterPlugin',
    'PostProcessPlugin',
    'create_default_engine',
]
