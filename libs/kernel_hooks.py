"""
 ============================================================
  MODULE/PLUGIN NAME: KernelHooksEngine
  VERSION: 1.0.0
  MODULE CLASS: KernelHooksEngine
  DESCRIPTION:
       Kernel Hooks Engine for SYS CALLS / EVENTS / TRAPS

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

import time
import json
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class HookMode(Enum):
    """Hook operation mode"""
    MONITOR = "monitor"
    BLOCK = "block"
    ALERT = "alert"


class KernelLogLevel(Enum):
    """Kernel hooks log level"""
    NORMAL = "normal"
    VERBOSE = "verbose"
    SILENT = "silent"


class TrapPolicy(Enum):
    """Trap policy"""
    STRICT = "strict"
    SOFT = "soft"


@dataclass
class HookEvent:
    """Hook event entry"""
    timestamp: str
    syscall: str
    args: tuple
    kwargs: dict
    result: Any
    error: Optional[str] = None


@dataclass
class HookRule:
    """Hook rule"""
    name: str
    condition: Callable
    action: str
    enabled: bool = True


@dataclass
class KernelPlugin:
    """Kernel plugin interface"""
    name: str
    version: str
    
    def on_load(self, engine):
        """Called when plugin is loaded"""
        pass
    
    def run(self, *args, **kwargs):
        """Run plugin"""
        pass


class KernelHooksEngine:
    """Kernel Hooks Engine for system call interception and event handling"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("KernelHooksEngine", LogLevel.INFO)
        
        self.hooks: Dict[str, Callable] = {}       # registered hooks
        self.events: List[HookEvent] = []          # event log
        self.traps: Dict[str, Callable] = {}       # trap handlers
        self.filters: List[Callable] = []          # event filters
        self.rules: List[HookRule] = []             # rule engine
        self.plugins: Dict[str, KernelPlugin] = {}  # plugin registry
        self.snapshots: Dict[str, Any] = {}        # state snapshots
        self.errors: List[str] = []                # error log
        
        self.config = {
            "mode": HookMode.MONITOR,
            "log_level": KernelLogLevel.NORMAL,
            "trap_policy": TrapPolicy.STRICT,
            "max_events": 10000,
            "auto_cleanup": True
        }
        
    # ============================================================
    # METADATA
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get engine metadata"""
        return {
            "name": "kernel_hooks",
            "version": "2.0",
            "author": "Sebastian Januchowski",
            "company": "polsoft.ITS™ Dev",
            "dependencies": [],
            "compatibility": {
                "shield": True,
                "sandbox": True,
                "ids_ips": True
            }
        }
        
    # ============================================================
    # LOGGING
    # ============================================================
    def log(self, msg: str, level: str = "INFO") -> None:
        """Log message"""
        if self.config["log_level"] == KernelLogLevel.SILENT:
            return
            
        if self.config["log_level"] == KernelLogLevel.VERBOSE or level == "ERROR":
            entry = f"[{datetime.now()}] [{level}] {msg}"
            self.logger.info(entry)
            
            if level == "ERROR":
                self.errors.append(entry)
                
    def get_errors(self) -> List[str]:
        """Get error log"""
        return self.errors.copy()
        
    def clear_errors(self) -> None:
        """Clear error log"""
        self.errors.clear()
        self.logger.info("Error log cleared")
        
    def get_events(self, limit: int = 100) -> List[HookEvent]:
        """Get event log"""
        return self.events[-limit:]
        
    def clear_events(self) -> None:
        """Clear event log"""
        self.events.clear()
        self.logger.info("Event log cleared")
        
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
            "mode": HookMode.MONITOR,
            "log_level": KernelLogLevel.NORMAL,
            "trap_policy": TrapPolicy.STRICT,
            "max_events": 10000,
            "auto_cleanup": True
        }
        self.logger.info("Config reset to defaults")
        
    # ============================================================
    # HOOKS
    # ============================================================
    def register_hook(self, syscall: str, handler: Callable) -> bool:
        """Register syscall hook"""
        self.hooks[syscall] = handler
        self.log(f"Hook registered: {syscall}")
        return True
        
    def unregister_hook(self, syscall: str) -> bool:
        """Unregister syscall hook"""
        if syscall in self.hooks:
            del self.hooks[syscall]
            self.log(f"Hook removed: {syscall}")
            return True
        return False
        
    def list_hooks(self) -> List[str]:
        """List all registered hooks"""
        return list(self.hooks.keys())
        
    def trigger_syscall(self, syscall: str, *args, **kwargs) -> Any:
        """Trigger syscall with hooks"""
        self.log(f"Syscall triggered: {syscall}")
        
        event = HookEvent(
            timestamp=datetime.now().isoformat(),
            syscall=syscall,
            args=args,
            kwargs=kwargs,
            result=None
        )
        
        # Apply filters
        for f in self.filters:
            if not f(syscall, args, kwargs):
                self.log(f"Filtered syscall: {syscall}")
                return None
                
        # Apply rules
        if self.evaluate_rules(syscall, args, kwargs):
            self.log(f"Rule matched for syscall: {syscall}")
            
        # Activate traps
        if syscall in self.traps:
            self.log(f"Trap activated: {syscall}")
            try:
                result = self.traps[syscall](syscall, args, kwargs)
                event.result = result
                self.events.append(event)
                self._cleanup_events()
                return result
            except Exception as e:
                error = str(e)
                event.error = error
                self.errors.append(error)
                self.log(f"Trap error: {error}", "ERROR")
                self.log(traceback.format_exc(), "ERROR")
                return None
                
        # Execute hooks
        if syscall in self.hooks:
            try:
                result = self.hooks[syscall](*args, **kwargs)
                event.result = result
                self.events.append(event)
                self._cleanup_events()
                return result
            except Exception as e:
                error = str(e)
                event.error = error
                self.errors.append(error)
                self.log(f"Hook error: {error}", "ERROR")
                self.log(traceback.format_exc(), "ERROR")
                return None
                
        self.events.append(event)
        self._cleanup_events()
        return None
        
    def _cleanup_events(self) -> None:
        """Cleanup old events if auto_cleanup is enabled"""
        if self.config.get("auto_cleanup", False):
            max_events = self.config.get("max_events", 10000)
            if len(self.events) > max_events:
                self.events = self.events[-max_events:]
                
    # ============================================================
    # TRAPS
    # ============================================================
    def register_trap(self, syscall: str, handler: Callable) -> bool:
        """Register syscall trap"""
        self.traps[syscall] = handler
        self.log(f"Trap registered: {syscall}")
        return True
        
    def unregister_trap(self, syscall: str) -> bool:
        """Unregister syscall trap"""
        if syscall in self.traps:
            del self.traps[syscall]
            self.log(f"Trap removed: {syscall}")
            return True
        return False
        
    def list_traps(self) -> List[str]:
        """List all registered traps"""
        return list(self.traps.keys())
        
    # ============================================================
    # FILTERS
    # ============================================================
    def add_filter(self, func: Callable) -> bool:
        """Add event filter"""
        self.filters.append(func)
        self.log("Filter added")
        return True
        
    def remove_filter(self, func: Callable) -> bool:
        """Remove event filter"""
        if func in self.filters:
            self.filters.remove(func)
            self.log("Filter removed")
            return True
        return False
        
    def list_filters(self) -> int:
        """Get filter count"""
        return len(self.filters)
        
    # ============================================================
    # RULE ENGINE
    # ============================================================
    def add_rule(self, name: str, condition: Callable, action: str = "log") -> bool:
        """Add hook rule"""
        rule = HookRule(name=name, condition=condition, action=action)
        self.rules.append(rule)
        self.log(f"Rule added: {name}")
        return True
        
    def remove_rule(self, name: str) -> bool:
        """Remove hook rule"""
        for i, rule in enumerate(self.rules):
            if rule.name == name:
                del self.rules[i]
                self.log(f"Rule removed: {name}")
                return True
        return False
        
    def enable_rule(self, name: str) -> bool:
        """Enable rule"""
        for rule in self.rules:
            if rule.name == name:
                rule.enabled = True
                self.log(f"Rule enabled: {name}")
                return True
        return False
        
    def disable_rule(self, name: str) -> bool:
        """Disable rule"""
        for rule in self.rules:
            if rule.name == name:
                rule.enabled = False
                self.log(f"Rule disabled: {name}")
                return True
        return False
        
    def list_rules(self) -> List[Dict[str, Any]]:
        """List all rules"""
        return [
            {
                "name": rule.name,
                "action": rule.action,
                "enabled": rule.enabled
            }
            for rule in self.rules
        ]
        
    def evaluate_rules(self, syscall: str, args: tuple, kwargs: dict) -> bool:
        """Evaluate rules against syscall"""
        for rule in self.rules:
            if rule.enabled and rule.condition(syscall, args, kwargs):
                self.log(f"Rule triggered: {rule.name}")
                return True
        return False
        
    # ============================================================
    # PLUGINS
    # ============================================================
    def load_plugin(self, plugin: KernelPlugin) -> bool:
        """Load kernel plugin"""
        self.plugins[plugin.name] = plugin
        plugin.on_load(self)
        self.log(f"Plugin loaded: {plugin.name}")
        return True
        
    def unload_plugin(self, name: str) -> bool:
        """Unload kernel plugin"""
        if name in self.plugins:
            del self.plugins[name]
            self.log(f"Plugin unloaded: {name}")
            return True
        return False
        
    def list_plugins(self) -> List[str]:
        """List loaded plugins"""
        return list(self.plugins.keys())
        
    def run_plugin(self, name: str, *args, **kwargs) -> Any:
        """Run plugin"""
        if name not in self.plugins:
            self.log(f"Plugin not found: {name}", "ERROR")
            return None
        return self.plugins[name].run(*args, **kwargs)
        
    # ============================================================
    # SNAPSHOTS
    # ============================================================
    def create_snapshot(self, name: str) -> bool:
        """Create state snapshot"""
        self.snapshots[name] = {
            "timestamp": datetime.now().isoformat(),
            "hooks": list(self.hooks.keys()),
            "traps": list(self.traps.keys()),
            "filters": len(self.filters),
            "rules": [r.name for r in self.rules],
            "config": self.config.copy()
        }
        self.log(f"Snapshot created: {name}")
        return True
        
    def restore_snapshot(self, name: str) -> bool:
        """Restore state snapshot"""
        if name not in self.snapshots:
            self.log(f"Snapshot not found: {name}", "ERROR")
            return False
            
        snapshot = self.snapshots[name]
        self.config = snapshot.get("config", self.config)
        self.log(f"Snapshot restored: {name}")
        return True
        
    def delete_snapshot(self, name: str) -> bool:
        """Delete snapshot"""
        if name in self.snapshots:
            del self.snapshots[name]
            self.log(f"Snapshot deleted: {name}")
            return True
        return False
        
    def list_snapshots(self) -> List[str]:
        """List snapshots"""
        return list(self.snapshots.keys())
        
    def export_state(self) -> Dict[str, Any]:
        """Export current state"""
        return {
            "hooks": list(self.hooks.keys()),
            "traps": list(self.traps.keys()),
            "filters": len(self.filters),
            "rules": [r.name for r in self.rules],
            "plugins": list(self.plugins.keys()),
            "config": self.config,
            "events_count": len(self.events),
            "errors_count": len(self.errors)
        }
        
    def import_state(self, state: Dict[str, Any]) -> bool:
        """Import state"""
        self.config = state.get("config", self.config)
        self.logger.info("KernelHooks state imported")
        return True
        
    # ============================================================
    # DIAGNOSTICS
    # ============================================================
    def diagnose(self) -> Dict[str, Any]:
        """Run diagnostics"""
        return {
            "hooks": len(self.hooks),
            "traps": len(self.traps),
            "filters": len(self.filters),
            "rules": len(self.rules),
            "plugins": len(self.plugins),
            "events": len(self.events),
            "errors": len(self.errors),
            "snapshots": len(self.snapshots),
            "config": self.config
        }
        
    def auto_fix(self) -> bool:
        """Auto-fix common issues"""
        self.errors.clear()
        if len(self.events) > self.config.get("max_events", 10000):
            self.events = self.events[-self.config["max_events"]:]
        self.logger.info("KernelHooks auto-fix executed")
        return True
        
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        return {
            "status": "healthy",
            "issues": [],
            "recommendations": []
        }
        
    # ============================================================
    # API
    # ============================================================
    def api_list(self) -> List[str]:
        """List available API methods"""
        return [
            "register_hook",
            "unregister_hook",
            "list_hooks",
            "trigger_syscall",
            "register_trap",
            "unregister_trap",
            "list_traps",
            "add_filter",
            "remove_filter",
            "list_filters",
            "add_rule",
            "remove_rule",
            "enable_rule",
            "disable_rule",
            "list_rules",
            "load_plugin",
            "unload_plugin",
            "list_plugins",
            "run_plugin",
            "create_snapshot",
            "restore_snapshot",
            "delete_snapshot",
            "list_snapshots",
            "export_state",
            "import_state",
            "diagnose",
            "auto_fix",
            "health_check",
            "config_get",
            "config_set",
            "config_reset",
            "get_errors",
            "clear_errors",
            "get_events",
            "clear_events"
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


# Global kernel hooks engine instance
kernel_hooks_engine = KernelHooksEngine()
