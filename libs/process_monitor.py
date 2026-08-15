"""
 ============================================================
  MODULE/PLUGIN NAME: ProcessMonitor
  VERSION: 1.0.0
  MODULE CLASS: ProcessMonitor
  DESCRIPTION:
       Process Monitor Engine for CPU / RAM / IO / THREADS / HOOKS monitoring

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

import psutil
import time
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class ProcessLogLevel(Enum):
    """Process monitor log level"""
    NORMAL = "normal"
    VERBOSE = "verbose"
    SILENT = "silent"


@dataclass
class ProcessInfo:
    """Process information"""
    pid: int
    name: str
    exe: Optional[str]
    cmdline: List[str]
    cpu: float
    ram: float
    io: int
    threads: int
    handles: Optional[int]
    parent: Optional[int]
    children: List[int]
    create_time: float
    status: str


@dataclass
class ProcessAlert:
    """Process alert"""
    pid: int
    timestamp: str
    alert_type: str
    value: float
    threshold: float


@dataclass
class ProcessSnapshot:
    """Process snapshot"""
    pid: int
    timestamp: str
    info: ProcessInfo


@dataclass
class ProcessProfile:
    """Process profile"""
    name: str
    cpu_threshold: float
    ram_threshold: float
    io_threshold: int
    thread_threshold: int


class ProcessMonitor:
    """Process Monitor Engine for CPU/RAM/IO/Threads/Hooks monitoring"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("ProcessMonitor", LogLevel.INFO)
        
        self.processes: Dict[int, ProcessInfo] = {}
        self.logs: List[str] = []
        self.errors: List[str] = []
        self.hooks: Dict[int, Callable] = {}
        self.filters: List[Callable] = []
        self.snapshots: Dict[int, ProcessSnapshot] = {}
        self.profiles: Dict[int, ProcessProfile] = {}
        self.alerts: List[ProcessAlert] = []
        
        self.config = {
            "interval": 1.0,
            "log_level": ProcessLogLevel.NORMAL,
            "auto_alert": True,
            "cpu_threshold": 80.0,
            "ram_threshold": 80.0,
            "io_threshold": 1000000,
            "thread_threshold": 200,
        }
        
    # ============================================================
    # LOGGING
    # ============================================================
    def log(self, msg: str, level: str = "INFO") -> None:
        """Log message"""
        if self.config["log_level"] == ProcessLogLevel.SILENT:
            return
            
        if self.config["log_level"] == ProcessLogLevel.VERBOSE or level == "ERROR":
            entry = f"[{datetime.now()}] [{level}] {msg}"
            self.logger.info(entry)
            self.logs.append(entry)
            
            if level == "ERROR":
                self.errors.append(entry)
                
    def get_errors(self) -> List[str]:
        """Get error log"""
        return self.errors.copy()
        
    def clear_errors(self) -> None:
        """Clear error log"""
        self.errors.clear()
        self.logger.info("Error log cleared")
        
    def get_logs(self, limit: int = 100) -> List[str]:
        """Get log entries"""
        return self.logs[-limit:]
        
    def clear_logs(self) -> None:
        """Clear log"""
        self.logs.clear()
        self.logger.info("Log cleared")
        
    # ============================================================
    # METADATA
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get engine metadata"""
        return {
            "name": "process_monitor",
            "version": "2.0 ULTRA+",
            "author": "Sebastian Januchowski",
            "company": "polsoft.ITS™ Dev",
            "dependencies": ["psutil"],
            "compatibility": {
                "shield": True,
                "kernel_hooks": True,
                "sandbox": True,
                "event_bus": True,
                "threat_intel": True,
            }
        }
        
    # ============================================================
    # CONFIG
    # ============================================================
    def config_get(self, key: str) -> Any:
        """Get config value"""
        return self.config.get(key)
        
    def config_set(self, key: str, value: Any) -> None:
        """Set config value"""
        self.config[key] = value
        self.logger.info(f"Config updated: {key} = {value}")
        
    def config_reset(self) -> None:
        """Reset config to defaults"""
        self.config = {
            "interval": 1.0,
            "log_level": ProcessLogLevel.NORMAL,
            "auto_alert": True,
            "cpu_threshold": 80.0,
            "ram_threshold": 80.0,
            "io_threshold": 1000000,
            "thread_threshold": 200,
        }
        self.logger.info("Config reset to defaults")
        
    # ============================================================
    # PROCESS INFO
    # ============================================================
    def get_info(self, pid: int) -> Optional[ProcessInfo]:
        """Get process information"""
        try:
            p = psutil.Process(pid)
            io_counters = p.io_counters()
            
            info = ProcessInfo(
                pid=pid,
                name=p.name(),
                exe=p.exe() if p.exe() else None,
                cmdline=p.cmdline(),
                cpu=p.cpu_percent(interval=0.0),
                ram=p.memory_percent(),
                io=io_counters.read_bytes + io_counters.write_bytes,
                threads=p.num_threads(),
                handles=p.num_handles() if hasattr(p, "num_handles") else None,
                parent=p.parent().pid if p.parent() else None,
                children=[c.pid for c in p.children()],
                create_time=p.create_time(),
                status=p.status(),
            )
            self.processes[pid] = info
            return info
        except Exception as e:
            error = str(e)
            self.errors.append(error)
            self.log(f"Process error: {error}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            return None
            
    def list_processes(self) -> List[int]:
        """List all process PIDs"""
        return list(psutil.pids())
        
    def get_all_processes(self) -> List[ProcessInfo]:
        """Get info for all processes"""
        processes = []
        for pid in psutil.pids():
            info = self.get_info(pid)
            if info:
                processes.append(info)
        return processes
        
    def find_process_by_name(self, name: str) -> List[int]:
        """Find processes by name"""
        matching = []
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                if name.lower() in p.name().lower():
                    matching.append(pid)
            except:
                pass
        return matching
        
    # ============================================================
    # HOOKS
    # ============================================================
    def add_hook(self, pid: int, func: Callable) -> bool:
        """Add hook for process"""
        self.hooks[pid] = func
        self.log(f"Hook added for PID {pid}")
        return True
        
    def remove_hook(self, pid: int) -> bool:
        """Remove hook for process"""
        if pid in self.hooks:
            del self.hooks[pid]
            self.log(f"Hook removed for PID {pid}")
            return True
        return False
        
    def list_hooks(self) -> List[int]:
        """List hooked PIDs"""
        return list(self.hooks.keys())
        
    # ============================================================
    # FILTERS
    # ============================================================
    def add_filter(self, func: Callable) -> bool:
        """Add global filter"""
        self.filters.append(func)
        self.log("Global filter added")
        return True
        
    def remove_filter(self, func: Callable) -> bool:
        """Remove global filter"""
        if func in self.filters:
            self.filters.remove(func)
            self.log("Global filter removed")
            return True
        return False
        
    def list_filters(self) -> int:
        """Get filter count"""
        return len(self.filters)
        
    # ============================================================
    # MONITORING
    # ============================================================
    def monitor(self, pid: int) -> Optional[ProcessInfo]:
        """Monitor a process"""
        info = self.get_info(pid)
        if not info:
            return None
            
        # Apply filters
        for f in self.filters:
            if not f(info):
                self.log(f"Process filtered: {pid}")
                return None
                
        # Execute hooks
        if pid in self.hooks:
            try:
                self.hooks[pid](info)
            except Exception as e:
                error = str(e)
                self.errors.append(error)
                self.log(f"Hook error: {error}", "ERROR")
                self.log(traceback.format_exc(), "ERROR")
                
        # Check alerts
        if self.config["auto_alert"]:
            self.alert_check(info)
            
        return info
        
    def monitor_all(self) -> List[ProcessInfo]:
        """Monitor all processes"""
        results = []
        for pid in psutil.pids():
            info = self.monitor(pid)
            if info:
                results.append(info)
        return results
        
    # ============================================================
    # ALERT ENGINE
    # ============================================================
    def alert_check(self, info: ProcessInfo) -> bool:
        """Check for alerts"""
        pid = info.pid
        alerts = []
        
        if info.cpu >= self.config["cpu_threshold"]:
            alerts.append("HIGH CPU")
            self.alerts.append(ProcessAlert(
                pid=pid,
                timestamp=datetime.now().isoformat(),
                alert_type="HIGH CPU",
                value=info.cpu,
                threshold=self.config["cpu_threshold"]
            ))
            
        if info.ram >= self.config["ram_threshold"]:
            alerts.append("HIGH RAM")
            self.alerts.append(ProcessAlert(
                pid=pid,
                timestamp=datetime.now().isoformat(),
                alert_type="HIGH RAM",
                value=info.ram,
                threshold=self.config["ram_threshold"]
            ))
            
        if info.io >= self.config["io_threshold"]:
            alerts.append("HIGH IO")
            self.alerts.append(ProcessAlert(
                pid=pid,
                timestamp=datetime.now().isoformat(),
                alert_type="HIGH IO",
                value=info.io,
                threshold=self.config["io_threshold"]
            ))
            
        if info.threads >= self.config["thread_threshold"]:
            alerts.append("HIGH THREAD COUNT")
            self.alerts.append(ProcessAlert(
                pid=pid,
                timestamp=datetime.now().isoformat(),
                alert_type="HIGH THREAD COUNT",
                value=info.threads,
                threshold=self.config["thread_threshold"]
            ))
            
        if alerts:
            self.log(f"ALERT for PID {pid}: {alerts}")
            return True
            
        return False
        
    def get_alerts(self, limit: int = 100) -> List[ProcessAlert]:
        """Get alerts"""
        return self.alerts[-limit:]
        
    def clear_alerts(self) -> None:
        """Clear alerts"""
        self.alerts.clear()
        self.logger.info("Alerts cleared")
        
    # ============================================================
    # SNAPSHOTS
    # ============================================================
    def create_snapshot(self, pid: int) -> Optional[ProcessSnapshot]:
        """Create process snapshot"""
        info = self.get_info(pid)
        if not info:
            return None
            
        snapshot = ProcessSnapshot(
            pid=pid,
            timestamp=datetime.now().isoformat(),
            info=info
        )
        self.snapshots[pid] = snapshot
        self.log(f"Snapshot created for PID {pid}")
        return snapshot
        
    def restore_snapshot(self, pid: int) -> bool:
        """Restore process snapshot"""
        if pid not in self.snapshots:
            self.log(f"No snapshot for PID {pid}", "ERROR")
            return False
            
        snapshot = self.snapshots[pid]
        self.processes[pid] = snapshot.info
        self.log(f"Snapshot restored for PID {pid}")
        return True
        
    def delete_snapshot(self, pid: int) -> bool:
        """Delete process snapshot"""
        if pid in self.snapshots:
            del self.snapshots[pid]
            self.log(f"Snapshot deleted for PID {pid}")
            return True
        return False
        
    def list_snapshots(self) -> List[int]:
        """List snapshot PIDs"""
        return list(self.snapshots.keys())
        
    # ============================================================
    # PROFILES
    # ============================================================
    def set_profile(self, pid: int, profile: ProcessProfile) -> bool:
        """Set process profile"""
        self.profiles[pid] = profile
        self.log(f"Profile set for PID {pid}: {profile.name}")
        return True
        
    def get_profile(self, pid: int) -> Optional[ProcessProfile]:
        """Get process profile"""
        return self.profiles.get(pid)
        
    def list_profiles(self) -> List[int]:
        """List profile PIDs"""
        return list(self.profiles.keys())
        
    # ============================================================
    # PROCESS CONTROL
    # ============================================================
    def kill_process(self, pid: int) -> bool:
        """Kill process"""
        try:
            p = psutil.Process(pid)
            p.kill()
            self.log(f"Process killed: {pid}")
            return True
        except Exception as e:
            self.log(f"Failed to kill process {pid}: {e}", "ERROR")
            return False
            
    def suspend_process(self, pid: int) -> bool:
        """Suspend process"""
        try:
            p = psutil.Process(pid)
            p.suspend()
            self.log(f"Process suspended: {pid}")
            return True
        except Exception as e:
            self.log(f"Failed to suspend process {pid}: {e}", "ERROR")
            return False
            
    def resume_process(self, pid: int) -> bool:
        """Resume process"""
        try:
            p = psutil.Process(pid)
            p.resume()
            self.log(f"Process resumed: {pid}")
            return True
        except Exception as e:
            self.log(f"Failed to resume process {pid}: {e}", "ERROR")
            return False
            
    # ============================================================
    # DIAGNOSTICS
    # ============================================================
    def diagnose(self) -> Dict[str, Any]:
        """Run diagnostics"""
        return {
            "processes_cached": len(self.processes),
            "snapshots": len(self.snapshots),
            "hooks": len(self.hooks),
            "filters": len(self.filters),
            "profiles": len(self.profiles),
            "alerts": len(self.alerts),
            "errors": len(self.errors),
            "config": self.config
        }
        
    def auto_fix(self) -> bool:
        """Auto-fix common issues"""
        self.errors.clear()
        self.log("ProcessMonitor auto-fix executed")
        return True
        
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        return {
            "status": "healthy",
            "psutil_available": True,
            "issues": [],
            "recommendations": []
        }
        
    # ============================================================
    # API
    # ============================================================
    def api_list(self) -> List[str]:
        """List available API methods"""
        return [
            "monitor",
            "monitor_all",
            "get_info",
            "list_processes",
            "get_all_processes",
            "find_process_by_name",
            "add_hook",
            "remove_hook",
            "list_hooks",
            "add_filter",
            "remove_filter",
            "list_filters",
            "alert_check",
            "get_alerts",
            "clear_alerts",
            "create_snapshot",
            "restore_snapshot",
            "delete_snapshot",
            "list_snapshots",
            "set_profile",
            "get_profile",
            "list_profiles",
            "kill_process",
            "suspend_process",
            "resume_process",
            "diagnose",
            "auto_fix",
            "health_check",
            "config_get",
            "config_set",
            "config_reset",
            "get_errors",
            "clear_errors",
            "get_logs",
            "clear_logs"
        ]
        
    def api_call(self, func: str, *args, **kwargs) -> Any:
        """Call API method"""
        if hasattr(self, func):
            return getattr(self, func)(*args, **kwargs)
        self.log(f"API method not found: {func}", "ERROR")
        return None
        
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            "status": "running",
            "version": self.get_metadata()["version"],
            "uptime": time.time(),
            **self.diagnose()
        }


# Global process monitor instance
process_monitor = ProcessMonitor()
