"""
Scheduler - Task scheduling system
"""

import asyncio
from typing import Callable, Any, Dict
from datetime import datetime, timedelta


class Scheduler:
    """Task scheduler"""
    
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.scheduled_tasks: Dict[str, Dict] = {}
        self.running = False
        
    async def initialize(self):
        """Initialize scheduler"""
        self.running = True
        
    async def start(self):
        """Start scheduler"""
        self.running = True
        asyncio.create_task(self._run_scheduled_tasks())
        
    async def stop(self):
        """Stop scheduler"""
        self.running = False
        
        # Cancel all tasks
        for task in self.tasks.values():
            task.cancel()
            
        self.tasks.clear()
        
    async def schedule(self, name: str, func: Callable, interval: float = None, 
                      delay: float = None):
        """Schedule a task"""
        task_info = {
            'func': func,
            'interval': interval,
            'delay': delay,
            'last_run': None,
        }
        
        self.scheduled_tasks[name] = task_info
        
    async def schedule_once(self, name: str, func: Callable, delay: float):
        """Schedule a one-time task"""
        async def wrapper():
            await asyncio.sleep(delay)
            await func()
            del self.scheduled_tasks[name]
            
        self.scheduled_tasks[name] = {
            'func': wrapper,
            'interval': None,
            'delay': delay,
            'last_run': None,
        }
        
    async def _run_scheduled_tasks(self):
        """Run scheduled tasks"""
        while self.running:
            for name, task_info in list(self.scheduled_tasks.items()):
                func = task_info['func']
                interval = task_info['interval']
                last_run = task_info['last_run']
                
                should_run = False
                
                if interval is not None:
                    if last_run is None:
                        should_run = True
                    else:
                        elapsed = (datetime.now() - last_run).total_seconds()
                        if elapsed >= interval:
                            should_run = True
                else:
                    # One-time task with delay
                    if last_run is None:
                        should_run = True
                        
                if should_run:
                    try:
                        if asyncio.iscoroutinefunction(func):
                            await func()
                        else:
                            func()
                        task_info['last_run'] = datetime.now()
                    except Exception as e:
                        print(f"Error in scheduled task {name}: {e}")
                        
            await asyncio.sleep(0.1)
