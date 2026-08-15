"""
 ============================================================
  MODULE/PLUGIN NAME: Debug
  VERSION: 1.0.0
  MODULE CLASS: Debug
  DESCRIPTION:
       Module debugging utilities for TerminalX

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
import traceback
import inspect
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class DebugEvent:
    """Debug event"""
    timestamp: str
    level: str
    module: str
    function: str
    message: str
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


class DebugManager:
    """Module debugging utilities"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize debug manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("DebugManager", LogLevel.INFO)
        self.debug_events: List[DebugEvent] = []
        self.breakpoints: Dict[str, List[int]] = {}
        self.watched_variables: Dict[str, Any] = {}
        self.debug_enabled = False
        self.max_events = 1000
        
    def enable_debug(self) -> None:
        """Enable debugging"""
        self.debug_enabled = True
        self.logger.info("Debugging enabled")
        
    def disable_debug(self) -> None:
        """Disable debugging"""
        self.debug_enabled = False
        self.logger.info("Debugging disabled")
        
    def log_event(self, level: str, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a debug event
        
        Args:
            level: Event level (debug, info, warning, error)
            message: Event message
            data: Additional data
        """
        if not self.debug_enabled:
            return
            
        # Get caller info
        frame = inspect.currentframe()
        if frame and frame.f_back:
            module = frame.f_back.f_globals.get('__name__', 'unknown')
            function = frame.f_back.f_code.co_name
        else:
            module = 'unknown'
            function = 'unknown'
            
        event = DebugEvent(
            timestamp=datetime.now().isoformat(),
            level=level,
            module=module,
            function=function,
            message=message,
            data=data or {}
        )
        
        self.debug_events.append(event)
        
        # Trim events if needed
        if len(self.debug_events) > self.max_events:
            self.debug_events = self.debug_events[-self.max_events:]
            
    def set_breakpoint(self, module: str, line: int) -> bool:
        """
        Set a breakpoint
        
        Args:
            module: Module name
            line: Line number
            
        Returns:
            True if breakpoint set
        """
        if module not in self.breakpoints:
            self.breakpoints[module] = []
            
        if line not in self.breakpoints[module]:
            self.breakpoints[module].append(line)
            self.logger.info(f"Breakpoint set: {module}:{line}")
            return True
            
        return False
        
    def remove_breakpoint(self, module: str, line: int) -> bool:
        """
        Remove a breakpoint
        
        Args:
            module: Module name
            line: Line number
            
        Returns:
            True if breakpoint removed
        """
        if module in self.breakpoints and line in self.breakpoints[module]:
            self.breakpoints[module].remove(line)
            self.logger.info(f"Breakpoint removed: {module}:{line}")
            return True
        return False
        
    def clear_breakpoints(self, module: Optional[str] = None) -> None:
        """
        Clear breakpoints
        
        Args:
            module: Module name (None for all)
        """
        if module:
            if module in self.breakpoints:
                del self.breakpoints[module]
                self.logger.info(f"Cleared breakpoints for {module}")
        else:
            self.breakpoints.clear()
            self.logger.info("Cleared all breakpoints")
            
    def watch_variable(self, name: str, value: Any) -> None:
        """
        Watch a variable
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.watched_variables[name] = value
        self.logger.info(f"Watching variable: {name}")
        
    def unwatch_variable(self, name: str) -> bool:
        """
        Stop watching a variable
        
        Args:
            name: Variable name
            
        Returns:
            True if unwatched
        """
        if name in self.watched_variables:
            del self.watched_variables[name]
            self.logger.info(f"Stopped watching: {name}")
            return True
        return False
        
    def get_watched_variables(self) -> Dict[str, Any]:
        """
        Get watched variables
        
        Returns:
            Dictionary of watched variables
        """
        return self.watched_variables.copy()
        
    def get_events(self, level: Optional[str] = None, module: Optional[str] = None,
                  limit: Optional[int] = None) -> List[DebugEvent]:
        """
        Get debug events
        
        Args:
            level: Filter by level
            module:_filter by module
            limit: Maximum events to return
            
        Returns:
            List of debug events
        """
        events = self.debug_events
        
        if level:
            events = [e for e in events if e.level == level]
            
        if module:
            events = [e for e in events if e.module == module]
            
        if limit:
            events = events[-limit:]
            
        return events
        
    def clear_events(self) -> None:
        """Clear all debug events"""
        self.debug_events.clear()
        self.logger.info("Cleared debug events")
        
    def trace_function(self, func: Callable) -> Callable:
        """
        Decorator to trace function execution
        
        Args:
            func: Function to trace
            
        Returns:
            Wrapped function
        """
        def wrapper(*args, **kwargs):
            self.log_event('debug', f"Entering {func.__name__}", {'args': str(args), 'kwargs': str(kwargs)})
            try:
                result = func(*args, **kwargs)
                self.log_event('debug', f"Exiting {func.__name__}", {'result': str(result)})
                return result
            except Exception as e:
                self.log_event('error', f"Error in {func.__name__}", {'error': str(e), 'traceback': traceback.format_exc()})
                raise
                
        return wrapper
        
    def inspect_object(self, obj: Any) -> Dict[str, Any]:
        """
        Inspect an object
        
        Args:
            obj: Object to inspect
            
        Returns:
            Inspection data
        """
        return {
            'type': type(obj).__name__,
            'module': type(obj).__module__,
            'class': obj.__class__.__name__,
            'attributes': [attr for attr in dir(obj) if not attr.startswith('_')],
            'methods': [method for method in dir(obj) if callable(getattr(obj, method, None))],
            'size': sys.getsizeof(obj)
        }
        
    def get_call_stack(self) -> List[Dict[str, Any]]:
        """
        Get current call stack
        
        Returns:
            List of stack frame info
        """
        stack = []
        
        for frame in inspect.stack():
            stack.append({
                'filename': frame.filename,
                'line': frame.lineno,
                'function': frame.function,
                'code': frame.code_context
            })
            
        return stack
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get debug statistics
        
        Returns:
            Statistics dictionary
        """
        level_counts = {}
        for event in self.debug_events:
            level_counts[event.level] = level_counts.get(event.level, 0) + 1
            
        return {
            'debug_enabled': self.debug_enabled,
            'total_events': len(self.debug_events),
            'level_counts': level_counts,
            'breakpoints': sum(len(bps) for bps in self.breakpoints.values()),
            'watched_variables': len(self.watched_variables)
        }


# Global debug manager instance
debug_manager = DebugManager()
