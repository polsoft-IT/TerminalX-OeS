"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkHooks
  VERSION: 1.0.0
  MODULE CLASS: NetworkHooks
  DESCRIPTION:
       Hook system for network operations in TerminalX

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

from typing import Dict, Callable, List, Any


class NetworkHooks:
    """Network operation hooks"""
    
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {}
        
    def register(self, hook_name: str, callback: Callable, priority: int = 10):
        """Register a hook"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
            
        self.hooks[hook_name].append({
            'callback': callback,
            'priority': priority,
        })
        
        # Sort by priority
        self.hooks[hook_name].sort(key=lambda x: x['priority'])
        
    def unregister(self, hook_name: str, callback: Callable):
        """Unregister a hook"""
        if hook_name in self.hooks:
            self.hooks[hook_name] = [
                h for h in self.hooks[hook_name]
                if h['callback'] != callback
            ]
            
    async def execute(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute hooks"""
        if hook_name not in self.hooks:
            return []
            
        results = []
        
        for hook in self.hooks[hook_name]:
            try:
                callback = hook['callback']
                
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(*args, **kwargs)
                else:
                    result = callback(*args, **kwargs)
                    
                results.append(result)
                
            except Exception as e:
                print(f"Hook error in {hook_name}: {e}")
                
        return results
        
    async def before_connect(self, host: str, port: int) -> bool:
        """Execute before connect hooks"""
        results = await self.execute('before_connect', host, port)
        return all(results) if results else True
        
    async def after_connect(self, connection_id: str):
        """Execute after connect hooks"""
        await self.execute('after_connect', connection_id)
        
    async def before_send(self, connection_id: str, data: bytes) -> bytes:
        """Execute before send hooks"""
        results = await self.execute('before_send', connection_id, data)
        return results[-1] if results else data
        
    async def after_receive(self, connection_id: str, data: bytes) -> bytes:
        """Execute after receive hooks"""
        results = await self.execute('after_receive', connection_id, data)
        return results[-1] if results else data
