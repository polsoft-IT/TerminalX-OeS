"""
 ============================================================
  MODULE/PLUGIN NAME: PluginLoader
  VERSION: 1.0.0
  MODULE CLASS: PluginLoader
  DESCRIPTION:
       Dynamic plugin loading for TerminalX plugin system

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

import importlib
import importlib.util
import os
import sys
import json
import shutil
import tempfile
import traceback
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class PluginInfo:
    """Plugin information"""
    name: str
    version: str
    author: str
    description: str
    entry: str
    permissions: Dict[str, bool]
    hooks: List[str]
    events: List[str]
    enabled: bool = True
    path: Optional[str] = None


class PluginLoader:
    """
    DYNAMIC PLUGIN LOADING:
    - Load plugins from directory
    - Load plugins from file
    - Unload plugins
    - Reload plugins
    - Validate plugin manifest
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginLoader", LogLevel.INFO)
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.plugin_dir = "plugin/plugins"
        self.manifest_dir = "plugin/manifest"

    # ============================================================
    # PLUGIN LOADING
    # ============================================================
    def load_plugin(self, plugin_path: str) -> Optional[PluginInfo]:
        """Load plugin from path"""
        try:
            # Load manifest
            manifest_path = os.path.join(plugin_path, "plugin.json")
            if not os.path.exists(manifest_path):
                self.logger.error(f"Plugin manifest not found: {manifest_path}")
                return None

            with open(manifest_path, "r") as f:
                manifest = json.load(f)

            # Validate manifest
            if not self._validate_manifest(manifest):
                self.logger.error(f"Invalid plugin manifest: {manifest_path}")
                return None

            # Create plugin info
            plugin_info = PluginInfo(
                name=manifest["name"],
                version=manifest["version"],
                author=manifest["author"],
                description=manifest["description"],
                entry=manifest["entry"],
                permissions=manifest.get("permissions", {}),
                hooks=manifest.get("hooks", []),
                events=manifest.get("events", []),
                enabled=True,
                path=plugin_path
            )

            # Load plugin module
            entry_path = os.path.join(plugin_path, plugin_info.entry)
            if not os.path.exists(entry_path):
                self.logger.error(f"Plugin entry point not found: {entry_path}")
                return None

            spec = importlib.util.spec_from_file_location(
                f"plugin_{plugin_info.name}",
                entry_path
            )
            
            if spec and spec.loader:
                plugin_module = importlib.util.module_from_spec(spec)
                sys.modules[f"plugin_{plugin_info.name}"] = plugin_module
                spec.loader.exec_module(plugin_module)

                # Store plugin
                self.loaded_plugins[plugin_info.name] = plugin_module
                self.plugin_info[plugin_info.name] = plugin_info

                self.logger.info(f"Plugin loaded: {plugin_info.name} v{plugin_info.version}")
                return plugin_info
            else:
                self.logger.error(f"Failed to load plugin module: {entry_path}")
                return None

        except Exception as e:
            self.logger.error(f"Error loading plugin: {e}")
            self.logger.error(traceback.format_exc())
            return None

    def load_plugin_from_file(self, plugin_file: str) -> Optional[PluginInfo]:
        """Load plugin from archive file"""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix="plugin_")
            
            # Extract archive
            if plugin_file.endswith(".zip"):
                shutil.unpack_archive(plugin_file, temp_dir)
            else:
                self.logger.error(f"Unsupported plugin format: {plugin_file}")
                return None

            # Load plugin
            plugin_info = self.load_plugin(temp_dir)
            
            if plugin_info:
                # Copy to plugins directory
                plugin_dest = os.path.join(self.plugin_dir, plugin_info.name)
                if os.path.exists(plugin_dest):
                    shutil.rmtree(plugin_dest)
                shutil.copytree(temp_dir, plugin_dest)
                plugin_info.path = plugin_dest

            # Cleanup
            shutil.rmtree(temp_dir)
            
            return plugin_info

        except Exception as e:
            self.logger.error(f"Error loading plugin from file: {e}")
            self.logger.error(traceback.format_exc())
            return None

    def unload_plugin(self, name: str) -> bool:
        """Unload plugin"""
        if name not in self.loaded_plugins:
            self.logger.error(f"Plugin not loaded: {name}")
            return False

        try:
            # Call cleanup if exists
            plugin_module = self.loaded_plugins[name]
            if hasattr(plugin_module, "cleanup"):
                plugin_module.cleanup()

            # Remove from sys.modules
            module_name = f"plugin_{name}"
            if module_name in sys.modules:
                del sys.modules[module_name]

            # Remove from loaded plugins
            del self.loaded_plugins[name]
            del self.plugin_info[name]

            self.logger.info(f"Plugin unloaded: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Error unloading plugin: {e}")
            return False

    def reload_plugin(self, name: str) -> Optional[PluginInfo]:
        """Reload plugin"""
        if name not in self.plugin_info:
            self.logger.error(f"Plugin not found: {name}")
            return None

        plugin_path = self.plugin_info[name].path
        if not plugin_path:
            self.logger.error(f"Plugin path not set: {name}")
            return None

        # Unload
        self.unload_plugin(name)

        # Reload
        return self.load_plugin(plugin_path)

    def reload_all(self) -> List[str]:
        """Reload all plugins"""
        reloaded = []
        for name in list(self.plugin_info.keys()):
            if self.reload_plugin(name):
                reloaded.append(name)
        return reloaded

    # ============================================================
    # PLUGIN DISCOVERY
    # ============================================================
    def discover_plugins(self) -> List[str]:
        """Discover plugins in plugins directory"""
        if not os.path.exists(self.plugin_dir):
            return []

        plugins = []
        for item in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, item)
            if os.path.isdir(plugin_path):
                manifest_path = os.path.join(plugin_path, "plugin.json")
                if os.path.exists(manifest_path):
                    plugins.append(item)

        return plugins

    def load_all_plugins(self) -> List[PluginInfo]:
        """Load all discovered plugins"""
        plugins = []
        for plugin_name in self.discover_plugins():
            plugin_path = os.path.join(self.plugin_dir, plugin_name)
            plugin_info = self.load_plugin(plugin_path)
            if plugin_info:
                plugins.append(plugin_info)
        return plugins

    # ============================================================
    # PLUGIN VALIDATION
    # ============================================================
    def _validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """Validate plugin manifest"""
        required_fields = ["name", "version", "author", "description", "entry"]
        
        for field in required_fields:
            if field not in manifest:
                self.logger.error(f"Missing required field: {field}")
                return False

        # Validate permissions
        if "permissions" in manifest:
            valid_permissions = ["tag", "meta", "rule", "file", "ai", "overlay", "watch", "sync", "network", "system"]
            for perm in manifest["permissions"]:
                if perm not in valid_permissions:
                    self.logger.warning(f"Unknown permission: {perm}")

        return True

    # ============================================================
    # PLUGIN STATUS
    # ============================================================
    def is_loaded(self, name: str) -> bool:
        """Check if plugin is loaded"""
        return name in self.loaded_plugins

    def get_plugin_info(self, name: str) -> Optional[PluginInfo]:
        """Get plugin information"""
        return self.plugin_info.get(name)

    def list_plugins(self) -> List[PluginInfo]:
        """List all loaded plugins"""
        return list(self.plugin_info.values())

    def get_plugin(self, name: str) -> Optional[Any]:
        """Get plugin module"""
        return self.loaded_plugins.get(name)

    # ============================================================
    # PLUGIN ENABLE/DISABLE
    # ============================================================
    def enable_plugin(self, name: str) -> bool:
        """Enable plugin"""
        if name in self.plugin_info:
            self.plugin_info[name].enabled = True
            self.logger.info(f"Plugin enabled: {name}")
            return True
        return False

    def disable_plugin(self, name: str) -> bool:
        """Disable plugin"""
        if name in self.plugin_info:
            self.plugin_info[name].enabled = False
            self.logger.info(f"Plugin disabled: {name}")
            return True
        return False

    def is_enabled(self, name: str) -> bool:
        """Check if plugin is enabled"""
        if name in self.plugin_info:
            return self.plugin_info[name].enabled
        return False
