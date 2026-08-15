"""
 ============================================================
  MODULE/PLUGIN NAME: KernelMonitor
  VERSION: 1.0.0
  MODULE CLASS: KernelMonitor
  DESCRIPTION:
       Kernel monitoring and statistics for TerminalX kernel operations

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
import psutil
import platform
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class MetricType(Enum):
    """Metric types"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    PROCESS = "process"
    SYSTEM = "system"


class AlertLevel(Enum):
    """Alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class KernelMonitor:
    """Kernel monitoring"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.stats: Dict[str, Any] = {}
        self.history: List[Dict] = []
        self.alerts: List[Dict] = []
        self.monitoring_tasks: List[asyncio.Task] = []
        self.notification_callback = None
        self.thresholds: Dict[str, Dict] = {}
        self.kernel_version = platform.release()
        self.system_info: Dict[str, Any] = {}
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize kernel monitor"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.thresholds = self.config.get('thresholds', {})
        
        # Collect system info once
        await self._collect_system_info()
        
    def set_notification_callback(self, callback):
        """Set callback for kernel notifications"""
        self.notification_callback = callback
        
    async def start(self):
        """Start monitoring"""
        if not self.enabled:
            return
            
        task = asyncio.create_task(self._monitor_loop())
        self.monitoring_tasks.append(task)
        
    async def stop(self):
        """Stop monitoring"""
        for task in self.monitoring_tasks:
            task.cancel()
        self.monitoring_tasks.clear()
        
    async def _monitor_loop(self):
        """Main monitoring loop"""
        interval = self.config.get('monitoring_interval', 1)
        while self.enabled:
            try:
                await self._collect_stats()
                await self._check_thresholds()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in monitor loop: {e}")
                
    async def _collect_system_info(self):
        """Collect static system information"""
        try:
            self.system_info = {
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total if platform.system() != 'Windows' else psutil.disk_usage('C:\\').total,
                'boot_time': psutil.boot_time(),
            }
        except Exception as e:
            print(f"Error collecting system info: {e}")
            
    async def _collect_stats(self):
        """Collect kernel statistics"""
        try:
            # Get disk usage based on OS
            if platform.system() == 'Windows':
                disk_usage = psutil.disk_usage('C:\\')
            else:
                disk_usage = psutil.disk_usage('/')
            
            # Network stats
            net_io = psutil.net_io_counters()
            
            self.stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'cpu_per_core': psutil.cpu_percent(interval=0.1, percpu=True),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available': psutil.virtual_memory().available,
                'memory_used': psutil.virtual_memory().used,
                'disk_usage': disk_usage.percent,
                'disk_free': disk_usage.free,
                'disk_used': disk_usage.used,
                'boot_time': psutil.boot_time(),
                'process_count': len(psutil.pids()),
                'network_bytes_sent': net_io.bytes_sent,
                'network_bytes_recv': net_io.bytes_recv,
                'network_packets_sent': net_io.packets_sent,
                'network_packets_recv': net_io.packets_recv,
            }
            
            self.history.append(self.stats)
            
            # Keep only last 1000 entries
            if len(self.history) > 1000:
                self.history = self.history[-1000:]
                
        except Exception as e:
            print(f"Error collecting stats: {e}")
            
    async def _check_thresholds(self):
        """Check if any thresholds are exceeded"""
        alerts = []
        
        # Check CPU threshold
        if 'cpu_percent' in self.thresholds:
            threshold = self.thresholds['cpu_percent']
            if self.stats['cpu_percent'] > threshold.get('max', 100):
                alerts.append({
                    'metric': 'cpu_percent',
                    'value': self.stats['cpu_percent'],
                    'threshold': threshold['max'],
                    'level': AlertLevel.WARNING.value if threshold.get('severity') == 'warning' else AlertLevel.CRITICAL.value,
                })
                
        # Check memory threshold
        if 'memory_percent' in self.thresholds:
            threshold = self.thresholds['memory_percent']
            if self.stats['memory_percent'] > threshold.get('max', 100):
                alerts.append({
                    'metric': 'memory_percent',
                    'value': self.stats['memory_percent'],
                    'threshold': threshold['max'],
                    'level': AlertLevel.WARNING.value if threshold.get('severity') == 'warning' else AlertLevel.CRITICAL.value,
                })
                
        # Check disk threshold
        if 'disk_usage' in self.thresholds:
            threshold = self.thresholds['disk_usage']
            if self.stats['disk_usage'] > threshold.get('max', 100):
                alerts.append({
                    'metric': 'disk_usage',
                    'value': self.stats['disk_usage'],
                    'threshold': threshold['max'],
                    'level': AlertLevel.WARNING.value if threshold.get('severity') == 'warning' else AlertLevel.CRITICAL.value,
                })
                
        # Send notifications for alerts
        for alert in alerts:
            alert['timestamp'] = datetime.now().isoformat()
            self.alerts.append(alert)
            
            if self.notification_callback:
                await self.notification_callback(
                    f"Kernel alert: {alert['metric']} exceeded threshold",
                    f"Value: {alert['value']}%, Threshold: {alert['threshold']}%",
                    'system',
                    alert['level']
                )
            
    async def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return self.stats.copy()
        
    async def get_history(self, limit: int = 100) -> List[Dict]:
        """Get historical statistics"""
        return self.history[-limit:]
        
    async def get_process_info(self, pid: int) -> Optional[Dict]:
        """Get process information"""
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_percent': process.memory_percent(),
                'memory_info': process.memory_info()._asdict(),
                'create_time': process.create_time(),
                'username': process.username(),
                'num_threads': process.num_threads(),
                'num_handles': process.num_handles() if platform.system() == 'Windows' else None,
                'exe': process.exe(),
                'cmdline': process.cmdline(),
                'cwd': process.cwd(),
            }
        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied:
            return {'pid': pid, 'error': 'Access denied'}
            
    async def list_processes(self, limit: int = None) -> List[Dict]:
        """List all processes"""
        processes = []
        
        for pid in psutil.pids():
            info = await self.get_process_info(pid)
            if info and 'error' not in info:
                processes.append(info)
                
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        if limit:
            processes = processes[:limit]
                
        return processes
        
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return self.system_info.copy()
        
    async def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        try:
            net_io = psutil.net_io_counters()
            net_connections = psutil.net_connections(kind='inet')
            
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout,
                'connections_count': len(net_connections),
            }
        except Exception as e:
            return {'error': str(e)}
            
    async def get_disk_stats(self) -> Dict[str, Any]:
        """Get disk statistics"""
        try:
            if platform.system() == 'Windows':
                disk_usage = psutil.disk_usage('C:\\')
            else:
                disk_usage = psutil.disk_usage('/')
                
            disk_io = psutil.disk_io_counters()
            
            return {
                'total': disk_usage.total,
                'used': disk_usage.used,
                'free': disk_usage.free,
                'percent': disk_usage.percent,
                'read_bytes': disk_io.read_bytes if disk_io else 0,
                'write_bytes': disk_io.write_bytes if disk_io else 0,
                'read_count': disk_io.read_count if disk_io else 0,
                'write_count': disk_io.write_count if disk_io else 0,
            }
        except Exception as e:
            return {'error': str(e)}
            
    async def get_cpu_stats(self) -> Dict[str, Any]:
        """Get CPU statistics"""
        try:
            cpu_times = psutil.cpu_times()
            cpu_freq = psutil.cpu_freq()
            
            return {
                'percent': psutil.cpu_percent(interval=0.1),
                'per_core': psutil.cpu_percent(interval=0.1, percpu=True),
                'times': cpu_times._asdict(),
                'freq': cpu_freq._asdict() if cpu_freq else None,
                'count': psutil.cpu_count(),
                'count_logical': psutil.cpu_count(logical=True),
            }
        except Exception as e:
            return {'error': str(e)}
            
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': mem.total,
                'available': mem.available,
                'used': mem.used,
                'free': mem.free,
                'percent': mem.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_free': swap.free,
                'swap_percent': swap.percent,
            }
        except Exception as e:
            return {'error': str(e)}
            
    async def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get kernel alerts"""
        return self.alerts[-limit:]
        
    async def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        
    async def set_threshold(self, metric: str, max_val: float = None, severity: str = 'warning'):
        """Set threshold for metric"""
        self.thresholds[metric] = {
            'max': max_val,
            'severity': severity,
        }
        
    async def remove_threshold(self, metric: str) -> bool:
        """Remove threshold for metric"""
        if metric in self.thresholds:
            del self.thresholds[metric]
            return True
        return False
        
    async def enable(self):
        """Enable kernel monitor"""
        self.enabled = True
        
    async def disable(self):
        """Disable kernel monitor"""
        self.enabled = False
        await self.stop()
        
    async def get_stats_summary(self) -> Dict[str, Any]:
        """Get summary of all statistics"""
        return {
            'system': await self.get_system_info(),
            'cpu': await self.get_cpu_stats(),
            'memory': await self.get_memory_stats(),
            'disk': await self.get_disk_stats(),
            'network': await self.get_network_stats(),
            'current': self.stats,
        }
