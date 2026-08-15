"""
 ============================================================
  MODULE/PLUGIN NAME: KernelEvents
  VERSION: 1.0.0
  MODULE CLASS: KernelEvents
  DESCRIPTION:
       Kernel event handling for TerminalX kernel operations

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


class EventType(Enum):
    """Kernel event types"""
    PROCESS_CREATED = "process.created"
    PROCESS_TERMINATED = "process.terminated"
    SYSCALL = "syscall"
    MODULE_LOADED = "module.loaded"
    MODULE_UNLOADED = "module.unloaded"
    SIGNAL = "signal"
    FILE_ACCESS = "file.access"
    NETWORK = "network"
    MEMORY = "memory"
    ERROR = "error"


class KernelEvents:
    """Kernel event handler"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Dict]] = {}
        self.event_history: List[Dict] = []
        self.notification_callback = None
        self.stats = {
            'total_events': 0,
            'events_by_type': {},
        }
        
    def set_notification_callback(self, callback):
        """Set callback for event notifications"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize kernel events"""
        self.config = config or {}
        pass  # No special initialization needed
        
    async def subscribe(self, event: str, callback: Callable, priority: int = 10) -> bool:
        """Subscribe to kernel events"""
        if event not in self.listeners:
            self.listeners[event] = []
            
        self.listeners[event].append({
            'callback': callback,
            'priority': priority,
            'subscribed_at': datetime.now().isoformat(),
        })
        
        # Sort by priority
        self.listeners[event].sort(key=lambda x: x['priority'])
        return True
        
    async def unsubscribe(self, event: str, callback: Callable) -> bool:
        """Unsubscribe from kernel events"""
        if event not in self.listeners:
            return False
            
        self.listeners[event] = [
            listener for listener in self.listeners[event]
            if listener['callback'] != callback
        ]
        return True
            
    async def emit(self, event: str, data: Dict[str, Any]):
        """Emit a kernel event"""
        self.stats['total_events'] += 1
        self.stats['events_by_type'][event] = self.stats['events_by_type'].get(event, 0) + 1
        
        # Add to history
        event_record = {
            'event': event,
            'data': data,
            'timestamp': datetime.now().isoformat(),
       }
        self.event_history.append(event_record)
        
        # Keep only last 1000 events
        if len(self.event_history) > 1000:
            self.event_history = self.event_history[-1000:]
        
        if event not in self.listeners:
            return
            
        for listener in self.listeners[event]:
            try:
                callback = listener['callback']
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                print(f"Event handler error: {e}")
                
    async def emit_process_created(self, pid: int, name: str, parent_pid: int = None):
        """Emit process created event"""
        await self.emit(EventType.PROCESS_CREATED.value, {
            'pid': pid,
            'name': name,
            'parent_pid': parent_pid,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_process_terminated(self, pid: int, exit_code: int, signal: int = None):
        """Emit process terminated event"""
        await self.emit(EventType.PROCESS_TERMINATED.value, {
            'pid': pid,
            'exit_code': exit_code,
            'signal': signal,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_syscall(self, pid: int, syscall: str, args: List, result: Any = None):
        """Emit syscall event"""
        await self.emit(EventType.SYSCALL.value, {
            'pid': pid,
            'syscall': syscall,
            'args': args,
            'result': result,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_module_loaded(self, name: str, path: str = None):
        """Emit module loaded event"""
        await self.emit(EventType.MODULE_LOADED.value, {
            'name': name,
            'path': path,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_module_unloaded(self, name: str):
        """Emit module unloaded event"""
        await self.emit(EventType.MODULE_UNLOADED.value, {
            'name': name,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_signal(self, pid: int, signal: int, sender: int = None):
        """Emit signal event"""
        await self.emit(EventType.SIGNAL.value, {
            'pid': pid,
            'signal': signal,
            'sender': sender,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_file_access(self, pid: int, path: str, mode: str):
        """Emit file access event"""
        await self.emit(EventType.FILE_ACCESS.value, {
            'pid': pid,
            'path': path,
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_network_event(self, pid: int, event_type: str, 
                                 src_addr: str, dst_addr: str, port: int):
        """Emit network event"""
        await self.emit(EventType.NETWORK.value, {
            'pid': pid,
            'event_type': event_type,
            'src_addr': src_addr,
            'dst_addr': dst_addr,
            'port': port,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_memory_event(self, pid: int, event_type: str, 
                               address: int, size: int):
        """Emit memory event"""
        await self.emit(EventType.MEMORY.value, {
            'pid': pid,
            'event_type': event_type,
            'address': address,
            'size': size,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def emit_error(self, source: str, error_type: str, message: str, 
                        severity: str = 'error'):
        """Emit error event"""
        await self.emit(EventType.ERROR.value, {
            'source': source,
            'error_type': error_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
        })
        
    async def get_history(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """Get event history"""
        if event_type:
            return [e for e in self.event_history if e['event'] == event_type][-limit:]
        return self.event_history[-limit:]
        
    async def get_listeners(self, event: str = None) -> Dict[str, int]:
        """Get listener counts"""
        if event:
            return {event: len(self.listeners.get(event, []))}
        return {e: len(listeners) for e, listeners in self.listeners.items()}
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get event statistics"""
        return {
            'total_events': self.stats['total_events'],
            'events_by_type': self.stats['events_by_type'].copy(),
            'total_listeners': sum(len(listeners) for listeners in self.listeners.values()),
            'listeners_by_event': {e: len(listeners) for e, listeners in self.listeners.items()},
            'history_size': len(self.event_history),
        }
        
    async def clear_history(self):
        """Clear event history"""
        self.event_history.clear()
        
    async def enable(self):
        """Enable event handling"""
        pass  # Always enabled
        
    async def disable(self):
        """Disable event handling"""
        self.listeners.clear()
