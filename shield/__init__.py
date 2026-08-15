"""
 ============================================================
  MODULE/PLUGIN NAME: Shield
  VERSION: 1.0.0
  MODULE CLASS: Shield
  DESCRIPTION:
       Shield Module - Security and protection for TerminalX

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

from .defender.defender import Defender
from .firewall.firewall import Firewall
from .sandbox.sandbox import Sandbox
from .threat_intel.threat_intel import ThreatIntel

__all__ = [
    'Defender',
    'Firewall',
    'Sandbox',
    'ThreatIntel',
]
