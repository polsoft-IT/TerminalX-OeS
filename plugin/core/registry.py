"""
 ============================================================
  MODULE/PLUGIN NAME: PluginRegistry
  VERSION: 1.0.0
  MODULE CLASS: PluginRegistry
  DESCRIPTION:
       Plugin registration system for TerminalX plugin system

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
# ============================================================

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from libs.clean_logger import CleanLogger, LogLevel
from plugin.core.loader import PluginInfo


@dataclass
class PluginRegistryEntry:
    """Plugin registry entry"""
    name: str
    version: str
    author: str
    description: str
    installed_at: str
    last_updated: str
    enabled: bool = True
    permissions: Dict[str, bool] = None
    hooks: List[str] = None
    events: List[str] = None
    path: Optional[str] = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = {}
        if self.hooks is None:
            self.hooks = []
        if self.events is None:
            self.events = []


class PluginRegistry:
    """
    PLUGIN REGISTRY SYSTEM:
    - Register plugins
    - Unregister plugins
    - Query plugins
    - Persist registry to disk
    - Load registry from disk
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginRegistry", LogLevel.INFO)
        self.registry: Dict[str, PluginRegistryEntry] = {}
        self.registry_file = "plugin/manifest/registry.json"

    # ============================================================
    # REGISTRATION
    # ============================================================
    def register(self, plugin_info: PluginInfo) -> bool:
        """Register plugin in registry"""
        try:
            entry = PluginRegistryEntry(
                name=plugin_info.name,
                version=plugin_info.version,
                author=plugin_info.author,
                description=plugin_info.description,
                installed_at=str(datetime.now()),
                last_updated=str(datetime.now()),
                enabled=plugin_info.enabled,
                permissions=plugin_info.permissions,
                hooks=plugin_info.hooks,
                events=plugin_info.events,
                path=plugin_info.path
            )

            self.registry[plugin_info.name] = entry
            self.logger.info(f"Plugin registered: {plugin_info.name}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering plugin: {e}")
            return False

    def unregister(self, name: str) -> bool:
        """Unregister plugin from registry"""
        if name in self.registry:
            del self.registry[name]
            self.logger.info(f"Plugin unregistered: {name}")
            return True
        self.logger.error(f"Plugin not in registry: {name}")
        return False

    def update(self, name: str, plugin_info: PluginInfo) -> bool:
        """Update plugin in registry"""
        if name not in self.registry:
            self.logger.error(f"Plugin not in registry: {name}")
            return False

        try:
            entry = self.registry[name]
            entry.version = plugin_info.version
            entry.last_updated = str(datetime.now())
            entry.permissions = plugin_info.permissions
            entry.hooks = plugin_info.hooks
            entry.events = plugin_info.events
            entry.path = plugin_info.path

            self.logger.info(f"Plugin updated: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating plugin: {e}")
            return False

    # ============================================================
    # QUERIES
    # ============================================================
    def get(self, name: str) -> Optional[PluginRegistryEntry]:
        """Get plugin from registry"""
        return self.registry.get(name)

    def list_all(self) -> List[PluginRegistryEntry]:
        """List all plugins in registry"""
        return list(self.registry.values())

    def list_enabled(self) -> List[PluginRegistryEntry]:
        """List enabled plugins"""
        return [entry for entry in self.registry.values() if entry.enabled]

    def list_disabled(self) -> List[PluginRegistryEntry]:
        """List disabled plugins"""
        return [entry for entry in self.registry.values() if not entry.enabled]

    def exists(self, name: str) -> bool:
        """Check if plugin exists in registry"""
        return name in self.registry

    def is_enabled(self, name: str) -> bool:
        """Check if plugin is enabled"""
        entry = self.get(name)
        return entry.enabled if entry else False

    # ============================================================
    # ENABLE/DISABLE
    # ============================================================
    def enable(self, name: str) -> bool:
        """Enable plugin"""
        if name in self.registry:
            self.registry[name].enabled = True
            self.logger.info(f"Plugin enabled in registry: {name}")
            return True
        return False

    def disable(self, name: str) -> bool:
        """Disable plugin"""
        if name in self.registry:
            self.registry[name].enabled = False
            self.logger.info(f"Plugin disabled in registry: {name}")
            return True
        return False

    # ============================================================
    # PERMISSIONS
    # ============================================================
    def get_permissions(self, name: str) -> Dict[str, bool]:
        """Get plugin permissions"""
        entry = self.get(name)
        return entry.permissions if entry else {}

    def has_permission(self, name: str, permission: str) -> bool:
        """Check if plugin has permission"""
        permissions = self.get_permissions(name)
        return permissions.get(permission, False)

    # ============================================================
    # HOOKS
    # ============================================================
    def get_hooks(self, name: str) -> List[str]:
        """Get plugin hooks"""
        entry = self.get(name)
        return entry.hooks if entry else []

    def get_plugins_with_hook(self, hook: str) -> List[str]:
        """Get plugins that have a specific hook"""
        return [name for name, entry in self.registry.items() if hook in entry.hooks]

    # ============================================================
    # EVENTS
    # ============================================================
    def get_events(self, name: str) -> List[str]:
        """Get plugin events"""
        entry = self.get(name)
        return entry.events if entry else []

    def get_plugins_with_event(self, event: str) -> List[str]:
        """Get plugins that subscribe to a specific event"""
        return [name for name, entry in self.registry.items() if event in entry.events]

    # ============================================================
    # PERSISTENCE
    # ============================================================
    def save(self) -> bool:
        """Save registry to disk"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)

            # Convert to dict
            data = {
                name: asdict(entry)
                for name, entry in self.registry.items()
            }

            # Save to file
            with open(self.registry_file, "w") as f:
                json.dump(data, f, indent=4)

            self.logger.info(f"Registry saved to: {self.registry_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving registry: {e}")
            return False

    def load(self) -> bool:
        """Load registry from disk"""
        try:
            if not os.path.exists(self.registry_file):
                self.logger.info(f"Registry file not found: {self.registry_file}")
                return True

            with open(self.registry_file, "r") as f:
                data = json.load(f)

            # Convert to entries
            self.registry = {
                name: PluginRegistryEntry(**entry_data)
                for name, entry_data in data.items()
            }

            self.logger.info(f"Registry loaded from: {self.registry_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error loading registry: {e}")
            return False

    # ============================================================
    # STATISTICS
    # ============================================================
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_plugins": len(self.registry),
            "enabled_plugins": len(self.list_enabled()),
            "disabled_plugins": len(self.list_disabled()),
            "plugins_with_hooks": len([e for e in self.registry.values() if e.hooks]),
            "plugins_with_events": len([e for e in self.registry.values() if e.events]),
        }
