"""
Process Monitor - Process monitoring
"""

import asyncio
import psutil
from typing import Dict, Any, List, Optional
from datetime import datetime


class ProcessMonitor:
    """Process monitor"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.monitored_processes: Dict[int, Dict] = {}
        self.history: List[Dict] = []
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize process monitor"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        
    async def start(self):
        """Start monitoring"""
        if not self.enabled:
            return
            
        asyncio.create_task(self._monitor_loop())
        
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.enabled:
            await self._monitor_processes()
            await asyncio.sleep(1)
            
    async def _monitor_processes(self):
        """Monitor all processes"""
        for pid in list(self.monitored_processes.keys()):
            info = await self.get_process_info(pid)
            
            if info is None:
                # Process terminated
                del self.monitored_processes[pid]
            else:
                self.monitored_processes[pid] = info
                
                # Add to history
                self.history.append(info)
                
                # Keep only last 1000 entries per process
                process_history = [
                    h for h in self.history 
                    if h.get('pid') == pid
                ]
                if len(process_history) > 1000:
                    self.history = [
                        h for h in self.history 
                        if h.get('pid') != pid or h not in process_history[:-1000]
                    ]
                    
    async def monitor_process(self, pid: int) -> bool:
        """Start monitoring a process"""
        info = await self.get_process_info(pid)
        
        if info:
            self.monitored_processes[pid] = info
            return True
        return False
        
    async def stop_monitoring(self, pid: int) -> bool:
        """Stop monitoring a process"""
        if pid in self.monitored_processes:
            del self.monitored_processes[pid]
            return True
        return False
        
    async def get_process_info(self, pid: int) -> Optional[Dict]:
        """Get process information"""
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_info': process.memory_info()._asdict(),
                'create_time': process.create_time(),
                'username': process.username(),
                'cmdline': process.cmdline(),
                'cwd': process.cwd(),
                'num_threads': process.num_threads(),
                'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 0,
                'timestamp': datetime.now().isoformat(),
            }
        except psutil.NoSuchProcess:
            return None
            
    async def list_processes(self) -> List[Dict]:
        """List all processes"""
        processes = []
        
        for pid in psutil.pids():
            info = await self.get_process_info(pid)
            if info:
                processes.append(info)
                
        return processes
        
    async def get_monitored_processes(self) -> List[Dict]:
        """Get monitored processes"""
        return list(self.monitored_processes.values())
        
    async def get_process_history(self, pid: int, limit: int = 100) -> List[Dict]:
        """Get process history"""
        history = [
            h for h in self.history 
            if h.get('pid') == pid
        ]
        return history[-limit:]
        
    async def kill_process(self, pid: int) -> bool:
        """Kill a process"""
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except psutil.NoSuchProcess:
            return False
            
    async def suspend_process(self, pid: int) -> bool:
        """Suspend a process"""
        try:
            process = psutil.Process(pid)
            process.suspend()
            return True
        except psutil.NoSuchProcess:
            return False
            
    async def resume_process(self, pid: int) -> bool:
        """Resume a process"""
        try:
            process = psutil.Process(pid)
            process.resume()
            return True
        except psutil.NoSuchProcess:
            return False
