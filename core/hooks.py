"""
Hooks - Hook system for extending functionality
"""

from typing import Dict, Callable, List, Any


class Hooks:
    """Hook system for extending functionality"""
    
    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {}
        
    def register(self, hook_name: str, callback: Callable, priority: int = 10):
        """Register a hook callback"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
            
        self.hooks[hook_name].append({
            'callback': callback,
            'priority': priority,
        })
        
        # Sort by priority (lower = higher priority)
        self.hooks[hook_name].sort(key=lambda x: x['priority'])
        
    def unregister(self, hook_name: str, callback: Callable):
        """Unregister a hook callback"""
        if hook_name in self.hooks:
            self.hooks[hook_name] = [
                h for h in self.hooks[hook_name] 
                if h['callback'] != callback
            ]
            
    async def execute(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute all callbacks for a hook"""
        if hook_name not in self.hooks:
            return None
            
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
        
    def get_hooks(self, hook_name: str) -> List[Callable]:
        """Get all callbacks for a hook"""
        return [h['callback'] for h in self.hooks.get(hook_name, [])]
