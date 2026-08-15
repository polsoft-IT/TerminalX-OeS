"""
 ============================================================
  MODULE/PLUGIN NAME: SystemOptimizer
  VERSION: 2.0.0
  MODULE CLASS: SystemOptimizer
  DESCRIPTION:
       Advanced RAM/CPU Optimizer for TerminalX with Windows API pagefile flush, working set trim, and system cache flush

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
import os
import asyncio
import gc
import time
import threading
import platform
import ctypes
import ctypes.wintypes as wintypes
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional
from datetime import datetime

from .exceptions import SystemOptError, ProcessKillError, RAMCleanError, CPUOptError, PagefileError


# ============================================================
# WIN32 / NT API DEFINITIONS (Windows only)
# ============================================================

if platform.system() == 'Windows':
    try:
        kernel32 = ctypes.WinDLL("kernel32")
        psapi = ctypes.WinDLL("psapi")
        ntdll = ctypes.WinDLL("ntdll")

        # EmptyWorkingSet
        EmptyWorkingSet = psapi.EmptyWorkingSet
        EmptyWorkingSet.argtypes = [wintypes.HANDLE]
        EmptyWorkingSet.restype = wintypes.BOOL

        # SetProcessWorkingSetSize
        SetProcessWorkingSetSize = kernel32.SetProcessWorkingSetSize
        SetProcessWorkingSetSize.argtypes = [wintypes.HANDLE, ctypes.c_size_t, ctypes.c_size_t]
        SetProcessWorkingSetSize.restype = wintypes.BOOL

        # NtSetSystemInformation
        NtSetSystemInformation = ntdll.NtSetSystemInformation
        NtSetSystemInformation.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong]
        NtSetSystemInformation.restype = ctypes.c_ulong

        SystemMemoryListInformation = 0x50  # undocumented NT API
        WINDOWS_API_AVAILABLE = True
    except:
        WINDOWS_API_AVAILABLE = False
else:
    WINDOWS_API_AVAILABLE = False


# ============================================================
# EVENT BUS
# ============================================================

class EventBus:
    """Event bus for system optimizer events"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def on(self, event: str, callback: Callable):
        """Subscribe to an event"""
        self.listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback: Callable):
        """Unsubscribe from an event"""
        if event in self.listeners:
            self.listeners[event].remove(callback)

    def emit(self, event: str, data: Any = None):
        """Emit an event"""
        for cb in self.listeners.get(event, []):
            try:
                cb(data)
            except Exception as e:
                print(f"[EventBus] Error in callback for event '{event}': {e}")


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class SystemOptConfig:
    """Configuration for system optimizer"""
    ram_threshold_mb: int = 500
    cpu_threshold_percent: int = 80
    scan_interval: float = 3.0
    enable_pagefile_clean: bool = False
    enable_pagefile_flush: bool = True  # v2: Real pagefile flush using NT API
    enable_workingset_trim: bool = True  # v2: Working set trim using Win32
    enable_system_cache_flush: bool = True  # v2: System cache flush using NT API
    enable_priority_opt: bool = True
    enable_auto_kill: bool = False
    enable_cache_flush: bool = True
    max_cache_size: int = 5000
    daemon_enabled: bool = False
    log_level: str = "INFO"


# ============================================================
# CORE ENGINE
# ============================================================

class SystemOptimizer:
    """Advanced RAM/CPU Optimizer with plugin system"""

    def __init__(self, config: Optional[SystemOptConfig] = None):
        self.config = config or SystemOptConfig()
        self.event_bus = EventBus()
        self.plugins: List['BasePlugin'] = []
        self.running = False
        self.daemon_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = {
            'ram_cleaned': 0,
            'cpu_optimized': 0,
            'processes_killed': 0,
            'pagefile_cleaned': 0,
            'scans_performed': 0,
            'errors': 0,
            'start_time': None,
        }

    # ------------------------------------------------------------
    # RAM CLEANER
    # ------------------------------------------------------------
    def clean_ram(self) -> Dict[str, Any]:
        """Clean RAM using Python GC and cache flush"""
        try:
            before = psutil.virtual_memory().available
            before_mb = before / (1024 * 1024)

            # Force garbage collection
            gc.collect()

            # Flush python caches if enabled
            if self.config.enable_cache_flush:
                for obj in gc.get_objects():
                    if isinstance(obj, dict):
                        if len(obj) > self.config.max_cache_size:
                            obj.clear()

            after = psutil.virtual_memory().available
            after_mb = after / (1024 * 1024)
            freed_mb = after_mb - before_mb

            self.stats['ram_cleaned'] += 1

            result = {
                'before_mb': round(before_mb, 2),
                'after_mb': round(after_mb, 2),
                'freed_mb': round(freed_mb, 2),
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("ram_cleaned", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise RAMCleanError(f"RAM cleaning failed: {e}")

    # ------------------------------------------------------------
    # CPU OPTIMIZER
    # ------------------------------------------------------------
    def optimize_cpu(self) -> Dict[str, Any]:
        """Optimize CPU by adjusting process priorities"""
        try:
            optimized = 0
            for proc in psutil.process_iter(['pid', 'cpu_percent', 'name']):
                try:
                    if proc.info['cpu_percent'] > self.config.cpu_threshold_percent:
                        p = psutil.Process(proc.info['pid'])
                        
                        # Set to below normal priority
                        if platform.system() == 'Windows':
                            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        else:
                            p.nice(10)  # Lower priority on Unix
                        
                        optimized += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            self.stats['cpu_optimized'] += 1

            result = {
                'processes_optimized': optimized,
                'threshold': self.config.cpu_threshold_percent,
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("cpu_optimized", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise CPUOptError(f"CPU optimization failed: {e}")

    # ------------------------------------------------------------
    # PAGEFILE CLEANER (Windows only)
    # ------------------------------------------------------------
    def clean_pagefile(self) -> Dict[str, Any]:
        """Clean pagefile (Windows only) - legacy method"""
        if not self.config.enable_pagefile_clean:
            return {'success': False, 'message': 'Pagefile cleaning disabled'}

        if platform.system() != 'Windows':
            return {'success': False, 'message': 'Pagefile cleaning only available on Windows'}

        try:
            # Note: Actual pagefile clearing requires admin privileges
            # This is a symbolic operation for demonstration
            # In production, this would use proper Windows API calls
            
            self.stats['pagefile_cleaned'] += 1

            result = {
                'success': True,
                'message': 'Pagefile clean initiated',
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("pagefile_cleaned", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise PagefileError(f"Pagefile cleaning failed: {e}")

    # ------------------------------------------------------------
    # REAL PAGEFILE FLUSH (NT API) - v2
    # ------------------------------------------------------------
    def flush_pagefile(self) -> Dict[str, Any]:
        """Real pagefile flush using NT API (Windows only)"""
        if not self.config.enable_pagefile_flush:
            return {'success': False, 'message': 'Pagefile flush disabled'}

        if not WINDOWS_API_AVAILABLE:
            return {'success': False, 'message': 'Windows API not available'}

        try:
            # 0 = Flush modified pages
            command = ctypes.c_int(0)
            status = NtSetSystemInformation(
                SystemMemoryListInformation,
                ctypes.byref(command),
                ctypes.sizeof(command)
            )

            self.stats['pagefile_cleaned'] += 1

            result = {
                'success': status == 0,
                'status': status,
                'message': 'Pagefile flush completed' if status == 0 else f'Pagefile flush failed with status {status}',
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("pagefile_flushed", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise PagefileError(f"Pagefile flush failed: {e}")

    # ------------------------------------------------------------
    # WORKING SET TRIM (Win32) - v2
    # ------------------------------------------------------------
    def trim_working_sets(self) -> Dict[str, Any]:
        """Working set trim using Win32 API (Windows only)"""
        if not self.config.enable_workingset_trim:
            return {'success': False, 'message': 'Working set trim disabled'}

        if not WINDOWS_API_AVAILABLE:
            return {'success': False, 'message': 'Windows API not available'}

        try:
            trimmed = 0
            for proc in psutil.process_iter(['pid']):
                try:
                    handle = kernel32.OpenProcess(0x1F0FFF, False, proc.info['pid'])
                    if handle:
                        SetProcessWorkingSetSize(handle, -1, -1)
                        EmptyWorkingSet(handle)
                        kernel32.CloseHandle(handle)
                        trimmed += 1
                except:
                    pass

            result = {
                'success': True,
                'trimmed_count': trimmed,
                'message': f'Trimmed working sets for {trimmed} processes',
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("workingset_trimmed", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise SystemOptError(f"Working set trim failed: {e}")

    # ------------------------------------------------------------
    # SYSTEM CACHE FLUSH (NT API) - v2
    # ------------------------------------------------------------
    def flush_system_cache(self) -> Dict[str, Any]:
        """System cache flush using NT API (Windows only)"""
        if not self.config.enable_system_cache_flush:
            return {'success': False, 'message': 'System cache flush disabled'}

        if not WINDOWS_API_AVAILABLE:
            return {'success': False, 'message': 'Windows API not available'}

        try:
            # 1 = Flush standby list
            command = ctypes.c_int(1)
            status = NtSetSystemInformation(
                SystemMemoryListInformation,
                ctypes.byref(command),
                ctypes.sizeof(command)
            )

            result = {
                'success': status == 0,
                'status': status,
                'message': 'System cache flush completed' if status == 0 else f'System cache flush failed with status {status}',
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("system_cache_flushed", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise SystemOptError(f"System cache flush failed: {e}")

    # ------------------------------------------------------------
    # ENHANCED PYTHON RAM CLEANER - v2
    # ------------------------------------------------------------
    def clean_python_ram(self) -> Dict[str, Any]:
        """Enhanced Python RAM cleaner with detailed reporting"""
        try:
            before = psutil.virtual_memory().available
            before_mb = before / (1024 * 1024)

            # Force garbage collection
            gc.collect()

            # Flush python caches if enabled
            if self.config.enable_cache_flush:
                for obj in gc.get_objects():
                    if isinstance(obj, dict):
                        if len(obj) > self.config.max_cache_size:
                            obj.clear()

            after = psutil.virtual_memory().available
            after_mb = after / (1024 * 1024)
            freed_mb = after_mb - before_mb

            self.stats['ram_cleaned'] += 1

            result = {
                'before_mb': round(before_mb, 2),
                'after_mb': round(after_mb, 2),
                'freed_mb': round(freed_mb, 2),
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("python_ram_cleaned", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise RAMCleanError(f"Python RAM cleaning failed: {e}")

    # ------------------------------------------------------------
    # PROCESS SCANNER
    # ------------------------------------------------------------
    def scan_processes(self, auto_kill: bool = False) -> Dict[str, Any]:
        """Scan processes and optionally kill high-resource ones"""
        try:
            high_resource = []
            killed = []

            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
                try:
                    mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    cpu = proc.info['cpu_percent']

                    if mem_mb > self.config.ram_threshold_mb or cpu > self.config.cpu_threshold_percent:
                        process_info = {
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'memory_mb': round(mem_mb, 2),
                            'cpu_percent': cpu
                        }
                        high_resource.append(process_info)

                        # Auto-kill if enabled
                        if auto_kill or self.config.enable_auto_kill:
                            try:
                                psutil.Process(proc.info['pid']).kill()
                                killed.append(process_info)
                                self.event_bus.emit("process_killed", process_info)
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            self.stats['scans_performed'] += 1
            self.stats['processes_killed'] += len(killed)

            result = {
                'high_resource_count': len(high_resource),
                'killed_count': len(killed),
                'high_resource': high_resource,
                'killed': killed,
                'timestamp': datetime.now().isoformat()
            }

            self.event_bus.emit("scan_completed", result)
            return result

        except Exception as e:
            self.stats['errors'] += 1
            raise SystemOptError(f"Process scan failed: {e}")

    # ------------------------------------------------------------
    # SYSTEM INFO
    # ------------------------------------------------------------
    def get_system_info(self) -> Dict[str, Any]:
        """Get current system resource information"""
        try:
            mem = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.1)

            return {
                'memory': {
                    'total_mb': round(mem.total / (1024 * 1024), 2),
                    'available_mb': round(mem.available / (1024 * 1024), 2),
                    'used_mb': round(mem.used / (1024 * 1024), 2),
                    'percent': mem.percent
                },
                'cpu': {
                    'percent': cpu,
                    'core_count': psutil.cpu_count()
                },
                'process_count': len(psutil.pids()),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise SystemOptError(f"Failed to get system info: {e}")

    # ------------------------------------------------------------
    # PLUGIN HANDLING
    # ------------------------------------------------------------
    def add_plugin(self, plugin: 'BasePlugin'):
        """Add a plugin to the optimizer"""
        self.plugins.append(plugin)

    def remove_plugin(self, plugin_name: str):
        """Remove a plugin by name"""
        self.plugins = [p for p in self.plugins if p.name != plugin_name]

    async def start_plugins(self):
        """Start all plugins"""
        for p in self.plugins:
            try:
                await p.start()
            except Exception as e:
                print(f"[SystemOpt] Failed to start plugin {p.name}: {e}")

    async def stop_plugins(self):
        """Stop all plugins"""
        for p in self.plugins:
            try:
                if hasattr(p, 'stop'):
                    await p.stop()
            except Exception as e:
                print(f"[SystemOpt] Failed to stop plugin {p.name}: {e}")

    # ------------------------------------------------------------
    # DAEMON - v2 Enhanced
    # ------------------------------------------------------------
    async def daemon(self):
        """Main daemon loop for continuous optimization with v2 features"""
        self.running = True
        self.stats['start_time'] = datetime.now().isoformat()

        await self.start_plugins()

        while self.running:
            try:
                # Enhanced Python RAM cleaning
                self.clean_python_ram()

                # Working set trim (v2)
                if self.config.enable_workingset_trim:
                    self.trim_working_sets()

                # System cache flush (v2)
                if self.config.enable_system_cache_flush:
                    self.flush_system_cache()

                # Pagefile flush (v2)
                if self.config.enable_pagefile_flush:
                    self.flush_pagefile()

                # Scan processes
                self.scan_processes(auto_kill=self.config.enable_auto_kill)

                # CPU optimization
                if self.config.enable_priority_opt:
                    self.optimize_cpu()

                # Legacy pagefile clean (if enabled)
                if self.config.enable_pagefile_clean:
                    self.clean_pagefile()

                # Wait for next scan
                await asyncio.sleep(self.config.scan_interval)

            except Exception as e:
                self.stats['errors'] += 1
                print(f"[SystemOpt] Daemon error: {e}")
                await asyncio.sleep(self.config.scan_interval)

    async def start_daemon(self):
        """Start the daemon"""
        if not self.daemon_task or self.daemon_task.done():
            self.daemon_task = asyncio.create_task(self.daemon())

    async def stop_daemon(self):
        """Stop the daemon"""
        self.running = False
        if self.daemon_task:
            self.daemon_task.cancel()
            try:
                await self.daemon_task
            except asyncio.CancelledError:
                pass
        await self.stop_plugins()

    # ------------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------------
    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics"""
        stats = self.stats.copy()
        if stats['start_time']:
            try:
                start = datetime.fromisoformat(stats['start_time'])
                stats['uptime_seconds'] = (datetime.now() - start).total_seconds()
            except:
                pass
        return stats

    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'ram_cleaned': 0,
            'cpu_optimized': 0,
            'processes_killed': 0,
            'pagefile_cleaned': 0,
            'scans_performed': 0,
            'errors': 0,
            'start_time': None,
        }
