"""
Multi-Task Engine GODMODE — ALL-IN-ONE
Advanced task scheduling with CFS, IPC, and priority support
"""

import asyncio
import concurrent.futures
import time
import os
import threading
from queue import PriorityQueue, Queue
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class TaskPriority(Enum):
    """Task priority levels"""
    HIGH = 0
    MEDIUM = 1
    LOW = 2


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Task object with priority and runtime tracking"""
    
    def __init__(self, name: str, func: Callable, priority: TaskPriority = TaskPriority.MEDIUM, 
                 *args, **kwargs):
        self.name = name
        self.func = func
        self.priority = priority
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
        self.vruntime = 0  # CFS virtual runtime
        self.status = TaskStatus.PENDING
        self.cyclic = False  # Whether task should repeat
        self.interval = 0  # Interval for cyclic tasks
        
    def runtime(self) -> Optional[float]:
        """Get task runtime"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
        
    def __lt__(self, other):
        # Compare by virtual runtime (CFS)
        return self.vruntime < other.vruntime


class MessageBus:
    """IPC Message Bus for inter-task communication"""
    
    def __init__(self):
        self.channels: Dict[str, Queue] = {}
        self.notification_callback = None
        
    def set_notification_callback(self, callback):
        """Set callback for message notifications"""
        self.notification_callback = callback
        
    def create_channel(self, name: str):
        """Create a new message channel"""
        if name not in self.channels:
            self.channels[name] = Queue()
            
    def send(self, channel: str, msg: Any) -> bool:
        """Send message to channel"""
        if channel in self.channels:
            self.channels[channel].put(msg)
            return True
        return False
        
    def recv(self, channel: str, timeout: float = None) -> Optional[Any]:
        """Receive message from channel"""
        if channel in self.channels:
            try:
                return self.channels[channel].get(timeout=timeout)
            except:
                return None
        return None
        
    def channel_size(self, channel: str) -> int:
        """Get channel queue size"""
        if channel in self.channels:
            return self.channels[channel].qsize()
        return 0


class Pipe:
    """IPC Pipe (bidirectional)"""
    
    def __init__(self):
        self.a = Queue()
        self.b = Queue()
        
    def send_a(self, msg: Any):
        """Send to endpoint A"""
        self.a.put(msg)
        
    def send_b(self, msg: Any):
        """Send to endpoint B"""
        self.b.put(msg)
        
    def recv_a(self, timeout: float = None) -> Optional[Any]:
        """Receive from endpoint A"""
        try:
            return self.a.get(timeout=timeout)
        except:
            return None
            
    def recv_b(self, timeout: float = None) -> Optional[Any]:
        """Receive from endpoint B"""
        try:
            return self.b.get(timeout=timeout)
        except:
            return None


class SharedBlock:
    """IPC Shared Memory with Semaphores and Mutexes"""
    
    def __init__(self, size: int):
        try:
            from multiprocessing import shared_memory, Semaphore, Lock
            self.shm = shared_memory.SharedMemory(create=True, size=size)
            self.sem = Semaphore(1)
            self.mutex = Lock()
            self.size = size
            self.using_multiprocessing = True
        except ImportError:
            # Fallback for systems without multiprocessing support
            self.shm = bytearray(size)
            self.sem = None
            self.mutex = None
            self.size = size
            self.using_multiprocessing = False
            
    def write(self, data: bytes) -> bool:
        """Write data to shared memory"""
        try:
            if self.using_multiprocessing:
                with self.mutex:
                    self.sem.acquire()
                    self.shm.buf[:len(data)] = data
                    self.sem.release()
            else:
                self.shm[:len(data)] = data
            return True
        except Exception:
            return False
            
    def read(self) -> bytes:
        """Read data from shared memory"""
        try:
            if self.using_multiprocessing:
                with self.mutex:
                    self.sem.acquire()
                    data = bytes(self.shm.buf[:self.size])
                    self.sem.release()
            else:
                data = bytes(self.shm)
            return data
        except Exception:
            return b""
            
    def close(self):
        """Close shared memory"""
        if self.using_multiprocessing:
            try:
                self.shm.close()
                self.shm.unlink()
            except:
                pass


class MultiTaskEngine:
    """Multi-Task Engine with CFS scheduling and IPC support"""
    
    def __init__(self, max_workers: int = 8, time_slice: float = 0.002):
        self.loop = asyncio.new_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        self.task_queue = PriorityQueue()
        self.running = False
        self.results: Dict[str, Task] = {}
        self.bus = MessageBus()
        self.time_slice = time_slice
        self.max_workers = max_workers
        self.notification_callback = None
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_runtime': 0,
        }
        self.task_history: List[Dict] = []
        
    def set_notification_callback(self, callback):
        """Set callback for task notifications"""
        self.notification_callback = callback
        self.bus.set_notification_callback(callback)
        
    def add(self, name: str, func: Callable, priority: TaskPriority = TaskPriority.MEDIUM, 
            *args, **kwargs) -> Task:
        """Add task to queue"""
        task = Task(name, func, priority, *args, **kwargs)
        self.task_queue.put(task)
        self.stats['total_tasks'] += 1
        return task
        
    def add_cyclic(self, name: str, func: Callable, interval: float, 
                   priority: TaskPriority = TaskPriority.MEDIUM, *args, **kwargs) -> Task:
        """Add cyclic (repeating) task"""
        task = Task(name, func, priority, *args, **kwargs)
        task.cyclic = True
        task.interval = interval
        self.task_queue.put(task)
        self.stats['total_tasks'] += 1
        return task
        
    def _run_thread(self, task: Task) -> Task:
        """Run task in thread"""
        try:
            task.status = TaskStatus.RUNNING
            task.start_time = time.time()
            
            # Execute task
            task.result = task.func(*task.args, **task.kwargs)
            
            task.end_time = time.time()
            task.vruntime += (task.end_time - task.start_time)
            task.status = TaskStatus.COMPLETED
            self.stats['completed_tasks'] += 1
            self.stats['total_runtime'] += task.runtime()
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            self.stats['failed_tasks'] += 1
            
        return task
        
    async def _async_run(self, task: Task) -> Task:
        """Async wrapper for task execution"""
        return await self.loop.run_in_executor(self.executor, self._run_thread, task)
        
    async def scheduler(self):
        """CFS scheduler with priority and time-slice"""
        while self.running:
            if not self.task_queue.empty():
                task = self.task_queue.get()
                
                # Priority-based delay
                if task.priority == TaskPriority.LOW:
                    await asyncio.sleep(0.001)
                elif task.priority == TaskPriority.HIGH:
                    pass  # No delay for high priority
                    
                # Execute task
                result = await self._async_run(task)
                self.results[task.name] = result
                
                # Add to history
                self.task_history.append({
                    'name': task.name,
                    'status': task.status.value,
                    'runtime': task.runtime(),
                    'priority': task.priority.value,
                    'timestamp': datetime.now().isoformat(),
                })
                
                # Keep only last 1000 entries
                if len(self.task_history) > 1000:
                    self.task_history = self.task_history[-1000:]
                
                # Re-add cyclic tasks
                if task.cyclic and task.status == TaskStatus.COMPLETED:
                    await asyncio.sleep(task.interval)
                    self.task_queue.put(task)
                    
                # Send notification for failed tasks
                if task.status == TaskStatus.FAILED and self.notification_callback:
                    await self.notification_callback(
                        f"Task failed: {task.name}",
                        f"Error: {task.error}",
                        'task',
                        'high'
                    )
                    
            await asyncio.sleep(self.time_slice)
            
    def start(self):
        """Start the multi-task engine"""
        self.running = True
        thread = threading.Thread(
            target=self.loop.run_until_complete,
            args=(self.scheduler(),),
            daemon=True
        )
        thread.start()
        
    def stop(self):
        """Stop the multi-task engine"""
        self.running = False
        time.sleep(0.05)
        self.executor.shutdown(wait=False)
        self.process_pool.shutdown(wait=False)
        
    def get(self, name: str) -> Optional[Task]:
        """Get task result by name"""
        return self.results.get(name, None)
        
    def cancel(self, name: str) -> bool:
        """Cancel a task"""
        if name in self.results:
            self.results[name].status = TaskStatus.CANCELLED
            return True
        return False
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            'running': self.running,
            'total_tasks': self.stats['total_tasks'],
            'completed_tasks': self.stats['completed_tasks'],
            'failed_tasks': self.stats['failed_tasks'],
            'total_runtime': self.stats['total_runtime'],
            'queue_size': self.task_queue.qsize(),
            'max_workers': self.max_workers,
            'history_size': len(self.task_history),
        }
        
    async def get_history(self, limit: int = 100) -> List[Dict]:
        """Get task history"""
        return self.task_history[-limit:]
        
    async def clear_history(self):
        """Clear task history"""
        self.task_history.clear()
        
    async def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_runtime': 0,
        }
