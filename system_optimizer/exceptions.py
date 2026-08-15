"""
 ============================================================
  MODULE/PLUGIN NAME: SystemOptExceptions
  VERSION: 1.0.0
  MODULE CLASS: SystemOptExceptions
  DESCRIPTION:
       Exception classes for SystemOptimizer operations

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


class SystemOptError(Exception):
    """Base exception for system optimizer"""
    pass


class ProcessKillError(SystemOptError):
    """Exception raised when process kill fails"""
    pass


class RAMCleanError(SystemOptError):
    """Exception raised when RAM cleaning fails"""
    pass


class CPUOptError(SystemOptError):
    """Exception raised when CPU optimization fails"""
    pass


class PagefileError(SystemOptError):
    """Exception raised when pagefile cleaning fails"""
    pass


class ConfigError(SystemOptError):
    """Exception raised when configuration is invalid"""
    pass
