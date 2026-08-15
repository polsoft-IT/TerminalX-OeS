"""
 ============================================================
  MODULE/PLUGIN NAME: Debugger
  VERSION: 1.0.0
  MODULE CLASS: Debugger
  DESCRIPTION:
       Advanced debugger for TerminalX operations

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
import inspect
import traceback
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class DebuggerState(Enum):
    """Debugger states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STEPPING = "stepping"
    ERROR = "error"


@dataclass
class Breakpoint:
    """Breakpoint information"""
    file: str
    line: int
    condition: Optional[str] = None
    hit_count: int = 0
    enabled: bool = True


@dataclass
class Variable:
    """Variable information"""
    name: str
    value: Any
    type: str
    scope: str


@dataclass
class StackFrame:
    """Stack frame information"""
    file: str
    line: int
    function: str
    locals: Dict[str, Any]
    globals: Dict[str, Any]


class AdvancedDebugger:
    """Advanced debugger with stepping and breakpoints"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize debugger
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("AdvancedDebugger", LogLevel.INFO)
        self.state = DebuggerState.IDLE
        self.breakpoints: Dict[str, List[Breakpoint]] = {}
        self.current_frame: Optional[StackFrame] = None
        self.call_stack: List[StackFrame] = []
        self.step_mode: Optional[str] = None  # step, step_over, step_out
        self.step_depth: int = 0
        self.watch_expressions: List[str] = []
        
    def start(self) -> None:
        """Start debugger"""
        self.state = DebuggerState.RUNNING
        self.logger.info("Debugger started")
        
    def stop(self) -> None:
        """Stop debugger"""
        self.state = DebuggerState.IDLE
        self.call_stack.clear()
        self.current_frame = None
        self.step_mode = None
        self.logger.info("Debugger stopped")
        
    def pause(self) -> None:
        """Pause execution"""
        self.state = DebuggerState.PAUSED
        self.logger.info("Execution paused")
        
    def resume(self) -> None:
        """Resume execution"""
        self.state = DebuggerState.RUNNING
        self.step_mode = None
        self.logger.info("Execution resumed")
        
    def step(self) -> None:
        """Step to next line"""
        self.state = DebuggerState.STEPPING
        self.step_mode = "step"
        self.logger.info("Stepping")
        
    def step_over(self) -> None:
        """Step over current function"""
        self.state = DebuggerState.STEPPING
        self.step_mode = "step_over"
        self.step_depth = len(self.call_stack)
        self.logger.info("Stepping over")
        
    def step_out(self) -> None:
        """Step out of current function"""
        self.state = DebuggerState.STEPPING
        self.step_mode = "step_out"
        self.step_depth = len(self.call_stack)
        self.logger.info("Stepping out")
        
    def add_breakpoint(self, file: str, line: int, condition: Optional[str] = None) -> bool:
        """
        Add a breakpoint
        
        Args:
            file: File path
            line: Line number
            condition: Optional condition
            
        Returns:
            True if breakpoint added
        """
        if file not in self.breakpoints:
            self.breakpoints[file] = []
            
        # Check if breakpoint already exists
        for bp in self.breakpoints[file]:
            if bp.line == line:
                self.logger.warning(f"Breakpoint already exists at {file}:{line}")
                return False
                
        self.breakpoints[file].append(Breakpoint(
            file=file,
            line=line,
            condition=condition
        ))
        
        self.logger.info(f"Breakpoint added at {file}:{line}")
        return True
        
    def remove_breakpoint(self, file: str, line: int) -> bool:
        """
        Remove a breakpoint
        
        Args:
            file: File path
            line: Line number
            
        Returns:
            True if breakpoint removed
        """
        if file not in self.breakpoints:
            return False
            
        for i, bp in enumerate(self.breakpoints[file]):
            if bp.line == line:
                del self.breakpoints[file][i]
                self.logger.info(f"Breakpoint removed at {file}:{line}")
                return True
                
        return False
        
    def toggle_breakpoint(self, file: str, line: int) -> bool:
        """
        Toggle breakpoint enabled state
        
        Args:
            file: File path
            line: Line number
            
        Returns:
            True if toggled
        """
        if file not in self.breakpoints:
            return False
            
        for bp in self.breakpoints[file]:
            if bp.line == line:
                bp.enabled = not bp.enabled
                self.logger.info(f"Breakpoint toggled at {file}:{line} (enabled: {bp.enabled})")
                return True
                
        return False
        
    def clear_breakpoints(self, file: Optional[str] = None) -> None:
        """
        Clear breakpoints
        
        Args:
            file: File path (None for all)
        """
        if file:
            if file in self.breakpoints:
                del self.breakpoints[file]
                self.logger.info(f"Cleared breakpoints for {file}")
        else:
            self.breakpoints.clear()
            self.logger.info("Cleared all breakpoints")
            
    def get_breakpoints(self, file: Optional[str] = None) -> List[Breakpoint]:
        """
        Get breakpoints
        
        Args:
            file: File path (None for all)
            
        Returns:
            List of breakpoints
        """
        if file:
            return self.breakpoints.get(file, []).copy()
        
        all_bps = []
        for bps in self.breakpoints.values():
            all_bps.extend(bps)
        return all_bps
        
    def add_watch(self, expression: str) -> None:
        """
        Add watch expression
        
        Args:
            expression: Expression to watch
        """
        self.watch_expressions.append(expression)
        self.logger.info(f"Added watch: {expression}")
        
    def remove_watch(self, expression: str) -> bool:
        """
        Remove watch expression
        
        Args:
            expression: Expression to remove
            
        Returns:
            True if removed
        """
        if expression in self.watch_expressions:
            self.watch_expressions.remove(expression)
            self.logger.info(f"Removed watch: {expression}")
            return True
        return False
        
    def evaluate_watch(self, expression: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Evaluate watch expression
        
        Args:
            expression: Expression to evaluate
            context: Evaluation context
            
        Returns:
            Evaluation result
        """
        try:
            if context is None and self.current_frame:
                context = self.current_frame.locals
                
            return eval(expression, {}, context)
        except Exception as e:
            self.logger.error(f"Watch evaluation failed: {e}")
            return None
            
    def get_current_frame(self) -> Optional[StackFrame]:
        """
        Get current stack frame
        
        Returns:
            Current frame or None
        """
        return self.current_frame
        
    def get_call_stack(self) -> List[StackFrame]:
        """
        Get call stack
        
        Returns:
            List of stack frames
        """
        return self.call_stack.copy()
        
    def get_locals(self) -> Dict[str, Any]:
        """
        Get local variables
        
        Returns:
            Local variables dictionary
        """
        if self.current_frame:
            return self.current_frame.locals.copy()
        return {}
        
    def get_globals(self) -> Dict[str, Any]:
        """
        Get global variables
        
        Returns:
            Global variables dictionary
        """
        if self.current_frame:
            return self.current_frame.globals.copy()
        return {}
        
    def inspect_variable(self, name: str) -> Optional[Variable]:
        """
        Inspect a variable
        
        Args:
            name: Variable name
            
        Returns:
            Variable info or None
        """
        locals_dict = self.get_locals()
        globals_dict = self.get_globals()
        
        if name in locals_dict:
            return Variable(
                name=name,
                value=locals_dict[name],
                type=type(locals_dict[name]).__name__,
                scope="local"
            )
        elif name in globals_dict:
            return Variable(
                name=name,
                value=globals_dict[name],
                type=type(globals_dict[name]).__name__,
                scope="global"
            )
            
        return None
        
    def set_variable(self, name: str, value: Any, scope: str = "local") -> bool:
        """
        Set a variable value
        
        Args:
            name: Variable name
            value: New value
            scope: Variable scope (local, global)
            
        Returns:
            True if set successfully
        """
        if not self.current_frame:
            return False
            
        if scope == "local":
            self.current_frame.locals[name] = value
        elif scope == "global":
            self.current_frame.globals[name] = value
        else:
            return False
            
        self.logger.info(f"Set {scope} variable {name} = {value}")
        return True
        
    def get_state(self) -> DebuggerState:
        """
        Get debugger state
        
        Returns:
            Current state
        """
        return self.state
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get debugger statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'state': self.state.value,
            'breakpoints': sum(len(bps) for bps in self.breakpoints.values()),
            'call_stack_depth': len(self.call_stack),
            'watch_expressions': len(self.watch_expressions),
            'step_mode': self.step_mode
        }


# Global advanced debugger instance
advanced_debugger = AdvancedDebugger()
