"""
Process Hooks - Hook system for process operations
"""

from typing import Dict, Callable, List, Any


class ProcessHooks:
    """Process operation hooks"""
    
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
        
    async def before_process_create(self, name: str, args: List) -> bool:
        """Execute before process create hooks"""
        results = await self.execute('before_process_create', name, args)
        return all(results) if results else True
        
    async def after_process_create(self, pid: int):
        """Execute after process create hooks"""
        await self.execute('after_process_create', pid)
        
    async def before_process_kill(self, pid: int) -> bool:
        """Execute before process kill hooks"""
        results = await self.execute('before_process_kill', pid)
        return all(results) if results else True
        
    async def after_process_kill(self, pid: int):
        """Execute after process kill hooks"""
        await self.execute('after_process_kill', pid)
