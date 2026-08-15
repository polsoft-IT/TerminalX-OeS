"""
 ============================================================
  MODULE/PLUGIN NAME: SystemOptPlugins
  VERSION: 1.0.0
  MODULE CLASS: SystemOptPlugins
  DESCRIPTION:
       Plugin system for SystemOptimizer extensions

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

from typing import Dict, Any
from datetime import datetime


class BasePlugin:
    """Base plugin class for system optimizer"""
    name = "base"

    def __init__(self, engine):
        self.engine = engine

    async def start(self):
        """Called when plugin starts"""
        pass

    async def stop(self):
        """Called when plugin stops"""
        pass


class LoggerPlugin(BasePlugin):
    """Logger plugin for system optimizer - logs all events"""
    name = "logger"

    async def start(self):
        """Subscribe to events"""
        self.engine.event_bus.on("ram_cleaned", self.on_ram)
        self.engine.event_bus.on("cpu_optimized", self.on_cpu)
        self.engine.event_bus.on("process_killed", self.on_kill)
        self.engine.event_bus.on("pagefile_cleaned", self.on_pagefile)
        self.engine.event_bus.on("scan_completed", self.on_scan)

    def on_ram(self, data: Dict[str, Any]):
        """Log RAM cleaning event"""
        print(f"[SystemOpt] RAM Cleaned: {data['freed_mb']} MB freed")

    def on_cpu(self, data: Dict[str, Any]):
        """Log CPU optimization event"""
        print(f"[SystemOpt] CPU Optimized: {data['processes_optimized']} processes")

    def on_kill(self, proc: Dict[str, Any]):
        """Log process kill event"""
        print(f"[SystemOpt] Process Killed: {proc['name']} (PID: {proc['pid']})")

    def on_pagefile(self, data: Dict[str, Any]):
        """Log pagefile cleaning event"""
        print(f"[SystemOpt] Pagefile Cleaned: {data['message']}")

    def on_scan(self, data: Dict[str, Any]):
        """Log scan completion event"""
        print(f"[SystemOpt] Scan Completed: {data['high_resource_count']} high-resource processes")


class StatsPlugin(BasePlugin):
    """Statistics plugin for system optimizer - tracks detailed stats"""
    name = "stats"

    def __init__(self, engine):
        super().__init__(engine)
        self.history = []
        self.max_history = 100

    async def start(self):
        """Subscribe to events"""
        self.engine.event_bus.on("ram_cleaned", self.on_ram)
        self.engine.event_bus.on("cpu_optimized", self.on_cpu)
        self.engine.event_bus.on("process_killed", self.on_kill)
        self.engine.event_bus.on("scan_completed", self.on_scan)

    def on_ram(self, data: Dict[str, Any]):
        """Track RAM cleaning"""
        self.history.append({
            'event': 'ram_cleaned',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()

    def on_cpu(self, data: Dict[str, Any]):
        """Track CPU optimization"""
        self.history.append({
            'event': 'cpu_optimized',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()

    def on_kill(self, proc: Dict[str, Any]):
        """Track process kills"""
        self.history.append({
            'event': 'process_killed',
            'data': proc,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()

    def on_scan(self, data: Dict[str, Any]):
        """Track scans"""
        self.history.append({
            'event': 'scan_completed',
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        self._trim_history()

    def _trim_history(self):
        """Keep history within max size"""
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self, limit: int = 10) -> list:
        """Get recent history"""
        return self.history[-limit:]

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of events"""
        summary = {}
        for item in self.history:
            event = item['event']
            summary[event] = summary.get(event, 0) + 1
        return summary


class AlertPlugin(BasePlugin):
    """Alert plugin for system optimizer - alerts on critical events"""
    name = "alert"

    def __init__(self, engine, alert_callback=None):
        super().__init__(engine)
        self.alert_callback = alert_callback
        self.alerts = []

    async def start(self):
        """Subscribe to events"""
        self.engine.event_bus.on("process_killed", self.on_kill)
        self.engine.event_bus.on("scan_completed", self.on_scan)

    def on_kill(self, proc: Dict[str, Any]):
        """Alert on process kill"""
        alert = {
            'type': 'process_killed',
            'message': f"Process {proc['name']} killed (PID: {proc['pid']})",
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        if self.alert_callback:
            self.alert_callback(alert)

    def on_scan(self, data: Dict[str, Any]):
        """Alert if many high-resource processes found"""
        if data['high_resource_count'] > 5:
            alert = {
                'type': 'high_resource_warning',
                'message': f"High resource processes detected: {data['high_resource_count']}",
                'timestamp': datetime.now().isoformat()
            }
            self.alerts.append(alert)
            if self.alert_callback:
                self.alert_callback(alert)

    def get_alerts(self, limit: int = 10) -> list:
        """Get recent alerts"""
        return self.alerts[-limit:]

    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()


class ThresholdPlugin(BasePlugin):
    """Threshold plugin - custom thresholds for different conditions"""
    name = "threshold"

    def __init__(self, engine, custom_thresholds: Dict[str, Any] = None):
        super().__init__(engine)
        self.custom_thresholds = custom_thresholds or {}

    async def start(self):
        """Subscribe to events"""
        self.engine.event_bus.on("scan_completed", self.on_scan)

    def on_scan(self, data: Dict[str, Any]):
        """Check custom thresholds"""
        # Check memory threshold
        if 'memory_mb' in self.custom_thresholds:
            for proc in data['high_resource']:
                if proc['memory_mb'] > self.custom_thresholds['memory_mb']:
                    print(f"[Threshold] Memory exceeded: {proc['name']} ({proc['memory_mb']} MB)")

        # Check CPU threshold
        if 'cpu_percent' in self.custom_thresholds:
            for proc in data['high_resource']:
                if proc['cpu_percent'] > self.custom_thresholds['cpu_percent']:
                    print(f"[Threshold] CPU exceeded: {proc['name']} ({proc['cpu_percent']}%)")
