"""
 ============================================================
  MODULE/PLUGIN NAME: PluginManager
  VERSION: 1.0.0
  MODULE CLASS: PluginManager
  DESCRIPTION:
       Main plugin manager for TerminalX plugin system

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

import os
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

from libs.clean_logger import CleanLogger, LogLevel
from plugin.core.loader import PluginLoader, PluginInfo
from plugin.core.registry import PluginRegistry, PluginRegistryEntry
from plugin.core.sandbox import PluginSandbox
from plugin.core.api import PluginAPI, PluginAPIContext
from plugin.core.hooks import PluginHooks
from plugin.core.events import PluginEvents
from plugin.security.verifier import PluginVerifier
from plugin.security.permissions import PluginPermissions


@dataclass
class PluginManagerConfig:
    """Plugin manager configuration"""
    auto_load: bool = True
    auto_verify: bool = True
    sandbox_enabled: bool = True
    strict_permissions: bool = True
    plugin_dir: str = "plugin/plugins"
    manifest_dir: str = "plugin/manifest"


class PluginManager:
    """
    MAIN PLUGIN MANAGER:
    - Load/unload plugins
    - Manage plugin lifecycle
    - Coordinate all plugin systems
    - Provide unified API
    - Handle plugin errors
    """

    def __init__(self, config: Optional[PluginManagerConfig] = None, logger: Optional[CleanLogger] = None):
        self.config = config or PluginManagerConfig()
        self.logger = logger or CleanLogger("PluginManager", LogLevel.INFO)
        
        # Initialize subsystems
        self.loader = PluginLoader(logger)
        self.registry = PluginRegistry(logger)
        self.sandbox = PluginSandbox(logger)
        self.hooks = PluginHooks(logger)
        self.events = PluginEvents(logger)
        self.verifier = PluginVerifier(logger)
        self.permissions = PluginPermissions(logger)
        
        # Plugin APIs
        self.plugin_apis: Dict[str, PluginAPI] = {}
        
        # State
        self.enabled = False
        self.loaded = False
        self.version_callback = None  # callback for version updates

    # ============================================================
    # VERSION CALLBACK
    # ============================================================
    def set_version_callback(self, callback):
        """Set callback for version updates when plugin count changes"""
        self.version_callback = callback

    def _notify_version_update(self):
        """Notify version callback of plugin count change"""
        if self.version_callback:
            plugin_count = len(self.list_plugins())
            self.version_callback(plugin_count)

    # ============================================================
    # INITIALIZATION
    # ============================================================
    def initialize(self) -> bool:
        """Initialize plugin manager"""
        try:
            # Load registry
            self.registry.load()
            
            # Load signatures
            self.verifier.load_signatures()
            
            # Create plugin directory if not exists
            os.makedirs(self.config.plugin_dir, exist_ok=True)
            os.makedirs(self.config.manifest_dir, exist_ok=True)
            
            self.logger.info("Plugin manager initialized")
            return True

        except Exception as e:
            self.logger.error(f"Error initializing plugin manager: {e}")
            return False

    def start(self) -> bool:
        """Start plugin manager"""
        try:
            # Auto-load plugins if enabled
            if self.config.auto_load:
                self.load_all_plugins()

            self.enabled = True
            self.loaded = True
            self.logger.info("Plugin manager started")
            return True

        except Exception as e:
            self.logger.error(f"Error starting plugin manager: {e}")
            return False

    def stop(self) -> bool:
        """Stop plugin manager"""
        try:
            # Unload all plugins
            self.unload_all_plugins()
            
            # Save registry
            self.registry.save()
            
            # Save signatures
            self.verifier.save_signatures()
            
            self.enabled = False
            self.loaded = False
            self.logger.info("Plugin manager stopped")
            return True

        except Exception as e:
            self.logger.error(f"Error stopping plugin manager: {e}")
            return False

    # ============================================================
    # PLUGIN LOADING
    # ============================================================
    def install_plugin(self, plugin_file: str) -> Optional[PluginInfo]:
        """Install plugin from file"""
        try:
            # Load plugin
            plugin_info = self.loader.load_plugin_from_file(plugin_file)
            if not plugin_info:
                self.logger.error(f"Failed to load plugin from: {plugin_file}")
                return None

            # Verify if enabled
            if self.config.auto_verify:
                verification = self.verifier.verify(plugin_info.name, plugin_info.path)
                if not verification.valid:
                    self.logger.error(f"Plugin verification failed: {plugin_info.name}")
                    self.loader.unload_plugin(plugin_info.name)
                    return None

            # Create sandbox if enabled
            if self.config.sandbox_enabled:
                self.sandbox.create_sandbox(plugin_info.name)

            # Set permissions
            self.permissions.set_permissions(plugin_info.name, plugin_info.permissions)

            # Register plugin
            self.registry.register(plugin_info)

            # Create API context
            api_context = PluginAPIContext(
                plugin_name=plugin_info.name,
                permissions=plugin_info.permissions
            )
            self.plugin_apis[plugin_info.name] = PluginAPI(api_context, self.logger)

            # Emit event
            self.events.emit("on_plugin_loaded", {"plugin": plugin_info.name})

            self.logger.info(f"Plugin installed: {plugin_info.name}")
            self._notify_version_update()
            return plugin_info

        except Exception as e:
            self.logger.error(f"Error installing plugin: {e}")
            return None

    def uninstall_plugin(self, name: str) -> bool:
        """Uninstall plugin"""
        try:
            # Unload plugin
            self.loader.unload_plugin(name)

            # Destroy sandbox
            if self.sandbox.sandbox_exists(name):
                self.sandbox.destroy_sandbox(name)

            # Unregister plugin
            self.registry.unregister(name)

            # Clear permissions
            self.permissions.clear_permissions(name)

            # Remove API
            if name in self.plugin_apis:
                del self.plugin_apis[name]

            # Unregister hooks
            self.hooks.unregister_plugin(name)

            # Unsubscribe from events
            self.events.unsubscribe_plugin(name)

            # Remove signature
            self.verifier.remove_signature(name)

            # Emit event
            self.events.emit("on_plugin_unloaded", {"plugin": name})

            self.logger.info(f"Plugin uninstalled: {name}")
            self._notify_version_update()
            return True

        except Exception as e:
            self.logger.error(f"Error uninstalling plugin: {e}")
            return False

    def load_all_plugins(self) -> List[PluginInfo]:
        """Load all plugins from directory"""
        plugins = []
        for plugin_name in self.loader.discover_plugins():
            plugin_path = os.path.join(self.config.plugin_dir, plugin_name)
            plugin_info = self.loader.load_plugin(plugin_path)
            if plugin_info:
                # Verify if enabled
                if self.config.auto_verify:
                    verification = self.verifier.verify(plugin_info.name, plugin_info.path)
                    if not verification.valid:
                        self.logger.warning(f"Plugin verification failed, skipping: {plugin_info.name}")
                        self.loader.unload_plugin(plugin_info.name)
                        continue

                # Create sandbox if enabled
                if self.config.sandbox_enabled:
                    self.sandbox.create_sandbox(plugin_info.name)

                # Set permissions
                self.permissions.set_permissions(plugin_info.name, plugin_info.permissions)

                # Register plugin
                if not self.registry.exists(plugin_info.name):
                    self.registry.register(plugin_info)
                else:
                    self.registry.update(plugin_info.name, plugin_info)

                # Create API context
                api_context = PluginAPIContext(
                    plugin_name=plugin_info.name,
                    permissions=plugin_info.permissions
                )
                self.plugin_apis[plugin_info.name] = PluginAPI(api_context, self.logger)

                # Emit event
                self.events.emit("on_plugin_loaded", {"plugin": plugin_info.name})

                plugins.append(plugin_info)

        self.logger.info(f"Loaded {len(plugins)} plugins")
        return plugins

    def unload_all_plugins(self) -> bool:
        """Unload all plugins"""
        for plugin_name in list(self.loader.list_plugins()):
            self.uninstall_plugin(plugin_name)
        return True

    # ============================================================
    # PLUGIN CONTROL
    # ============================================================
    def enable_plugin(self, name: str) -> bool:
        """Enable plugin"""
        if not self.loader.enable_plugin(name):
            return False
        
        if not self.registry.enable(name):
            return False

        self.events.emit("on_plugin_enabled", {"plugin": name})
        self.logger.info(f"Plugin enabled: {name}")
        return True

    def disable_plugin(self, name: str) -> bool:
        """Disable plugin"""
        if not self.loader.disable_plugin(name):
            return False
        
        if not self.registry.disable(name):
            return False

        self.events.emit("on_plugin_disabled", {"plugin": name})
        self.logger.info(f"Plugin disabled: {name}")
        return True

    def reload_plugin(self, name: str) -> Optional[PluginInfo]:
        """Reload plugin"""
        plugin_info = self.loader.reload_plugin(name)
        if plugin_info:
            self.registry.update(name, plugin_info)
            self.events.emit("on_plugin_loaded", {"plugin": name})
            self.logger.info(f"Plugin reloaded: {name}")
        return plugin_info

    # ============================================================
    # PLUGIN QUERIES
    # ============================================================
    def list_plugins(self) -> List[PluginRegistryEntry]:
        """List all plugins"""
        return self.registry.list_all()

    def list_enabled_plugins(self) -> List[PluginRegistryEntry]:
        """List enabled plugins"""
        return self.registry.list_enabled()

    def list_disabled_plugins(self) -> List[PluginRegistryEntry]:
        """List disabled plugins"""
        return self.registry.list_disabled()

    def get_plugin_info(self, name: str) -> Optional[PluginRegistryEntry]:
        """Get plugin information"""
        return self.registry.get(name)

    def is_loaded(self, name: str) -> bool:
        """Check if plugin is loaded"""
        return self.loader.is_loaded(name)

    def is_enabled(self, name: str) -> bool:
        """Check if plugin is enabled"""
        return self.registry.is_enabled(name)

    # ============================================================
    # HOOKS
    # ============================================================
    def register_hook(self, hook_name: str, plugin_name: str, callback: Callable, priority: int = 0) -> bool:
        """Register hook callback"""
        return self.hooks.register(hook_name, plugin_name, callback, priority)

    def unregister_hook(self, hook_name: str, plugin_name: str) -> bool:
        """Unregister hook callback"""
        return self.hooks.unregister(hook_name, plugin_name)

    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute hook callbacks"""
        return self.hooks.execute(hook_name, *args, **kwargs)

    def list_hooks(self) -> List[str]:
        """List all hooks"""
        return self.hooks.list_hooks()

    # ============================================================
    # EVENTS
    # ============================================================
    def subscribe_event(self, event_name: str, plugin_name: str, callback: Callable, once: bool = False) -> bool:
        """Subscribe to event"""
        return self.events.subscribe(event_name, plugin_name, callback, once)

    def unsubscribe_event(self, event_name: str, plugin_name: str) -> bool:
        """Unsubscribe from event"""
        return self.events.unsubscribe(event_name, plugin_name)

    def emit_event(self, event_name: str, data: Dict[str, Any] = None) -> List[Any]:
        """Emit event"""
        return self.events.emit(event_name, data)

    def list_events(self) -> List[str]:
        """List all events"""
        return self.events.list_events()

    # ============================================================
    # API
    # ============================================================
    def get_plugin_api(self, name: str) -> Optional[PluginAPI]:
        """Get plugin API"""
        return self.plugin_apis.get(name)

    # ============================================================
    # PERMISSIONS
    # ============================================================
    def check_permission(self, plugin_name: str, permission: str) -> bool:
        """Check plugin permission"""
        return self.permissions.check(plugin_name, permission)

    def grant_permission(self, plugin_name: str, permission: str) -> bool:
        """Grant permission to plugin"""
        return self.permissions.grant(plugin_name, permission)

    def revoke_permission(self, plugin_name: str, permission: str) -> bool:
        """Revoke permission from plugin"""
        return self.permissions.revoke(plugin_name, permission)

    # ============================================================
    # SANDBOX
    # ============================================================
    def get_sandbox_status(self, plugin_name: str) -> Dict[str, Any]:
        """Get sandbox status"""
        return self.sandbox.get_status(plugin_name)

    # ============================================================
    # STATISTICS
    # ============================================================
    def get_stats(self) -> Dict[str, Any]:
        """Get plugin manager statistics"""
        return {
            "enabled": self.enabled,
            "loaded": self.loaded,
            "total_plugins": len(self.list_plugins()),
            "enabled_plugins": len(self.list_enabled_plugins()),
            "disabled_plugins": len(self.list_disabled_plugins()),
            "loaded_plugins": len(self.loader.list_plugins()),
            "total_hooks": len(self.list_hooks()),
            "total_events": len(self.list_events()),
            "permission_stats": self.permissions.get_stats(),
            "registry_stats": self.registry.get_stats(),
        }

    # ============================================================
    # CONFIGURATION
    # ============================================================
    def config_get(self, key: str) -> Any:
        """Get configuration value"""
        return getattr(self.config, key, None)

    def config_set(self, key: str, value: Any) -> bool:
        """Set configuration value"""
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.logger.info(f"Config updated: {key} = {value}")
            return True
        return False
