"""
Logging - Logging system for TerminalX
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional


def enable_windows_vt():
    """Enable Windows VT mode for ANSI colors"""
    if sys.platform == 'win32':
        try:
            import ctypes
            from ctypes import wintypes
            STD_OUTPUT_HANDLE = -11
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32 = ctypes.windll.kernel32
            h_out = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = wintypes.DWORD()
            kernel32.GetConsoleMode(h_out, ctypes.byref(mode))
            mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(h_out, mode)
            
            # Also try to enable for stderr
            h_err = kernel32.GetStdHandle(-12)  # STD_ERROR_HANDLE
            if h_err:
                err_mode = wintypes.DWORD()
                kernel32.GetConsoleMode(h_err, ctypes.byref(err_mode))
                err_mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(h_err, err_mode)
            
            return True
        except Exception as e:
            print(f"Warning: Could not enable VT mode: {e}")
            return False
    return True


# Enable Windows VT mode at module import
enable_windows_vt()

# Register custom SUCCESS level
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, 'SUCCESS')


class ColoredFormatter(logging.Formatter):
    """Custom formatter with ANSI colors for log levels"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .ansi import ANSI
        
        self.COLORS = {
            'DEBUG': ANSI.CYAN,
            'INFO': ANSI.BRIGHT_BLUE,
            'WARNING': ANSI.BRIGHT_YELLOW,
            'ERROR': ANSI.BRIGHT_RED,
            'CRITICAL': ANSI.BRIGHT_MAGENTA,
            'SUCCESS': ANSI.BRIGHT_GREEN,
        }
        self.RESET = ANSI.RESET
    
    def format(self, record):
        """Format log record with colors"""
        log_color = self.COLORS.get(record.levelname, '')
        # Store original levelname
        original_levelname = record.levelname
        # Modify levelname with colors
        if log_color:
            record.levelname = f"{log_color}{original_levelname}{self.RESET}"
        # Format the message
        message = super().format(record)
        # Restore original levelname
        record.levelname = original_levelname
        return message


class Logger:
    """Logger for TerminalX"""
    
    def __init__(self, name: str = "TerminalX", log_dir: str = None):
        self.name = name
        self.log_dir = log_dir or os.path.join(
            os.path.dirname(__file__), '..', 'logs'
        )
        self.logger = logging.getLogger(name)
        self._setup()
        
    def _setup(self):
        """Setup logger"""
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_file = os.path.join(
            self.log_dir,
            f"{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        # File handler (no colors for file)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler (with colors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)
        
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
        
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
        
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
        
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
        
    def success(self, message: str):
        """Log success message"""
        self.logger.log(SUCCESS_LEVEL, message)
