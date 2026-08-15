"""
 ============================================================
  MODULE/PLUGIN NAME: KernelTraps
  VERSION: 1.0.0
  MODULE CLASS: KernelTraps
  DESCRIPTION:
       Kernel trap handling for TerminalX kernel operations

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

import asyncio
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from enum import Enum


class TrapType(Enum):
    """Trap types"""
    SYSCALL = "syscall"
    PROCESS = "process"
    SIGNAL = "signal"
    PAGE_FAULT = "page_fault"
    GENERAL_PROTECTION = "general_protection"
    DIVIDE_ERROR = "divide_error"
    DEBUG = "debug"
    BREAKPOINT = "breakpoint"
    INTERRUPT = "interrupt"
    EXCEPTION = "exception"


class TrapAction(Enum):
    """Trap actions"""
    CONTINUE = "continue"
    TERMINATE = "terminate"
    SUSPEND = "suspend"
    IGNORE = "ignore"
    LOG = "log"
    CUSTOM = "custom"


class Traps:
    """Kernel trap handler"""
    
    def __init__(self):
        self.traps: Dict[str, List[Dict]] = {}
        self.trap_history: List[Dict] = []
        self.notification_callback = None
        self.stats = {
            'total_traps': 0,
            'traps_by_type': {},
            'handled_count': 0,
        }
        self.enabled = True
        
    def set_notification_callback(self, callback):
        """Set callback for trap notifications"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize trap handler"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        
    def register(self, trap_type: str, callback: Callable, priority: int = 10, 
                description: str = "") -> bool:
        """Register a trap handler"""
        if trap_type not in self.traps:
            self.traps[trap_type] = []
            
        self.traps[trap_type].append({
            'callback': callback,
            'priority': priority,
            'description': description,
            'registered_at': datetime.now().isoformat(),
        })
        
        # Sort by priority
        self.traps[trap_type].sort(key=lambda x: x['priority'])
        return True
        
    def unregister(self, trap_type: str, callback: Callable) -> bool:
        """Unregister a trap handler"""
        if trap_type not in self.traps:
            return False
            
        original_count = len(self.traps[trap_type])
        self.traps[trap_type] = [
            t for t in self.traps[trap_type]
            if t['callback'] != callback
        ]
        
        return len(self.traps[trap_type]) < original_count
            
    async def handle(self, trap_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a trap"""
        if not self.enabled:
            return {'handled': False, 'reason': 'Traps disabled'}
            
        self.stats['total_traps'] += 1
        self.stats['traps_by_type'][trap_type] = self.stats['traps_by_type'].get(trap_type, 0) + 1
        
        # Add to history
        trap_record = {
            'trap_type': trap_type,
            'data': data,
            'timestamp': datetime.now().isoformat(),
        }
        self.trap_history.append(trap_record)
        
        # Keep only last 1000 traps
        if len(self.trap_history) > 1000:
            self.trap_history = self.trap_history[-1000:]
        
        if trap_type not in self.traps:
            return {'handled': False, 'reason': 'No handlers registered'}
            
        handled = False
        action = TrapAction.CONTINUE.value
        results = []
        
        for trap in self.traps[trap_type]:
            try:
                callback = trap['callback']
                
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(data)
                else:
                    result = callback(data)
                    
                results.append({
                    'result': result,
                    'description': trap.get('description', ''),
                    'priority': trap['priority'],
                })
                    
                if result:
                    handled = True
                    self.stats['handled_count'] += 1
                    
                    # If result is a string, treat it as action
                    if isinstance(result, str) and result in [a.value for a in TrapAction]:
                        action = result
                        
            except Exception as e:
                results.append({
                    'error': str(e),
                    'description': trap.get('description', ''),
                    'priority': trap['priority'],
                })
                
        return {
            'handled': handled,
            'action': action,
            'results': results,
        }
        
    async def handle_syscall_trap(self, pid: int, syscall: str, args: List, 
                                  result: Any = None) -> Dict[str, Any]:
        """Handle syscall trap"""
        return await self.handle(TrapType.SYSCALL.value, {
            'pid': pid,
            'syscall': syscall,
            'args': args,
            'result': result,
        })
        
    async def handle_process_trap(self, pid: int, action: str, 
                                 exit_code: int = None) -> Dict[str, Any]:
        """Handle process trap"""
        return await self.handle(TrapType.PROCESS.value, {
            'pid': pid,
            'action': action,
            'exit_code': exit_code,
        })
        
    async def handle_signal_trap(self, pid: int, signal: int, 
                                 sender: int = None) -> Dict[str, Any]:
        """Handle signal trap"""
        result = await self.handle(TrapType.SIGNAL.value, {
            'pid': pid,
            'signal': signal,
            'sender': sender,
        })
        
        # Send notification for critical signals
        if signal in [9, 11, 15]:  # SIGKILL, SIGSEGV, SIGTERM
            if self.notification_callback:
                await self.notification_callback(
                    f"Critical signal trapped: {signal}",
                    f"PID: {pid}, Signal: {signal}",
                    'system',
                    'high'
                )
                
        return result
        
    async def handle_page_fault(self, pid: int, address: int, 
                                access_type: str) -> Dict[str, Any]:
        """Handle page fault trap"""
        return await self.handle(TrapType.PAGE_FAULT.value, {
            'pid': pid,
            'address': address,
            'access_type': access_type,
        })
        
    async def handle_general_protection(self, pid: int, error_code: int) -> Dict[str, Any]:
        """Handle general protection fault"""
        result = await self.handle(TrapType.GENERAL_PROTECTION.value, {
            'pid': pid,
            'error_code': error_code,
        })
        
        # Send notification for GPF
        if self.notification_callback:
            await self.notification_callback(
                f"General Protection Fault",
                f"PID: {pid}, Error code: {error_code}",
                'system',
                'critical'
            )
            
        return result
        
    async def handle_breakpoint(self, pid: int, address: int) -> Dict[str, Any]:
        """Handle breakpoint trap"""
        return await self.handle(TrapType.BREAKPOINT.value, {
            'pid': pid,
            'address': address,
        })
        
    async def handle_interrupt(self, interrupt_num: int, context: Dict) -> Dict[str, Any]:
        """Handle interrupt trap"""
        return await self.handle(TrapType.INTERRUPT.value, {
            'interrupt_num': interrupt_num,
            'context': context,
        })
        
    async def handle_exception(self, exception_type: str, pid: int, 
                              context: Dict) -> Dict[str, Any]:
        """Handle exception trap"""
        return await self.handle(TrapType.EXCEPTION.value, {
            'exception_type': exception_type,
            'pid': pid,
            'context': context,
        })
        
    async def get_history(self, trap_type: str = None, limit: int = 100) -> List[Dict]:
        """Get trap history"""
        if trap_type:
            return [t for t in self.trap_history if t['trap_type'] == trap_type][-limit:]
        return self.trap_history[-limit:]
        
    async def get_handlers(self, trap_type: str = None) -> Dict[str, List[Dict]]:
        """Get registered handlers"""
        if trap_type:
            if trap_type in self.traps:
                return {
                    trap_type: [
                        {
                            'priority': t['priority'],
                            'description': t.get('description', ''),
                            'registered_at': t['registered_at'],
                        }
                        for t in self.traps[trap_type]
                    ]
                }
            return {}
            
        return {
            name: [
                {
                    'priority': t['priority'],
                    'description': t.get('description', ''),
                    'registered_at': t['registered_at'],
                }
                for t in traps
            ]
            for name, traps in self.traps.items()
        }
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get trap statistics"""
        return {
            'enabled': self.enabled,
            'total_traps': self.stats['total_traps'],
            'traps_by_type': self.stats['traps_by_type'].copy(),
            'handled_count': self.stats['handled_count'],
            'handlers_registered': sum(len(handlers) for handlers in self.traps.values()),
            'history_size': len(self.trap_history),
        }
        
    async def clear_history(self):
        """Clear trap history"""
        self.trap_history.clear()
        
    async def clear_handlers(self, trap_type: str = None) -> bool:
        """Clear handlers"""
        if trap_type:
            if trap_type in self.traps:
                del self.traps[trap_type]
                return True
            return False
        self.traps.clear()
        return True
        
    async def enable(self):
        """Enable trap handling"""
        self.enabled = True
        
    async def disable(self):
        """Disable trap handling"""
        self.enabled = False
