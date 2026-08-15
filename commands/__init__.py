"""
 ============================================================
  MODULE/PLUGIN NAME: Commands
  VERSION: 1.0.2
  MODULE CLASS: Commands
  DESCRIPTION:
       Commands Module - Command handlers for TerminalX (updated with wifi, lan, ethernet command handlers)

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

from .terminal import TerminalCommands
from .ai import AICommands
from .gui import GUICommands
from .network import NetworkCommands
from .kernel import KernelCommands
from .shield import ShieldCommands
from .process import ProcessCommands
from .cloud import CloudCommands
from .advanced_shield import AdvancedShieldCommands
from .module_commands import ModuleCommands
from .plugin import PluginCommands
from .cd import CDCommands
from .dev import DevCommands
from .geo import GeoCommands
from .system_opt import SystemOptCommands
from .man import ManCommands
from .event import EventCommands
from .bluetooth import BluetoothCommands
from .wifi import WiFiCommands
from .lan import LANCommands
from .ethernet import EthernetCommands
from .alert import AlertCommands
from .alias import AliasCommands

# Direct import of VersionCommands to avoid import issues
import sys
import os
import importlib.util
spec = importlib.util.spec_from_file_location("version_commands", os.path.join(os.path.dirname(__file__), "version.py"))
version_commands_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_commands_module)
VersionCommands = version_commands_module.VersionCommands

# Direct import of ReportCommands to avoid import issues
spec = importlib.util.spec_from_file_location("report_commands", os.path.join(os.path.dirname(__file__), "report.py"))
report_commands_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report_commands_module)
ReportCommands = report_commands_module.ReportCommands

__all__ = [
    'TerminalCommands',
    'AICommands',
    'GUICommands',
    'NetworkCommands',
    'KernelCommands',
    'ShieldCommands',
    'ProcessCommands',
    'CloudCommands',
    'AdvancedShieldCommands',
    'ModuleCommands',
    'PluginCommands',
    'CDCommands',
    'DevCommands',
    'GeoCommands',
    'SystemOptCommands',
    'ManCommands',
    'EventCommands',
    'BluetoothCommands',
    'WiFiCommands',
    'LANCommands',
    'EthernetCommands',
    'AlertCommands',
    'AliasCommands',
    'VersionCommands',
    'ReportCommands',
]
