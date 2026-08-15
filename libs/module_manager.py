"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleManager
  VERSION: 1.0.0
  MODULE CLASS: ModuleManager
  DESCRIPTION:
       Advanced Multi-Module Control Engine for TerminalX

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

import importlib
import traceback
import json
import os
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class ModuleLogLevel(Enum):
    """Module manager log level"""
    NORMAL = "normal"
    VERBOSE = "verbose"
    SILENT = "silent"


@dataclass
class ModuleMetadata:
    """Module metadata"""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    compatibility: Dict[str, str] = field(default_factory=dict)
    api_methods: List[str] = field(default_factory=list)
    plugins: List[str] = field(default_factory=list)


@dataclass
class ModuleSnapshot:
    """Module snapshot"""
    name: str
    module_name: str
    timestamp: str
    state: Dict[str, Any]


@dataclass
class ModuleProfile:
    """Module profile"""
    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    priority: int = 0


class ModuleManager:
    """
    ADVANCED MULTI-MODULE CONTROL ENGINE:
    - Module loading/unloading/reloading
    - Module status monitoring
    - Module snapshots
    - Module configuration
    - Module diagnostics
    - Dependency management
    - Compatibility checking
    - Plugin management
    - API access
    - Profile management
    - Export/Import
    - Auto-diagnose/auto-fix
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("ModuleManager", LogLevel.INFO)
        self.modules = {}          # loaded modules
        self.metadata = {}         # module metadata
        self.snapshots = {}        # module state snapshots
        self.logs = []             # global manager logs
        self.profiles = {}         # module profiles
        self.auto_mode = True      # auto-diagnose / auto-fix
        self.thread = None         # monitoring thread
        self.enabled = True        # manager enabled state
        self.version_callback = None  # callback for version updates

        # config
        self.config = {
            "log_level": ModuleLogLevel.NORMAL,
            "auto_mode": True,
            "auto_reload": False,
            "auto_fix": True,
            "check_interval": 5.0,
        }

        # statistics
        self.stats = {
            "modules_loaded": 0,
            "modules_unloaded": 0,
            "modules_reloaded": 0,
            "snapshots_created": 0,
            "snapshots_restored": 0,
            "errors_fixed": 0,
        }

    # ============================================================
    # VERSION CALLBACK
    # ============================================================
    def set_version_callback(self, callback):
        """Set callback for version updates when module count changes"""
        self.version_callback = callback

    def _notify_version_update(self):
        """Notify version callback of module count change"""
        if self.version_callback:
            module_count = len(self.modules)
            self.version_callback(module_count)

    # ============================================================
    # LOGGING
    # ============================================================
    def log(self, msg: str, level: str = "INFO") -> None:
        """Log message"""
        entry = f"[{datetime.now()}] [{level}] {msg}"
        self.logs.append(entry)
        
        if self.config["log_level"] != ModuleLogLevel.SILENT:
            if self.config["log_level"] == ModuleLogLevel.VERBOSE or level == "ERROR":
                self.logger.info(entry)

    def get_logs(self) -> List[str]:
        """Get logs"""
        return self.logs.copy()

    def clear_logs(self) -> None:
        """Clear logs"""
        self.logs.clear()

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
            "log_level": ModuleLogLevel.NORMAL,
            "auto_mode": True,
            "auto_reload": False,
            "auto_fix": True,
            "check_interval": 5.0,
        }
        self.logger.info("Config reset to defaults")

    # ============================================================
    # MODULE LOADING
    # ============================================================
    def load_module(self, name: str, path: Optional[str] = None) -> bool:
        """Load module"""
        try:
            if path:
                # Load from custom path
                spec = importlib.util.spec_from_file_location(name, path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                else:
                    self.log(f"Failed to load module from path: {path}", "ERROR")
                    return False
            else:
                # Load from modules package
                mod = importlib.import_module(f"modules.{name}")
            
            if hasattr(mod, "register"):
                engine = mod.register(self)
                self.modules[name] = engine
                self.metadata[name] = self._extract_metadata(engine)
                self.stats["modules_loaded"] += 1
                self.log(f"Module loaded: {name}")
                self._notify_version_update()
                return True
            else:
                self.log(f"Module {name} has no register()", "ERROR")
                return False
        except Exception as e:
            self.log(f"Error loading module {name}: {e}", "ERROR")
            self.log(traceback.format_exc(), "ERROR")
            return False

    def unload_module(self, name: str) -> bool:
        """Unload module"""
        if name in self.modules:
            del self.modules[name]
            if name in self.metadata:
                del self.metadata[name]
            self.stats["modules_unloaded"] += 1
            self.log(f"Module unloaded: {name}")
            self._notify_version_update()
            return True
        self.log(f"Module not loaded: {name}", "ERROR")
        return False

    def reload_module(self, name: str) -> bool:
        """Reload module"""
        if name in self.modules:
            self.unload_module(name)
            result = self.load_module(name)
            if result:
                self.stats["modules_reloaded"] += 1
            return result
        self.log(f"Cannot reload module that is not loaded: {name}", "ERROR")
        return False

    def list_modules(self) -> List[str]:
        """List loaded modules"""
        return list(self.modules.keys())

    def get_module(self, name: str) -> Optional[Any]:
        """Get module instance"""
        return self.modules.get(name)

    # ============================================================
    # MODULE STATUS
    # ============================================================
    def status(self, name: str) -> Dict[str, Any]:
        """Get module status"""
        if name not in self.modules:
            return {"status": "not_loaded"}
        engine = self.modules[name]
        result = {
            "status": "loaded",
            "metadata": self.metadata.get(name, {}),
        }
        
        # Try to get additional info if available
        if hasattr(engine, "get_resources"):
            result["resources"] = engine.get_resources()
        if hasattr(engine, "get_errors"):
            result["errors"] = engine.get_errors()
        if hasattr(engine, "get_stats"):
            result["stats"] = engine.get_stats()
            
        return result

    def status_all(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all modules"""
        return {name: self.status(name) for name in self.modules}

    # ============================================================
    # MODULE SNAPSHOTS
    # ============================================================
    def snapshot(self, name: str) -> Optional[Dict[str, Any]]:
        """Create module snapshot"""
        if name not in self.modules:
            self.log(f"Cannot snapshot module that is not loaded: {name}", "ERROR")
            return None
        engine = self.modules[name]
        
        if hasattr(engine, "export_state"):
            snap = engine.export_state()
        else:
            snap = {"state": "basic_snapshot"}
        
        snapshot = ModuleSnapshot(
            name=f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            module_name=name,
            timestamp=str(datetime.now()),
            state=snap
        )
        self.snapshots[snapshot.name] = snapshot
        self.stats["snapshots_created"] += 1
        self.log(f"Snapshot created for module: {name}")
        return snapshot.state

    def restore_snapshot(self, snapshot_name: str) -> bool:
        """Restore module snapshot"""
        if snapshot_name not in self.snapshots:
            self.log(f"Snapshot not found: {snapshot_name}", "ERROR")
            return False
        
        snapshot = self.snapshots[snapshot_name]
        module_name = snapshot.module_name
        
        if module_name not in self.modules:
            self.log(f"Module not loaded: {module_name}", "ERROR")
            return False
        
        engine = self.modules[module_name]
        if hasattr(engine, "import_state"):
            engine.import_state(snapshot.state)
        else:
            self.log(f"Module does not support state import", "ERROR")
            return False
        
        self.stats["snapshots_restored"] += 1
        self.log(f"Snapshot restored for module: {module_name}")
        return True

    def delete_snapshot(self, snapshot_name: str) -> bool:
        """Delete snapshot"""
        if snapshot_name in self.snapshots:
            del self.snapshots[snapshot_name]
            self.log(f"Snapshot deleted: {snapshot_name}")
            return True
        return False

    def list_snapshots(self) -> List[str]:
        """List snapshots"""
        return list(self.snapshots.keys())

    # ============================================================
    # MODULE CONFIG
    # ============================================================
    def module_config_get(self, name: str, key: str) -> Any:
        """Get module config value"""
        if name not in self.modules:
            return None
        engine = self.modules[name]
        if hasattr(engine, "config_get"):
            return engine.config_get(key)
        return None

    def module_config_set(self, name: str, key: str, value: Any) -> bool:
        """Set module config value"""
        if name not in self.modules:
            return False
        engine = self.modules[name]
        if hasattr(engine, "config_set"):
            engine.config_set(key, value)
            self.log(f"Config updated: {name}.{key} = {value}")
            return True
        return False

    # ============================================================
    # MODULE DIAGNOSTICS
    # ============================================================
    def diagnose(self, name: str) -> Optional[Dict[str, Any]]:
        """Diagnose module"""
        if name not in self.modules:
            return None
        engine = self.modules[name]
        if hasattr(engine, "diagnose"):
            diag = engine.diagnose()
            self.log(f"Diagnostics for {name}: {diag}")
            return diag
        return {"status": "diagnostics_not_supported"}

    def diagnose_all(self) -> Dict[str, Dict[str, Any]]:
        """Diagnose all modules"""
        return {name: self.diagnose(name) for name in self.modules}

    def auto_fix(self, name: str) -> bool:
        """Auto-fix module"""
        if name not in self.modules:
            return False
        engine = self.modules[name]
        if hasattr(engine, "auto_fix"):
            result = engine.auto_fix()
            if result:
                self.stats["errors_fixed"] += 1
            self.log(f"Auto-fix for {name}: {result}")
            return result
        return False

    def auto_fix_all(self) -> Dict[str, bool]:
        """Auto-fix all modules"""
        return {name: self.auto_fix(name) for name in self.modules}

    # ============================================================
    # MODULE DEPENDENCIES
    # ============================================================
    def dependencies(self, name: str) -> List[str]:
        """Get module dependencies"""
        if name not in self.metadata:
            return []
        return self.metadata[name].get("dependencies", [])

    def check_dependencies(self, name: str) -> List[str]:
        """Check module dependencies"""
        deps = self.dependencies(name)
        missing = [d for d in deps if d not in self.modules]
        if missing:
            self.log(f"Missing dependencies for {name}: {missing}", "ERROR")
        return missing

    def check_all_dependencies(self) -> Dict[str, List[str]]:
        """Check all module dependencies"""
        return {name: self.check_dependencies(name) for name in self.modules}

    # ============================================================
    # MODULE COMPATIBILITY
    # ============================================================
    def compatibility(self, name: str) -> Dict[str, str]:
        """Get module compatibility"""
        if name not in self.metadata:
            return {}
        return self.metadata[name].get("compatibility", {})

    def check_compatibility(self, name: str, version: str) -> bool:
        """Check module compatibility with version"""
        compat = self.compatibility(name)
        min_version = compat.get("min_version")
        max_version = compat.get("max_version")
        
        if min_version and version < min_version:
            return False
        if max_version and version > max_version:
            return False
        return True

    # ============================================================
    # MODULE PLUGINS
    # ============================================================
    def plugin_list(self, name: str) -> List[str]:
        """List module plugins"""
        if name not in self.modules:
            return []
        engine = self.modules[name]
        if hasattr(engine, "plugin_list"):
            return engine.plugin_list()
        return []

    def plugin_run(self, name: str, plugin: str, *args, **kwargs) -> Any:
        """Run module plugin"""
        if name not in self.modules:
            return None
        engine = self.modules[name]
        if hasattr(engine, "plugin_run"):
            return engine.plugin_run(plugin, *args, **kwargs)
        return None

    # ============================================================
    # MODULE API
    # ============================================================
    def api_list(self, name: str) -> List[str]:
        """List module API methods"""
        if name not in self.modules:
            return []
        engine = self.modules[name]
        if hasattr(engine, "api_list"):
            return engine.api_list()
        return []

    def api_call(self, name: str, func: str, *args, **kwargs) -> Any:
        """Call module API method"""
        if name not in self.modules:
            return None
        engine = self.modules[name]
        if hasattr(engine, "api_call"):
            return engine.api_call(func, *args, **kwargs)
        return None

    # ============================================================
    # MODULE PROFILES
    # ============================================================
    def profile_set(self, name: str, profile: ModuleProfile) -> None:
        """Set module profile"""
        self.profiles[name] = profile
        self.log(f"Profile set for {name}: {profile.name}")

    def profile_get(self, name: str) -> Optional[ModuleProfile]:
        """Get module profile"""
        return self.profiles.get(name)

    def profile_delete(self, name: str) -> bool:
        """Delete module profile"""
        if name in self.profiles:
            del self.profiles[name]
            self.log(f"Profile deleted for {name}")
            return True
        return False

    def profile_apply(self, name: str) -> bool:
        """Apply profile to module"""
        profile = self.profile_get(name)
        if not profile:
            return False
        
        if name not in self.modules:
            return False
        
        for key, value in profile.config.items():
            self.module_config_set(name, key, value)
        
        self.log(f"Profile applied to {name}")
        return True

    # ============================================================
    # EXPORT / IMPORT
    # ============================================================
    def export_all(self, path: str = "module_manager_export.json") -> str:
        """Export all module manager data"""
        data = {
            "metadata": self._serialize_metadata(),
            "snapshots": self._serialize_snapshots(),
            "profiles": self._serialize_profiles(),
            "config": self.config,
            "stats": self.stats,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        self.log(f"Module manager exported to {path}")
        return path

    def import_all(self, path: str) -> bool:
        """Import module manager data"""
        if not os.path.exists(path):
            self.log(f"Import file not found: {path}", "ERROR")
            return False
        try:
            with open(path, "r") as f:
                data = json.load(f)
            self.metadata = data.get("metadata", {})
            self.snapshots = data.get("snapshots", {})
            self.profiles = data.get("profiles", {})
            self.config = data.get("config", self.config)
            self.stats = data.get("stats", self.stats)
            self.log("Module manager imported")
            return True
        except Exception as e:
            self.log(f"Error importing: {e}", "ERROR")
            return False

    # ============================================================
    # REALTIME MONITORING
    # ============================================================
    def _monitor_loop(self) -> None:
        """Monitoring loop"""
        while self.enabled:
            time.sleep(self.config["check_interval"])
            if self.config["auto_mode"]:
                self._auto_check()

    def _auto_check(self) -> None:
        """Auto-check modules"""
        for name in self.modules:
            if self.config["auto_fix"]:
                self.auto_fix(name)

    def start(self) -> None:
        """Start module manager"""
        self.enabled = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        self.log("Module manager started")

    def stop(self) -> None:
        """Stop module manager"""
        self.enabled = False
        self.log("Module manager stopped")

    # ============================================================
    # METADATA
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get module manager metadata"""
        return {
            "name": "ModuleManager",
            "version": "2.0-ULTRA",
            "author": "Sebastian Januchowski",
            "company": "polsoft.ITS™ Dev",
            "description": "Advanced Multi-Module Control Engine",
            "dependencies": [],
            "compatibility": {
                "min_version": "2.5.0",
                "max_version": "3.0.0",
            },
            "api_methods": self.api_list_all(),
            "plugins": [],
        }

    def _extract_metadata(self, engine: Any) -> Dict[str, Any]:
        """Extract metadata from module"""
        if hasattr(engine, "get_metadata"):
            return engine.get_metadata()
        return {
            "name": "unknown",
            "version": "2.5.0",
            "author": "unknown",
            "description": "No description",
            "dependencies": [],
            "compatibility": {},
            "api_methods": [],
            "plugins": [],
        }

    def _serialize_metadata(self) -> Dict[str, Any]:
        """Serialize metadata for export"""
        return self.metadata

    def _serialize_snapshots(self) -> Dict[str, Any]:
        """Serialize snapshots for export"""
        return {
            name: {
                "module_name": snap.module_name,
                "timestamp": snap.timestamp,
                "state": snap.state,
            }
            for name, snap in self.snapshots.items()
        }

    def _serialize_profiles(self) -> Dict[str, Any]:
        """Serialize profiles for export"""
        return {
            name: {
                "name": profile.name,
                "config": profile.config,
                "enabled": profile.enabled,
                "priority": profile.priority,
            }
            for name, profile in self.profiles.items()
        }

    # ============================================================
    # STATISTICS
    # ============================================================
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics"""
        return {
            "status": "running" if self.enabled else "stopped",
            "modules_loaded": len(self.modules),
            "snapshots_count": len(self.snapshots),
            "profiles_count": len(self.profiles),
            "logs_count": len(self.logs),
            "stats": self.stats,
        }

    # ============================================================
    # DIAGNOSTICS
    # ============================================================
    def manager_diagnose(self) -> Dict[str, Any]:
        """Run manager diagnostics"""
        return {
            "enabled": self.enabled,
            "thread_alive": self.thread.is_alive() if self.thread else False,
            "auto_mode": self.config["auto_mode"],
            "auto_fix": self.config["auto_fix"],
            "modules_count": len(self.modules),
            "snapshots_count": len(self.snapshots),
            "profiles_count": len(self.profiles),
        }

    def health_check(self) -> Dict[str, Any]:
        """Run health check"""
        diag = self.manager_diagnose()
        healthy = all([
            diag["enabled"],
            diag["thread_alive"] if self.thread else True,
        ])
        return {
            "status": "healthy" if healthy else "unhealthy",
            "details": diag,
        }

    # ============================================================
    # API
    # ============================================================
    def api_list_all(self) -> List[str]:
        """List all available API methods"""
        return [
            "log", "get_logs", "clear_logs",
            "config_get", "config_set", "config_reset",
            "load_module", "unload_module", "reload_module",
            "list_modules", "get_module",
            "status", "status_all",
            "snapshot", "restore_snapshot", "delete_snapshot", "list_snapshots",
            "module_config_get", "module_config_set",
            "diagnose", "diagnose_all", "auto_fix", "auto_fix_all",
            "dependencies", "check_dependencies", "check_all_dependencies",
            "compatibility", "check_compatibility",
            "plugin_list", "plugin_run",
            "api_list", "api_call",
            "profile_set", "profile_get", "profile_delete", "profile_apply",
            "export_all", "import_all",
            "start", "stop",
            "get_stats", "manager_diagnose", "health_check",
        ]

    def api_call_manager(self, method: str, *args, **kwargs) -> Any:
        """Call manager API method"""
        if method in self.api_list_all():
            return getattr(self, method)(*args, **kwargs)
        return None


# Global instance
module_manager = ModuleManager()
