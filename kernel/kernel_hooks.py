"""
 ============================================================
  MODULE/PLUGIN NAME: KernelHooks
  VERSION: 1.0.0
  MODULE CLASS: KernelHooks
  DESCRIPTION:
       Hook system for kernel operations in TerminalX

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
from typing import Dict, Callable, List, Any, Optional
from datetime import datetime
from enum import Enum


class HookType(Enum):
    """Hook types"""
    BEFORE_SYSCALL = "before_syscall"
    AFTER_SYSCALL = "after_syscall"
    BEFORE_PROCESS_CREATE = "before_process_create"
    AFTER_PROCESS_CREATE = "after_process_create"
    BEFORE_PROCESS_TERMINATE = "before_process_terminate"
    AFTER_PROCESS_TERMINATE = "after_process_terminate"
    BEFORE_FILE_OPEN = "before_file_open"
    AFTER_FILE_OPEN = "after_file_open"
    BEFORE_NETWORK_CONNECT = "before_network_connect"
    AFTER_NETWORK_CONNECT = "after_network_connect"
    MEMORY_ALLOCATE = "memory_allocate"
    MEMORY_FREE = "memory_free"


class KernelHooks:
    """Kernel operation hooks"""
    
    def __init__(self):
        self.hooks: Dict[str, List[Dict]] = {}
        self.hook_stats: Dict[str, Dict] = {}
        self.notification_callback = None
        
    def set_notification_callback(self, callback):
        """Set callback for hook notifications"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize kernel hooks"""
        self.config = config or {}
        pass  # No special initialization needed
        
    def register(self, hook_name: str, callback: Callable, priority: int = 10, 
                description: str = "") -> bool:
        """Register a hook"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
            self.hook_stats[hook_name] = {
                'total_executions': 0,
                'total_errors': 0,
                'last_execution': None,
            }
            
        self.hooks[hook_name].append({
            'callback': callback,
            'priority': priority,
            'description': description,
            'registered_at': datetime.now().isoformat(),
        })
        
        # Sort by priority (lower number = higher priority)
        self.hooks[hook_name].sort(key=lambda x: x['priority'])
        return True
        
    def unregister(self, hook_name: str, callback: Callable) -> bool:
        """Unregister a hook"""
        if hook_name not in self.hooks:
            return False
            
        original_count = len(self.hooks[hook_name])
        self.hooks[hook_name] = [
            h for h in self.hooks[hook_name]
            if h['callback'] != callback
        ]
        
        return len(self.hooks[hook_name]) < original_count
            
    async def execute(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute hooks"""
        if hook_name not in self.hooks:
            return []
            
        results = []
        self.hook_stats[hook_name]['total_executions'] += 1
        self.hook_stats[hook_name]['last_execution'] = datetime.now().isoformat()
        
        for hook in self.hooks[hook_name]:
            try:
                callback = hook['callback']
                
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(*args, **kwargs)
                else:
                    result = callback(*args, **kwargs)
                    
                results.append({
                    'result': result,
                    'description': hook.get('description', ''),
                    'priority': hook['priority'],
                })
                
            except Exception as e:
                self.hook_stats[hook_name]['total_errors'] += 1
                results.append({
                    'error': str(e),
                    'description': hook.get('description', ''),
                    'priority': hook['priority'],
                })
                
        return results
        
    async def before_syscall(self, pid: int, syscall: str, args: List) -> bool:
        """Execute before syscall hooks"""
        results = await self.execute(HookType.BEFORE_SYSCALL.value, pid, syscall, args)
        # If any hook returns False or raises an error, block the syscall
        for result in results:
            if 'error' in result:
                continue
            if result['result'] is False:
                return False
        return True
        
    async def after_syscall(self, pid: int, syscall: str, result: Any):
        """Execute after syscall hooks"""
        await self.execute(HookType.AFTER_SYSCALL.value, pid, syscall, result)
        
    async def before_process_create(self, name: str, args: List) -> bool:
        """Execute before process create hooks"""
        results = await self.execute(HookType.BEFORE_PROCESS_CREATE.value, name, args)
        for result in results:
            if 'error' in result:
                continue
            if result['result'] is False:
                return False
        return True
        
    async def after_process_create(self, pid: int):
        """Execute after process create hooks"""
        await self.execute(HookType.AFTER_PROCESS_CREATE.value, pid)
        
    async def before_process_terminate(self, pid: int, signal: int = None) -> bool:
        """Execute before process terminate hooks"""
        results = await self.execute(HookType.BEFORE_PROCESS_TERMINATE.value, pid, signal)
        for result in results:
            if 'error' in result:
                continue
            if result['result'] is False:
                return False
        return True
        
    async def after_process_terminate(self, pid: int, exit_code: int):
        """Execute after process terminate hooks"""
        await self.execute(HookType.AFTER_PROCESS_TERMINATE.value, pid, exit_code)
        
    async def before_file_open(self, pid: int, path: str, flags: int) -> bool:
        """Execute before file open hooks"""
        results = await self.execute(HookType.BEFORE_FILE_OPEN.value, pid, path, flags)
        for result in results:
            if 'error' in result:
                continue
            if result['result'] is False:
                return False
        return True
        
    async def after_file_open(self, pid: int, path: str, fd: int):
        """Execute after file open hooks"""
        await self.execute(HookType.AFTER_FILE_OPEN.value, pid, path, fd)
        
    async def before_network_connect(self, pid: int, addr: str, port: int) -> bool:
        """Execute before network connect hooks"""
        results = await self.execute(HookType.BEFORE_NETWORK_CONNECT.value, pid, addr, port)
        for result in results:
            if 'error' in result:
                continue
            if result['result'] is False:
                return False
        return True
        
    async def after_network_connect(self, pid: int, addr: str, port: int, success: bool):
        """Execute after network connect hooks"""
        await self.execute(HookType.AFTER_NETWORK_CONNECT.value, pid, addr, port, success)
        
    async def on_memory_allocate(self, pid: int, size: int, address: int):
        """Execute memory allocate hooks"""
        await self.execute(HookType.MEMORY_ALLOCATE.value, pid, size, address)
        
    async def on_memory_free(self, pid: int, address: int, size: int):
        """Execute memory free hooks"""
        await self.execute(HookType.MEMORY_FREE.value, pid, address, size)
        
    async def list_hooks(self, hook_name: str = None) -> Dict[str, List[Dict]]:
        """List registered hooks"""
        if hook_name:
            if hook_name in self.hooks:
                return {
                    hook_name: [
                        {
                            'priority': h['priority'],
                            'description': h.get('description', ''),
                            'registered_at': h['registered_at'],
                        }
                        for h in self.hooks[hook_name]
                    ]
                }
            return {}
            
        return {
            name: [
                {
                    'priority': h['priority'],
                    'description': h.get('description', ''),
                    'registered_at': h['registered_at'],
                }
                for h in hooks
            ]
            for name, hooks in self.hooks.items()
        }
        
    async def get_stats(self, hook_name: str = None) -> Dict[str, Dict]:
        """Get hook statistics"""
        if hook_name:
            if hook_name in self.hook_stats:
                return {hook_name: self.hook_stats[hook_name].copy()}
            return {}
        return self.hook_stats.copy()
        
    async def clear_hooks(self, hook_name: str = None) -> bool:
        """Clear hooks"""
        if hook_name:
            if hook_name in self.hooks:
                del self.hooks[hook_name]
                del self.hook_stats[hook_name]
                return True
            return False
        self.hooks.clear()
        self.hook_stats.clear()
        return True
