"""
 ============================================================
  MODULE/PLUGIN NAME: CleanLogger
  VERSION: 1.0.0
  MODULE CLASS: CleanLogger
  DESCRIPTION:
       Lightweight logging without excess data for TerminalX

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

import sys
import time
from datetime import datetime
from typing import Optional, TextIO
from enum import Enum

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True, strip=False)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class LogLevel(Enum):
    """Log levels"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    SUCCESS = 5


class CleanLogger:
    """Lightweight logger with minimal overhead and colored output"""
    
    LEVEL_COLORS = {
        LogLevel.DEBUG: Fore.LIGHTBLACK_EX if COLORAMA_AVAILABLE else '\033[90m',
        LogLevel.INFO: Fore.BLUE if COLORAMA_AVAILABLE else '\033[94m',
        LogLevel.WARNING: Fore.YELLOW if COLORAMA_AVAILABLE else '\033[93m',
        LogLevel.ERROR: Fore.RED if COLORAMA_AVAILABLE else '\033[91m',
        LogLevel.CRITICAL: Fore.RED if COLORAMA_AVAILABLE else '\033[91m',
        LogLevel.SUCCESS: Fore.GREEN if COLORAMA_AVAILABLE else '\033[92m',
    }
    
    RESET = Style.RESET_ALL if COLORAMA_AVAILABLE else '\033[0m'
    
    def __init__(self, name: str, level: LogLevel = LogLevel.INFO, 
                 output: Optional[TextIO] = None, colored: bool = True):
        """
        Initialize clean logger
        
        Args:
            name: Logger name
            level: Minimum log level
            output: Output stream (default: stdout)
            colored: Enable colored output
        """
        self.name = name
        self.level = level
        self.output = output or sys.stdout
        self.start_time = time.time()
        self.colored = colored
        
    def _format_message(self, level: LogLevel, message: str) -> str:
        """Format log message with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_name = level.name
        
        if self.colored:
            color = self.LEVEL_COLORS.get(level, '')
            reset = self.RESET
            return f"[{timestamp}] [{color}{level_name}{reset}] {self.name}: {message}"
        else:
            return f"[{timestamp}] [{level_name}] {self.name}: {message}"
        
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged"""
        return level.value >= self.level.value
        
    def log(self, level: LogLevel, message: str) -> None:
        """Log message at specified level"""
        if self._should_log(level):
            formatted = self._format_message(level, message)
            print(formatted, file=self.output)
            
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.log(LogLevel.DEBUG, message)
        
    def info(self, message: str) -> None:
        """Log info message"""
        self.log(LogLevel.INFO, message)
        
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.log(LogLevel.WARNING, message)
        
    def error(self, message: str) -> None:
        """Log error message"""
        self.log(LogLevel.ERROR, message)
        
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.log(LogLevel.CRITICAL, message)
        
    def success(self, message: str) -> None:
        """Log success message"""
        self.log(LogLevel.SUCCESS, message)
        
    def set_level(self, level: LogLevel) -> None:
        """Set log level"""
        self.level = level
        
    def set_colored(self, colored: bool) -> None:
        """Enable or disable colored output"""
        self.colored = colored
        
    def get_elapsed_time(self) -> float:
        """Get elapsed time since logger creation"""
        return time.time() - self.start_time


# Global logger instance
default_logger = CleanLogger("TerminalX", LogLevel.INFO)
