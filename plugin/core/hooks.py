"""
 ============================================================
  MODULE/PLUGIN NAME: PluginHooks
  VERSION: 1.0.0
  MODULE CLASS: PluginHooks
  DESCRIPTION:
       Hook system for TerminalX plugin system

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

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

from libs.clean_logger import CleanLogger, LogLevel


class HookPhase(Enum):
    """Hook phase"""
    PRE = "pre"
    POST = "post"


@dataclass
class HookCallback:
    """Hook callback"""
    plugin_name: str
    callback: Callable
    priority: int = 0


class PluginHooks:
    """
    PLUGIN HOOK SYSTEM:
    - Register hooks
    - Unregister hooks
    - Execute hooks
    - Hook priority
    - Pre/post hooks
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginHooks", LogLevel.INFO)
        self.hooks: Dict[str, List[HookCallback]] = {}

    # ============================================================
    # HOOK REGISTRATION
    # ============================================================
    def register(self, hook_name: str, plugin_name: str, callback: Callable, priority: int = 0) -> bool:
        """Register hook callback"""
        try:
            if hook_name not in self.hooks:
                self.hooks[hook_name] = []

            hook_callback = HookCallback(
                plugin_name=plugin_name,
                callback=callback,
                priority=priority
            )

            self.hooks[hook_name].append(hook_callback)
            # Sort by priority (higher priority first)
            self.hooks[hook_name].sort(key=lambda x: x.priority, reverse=True)

            self.logger.info(f"Hook registered: {hook_name} by {plugin_name} (priority: {priority})")
            return True

        except Exception as e:
            self.logger.error(f"Error registering hook: {e}")
            return False

    def unregister(self, hook_name: str, plugin_name: str) -> bool:
        """Unregister hook callback"""
        if hook_name not in self.hooks:
            self.logger.error(f"Hook not found: {hook_name}")
            return False

        # Remove callbacks for plugin
        original_count = len(self.hooks[hook_name])
        self.hooks[hook_name] = [
            cb for cb in self.hooks[hook_name] if cb.plugin_name != plugin_name
        ]

        if len(self.hooks[hook_name]) == 0:
            del self.hooks[hook_name]

        removed = original_count - len(self.hooks[hook_name])
        self.logger.info(f"Unregistered {removed} hooks for {plugin_name}: {hook_name}")
        return True

    def unregister_plugin(self, plugin_name: str) -> int:
        """Unregister all hooks for plugin"""
        removed = 0
        for hook_name in list(self.hooks.keys()):
            original_count = len(self.hooks[hook_name])
            self.hooks[hook_name] = [
                cb for cb in self.hooks[hook_name] if cb.plugin_name != plugin_name
            ]
            removed += original_count - len(self.hooks[hook_name])

            if len(self.hooks[hook_name]) == 0:
                del self.hooks[hook_name]

        self.logger.info(f"Unregistered {removed} hooks for plugin: {plugin_name}")
        return removed

    # ============================================================
    # HOOK EXECUTION
    # ============================================================
    def execute(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute all callbacks for hook"""
        if hook_name not in self.hooks:
            return []

        results = []
        for hook_callback in self.hooks[hook_name]:
            try:
                result = hook_callback.callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name} for {hook_callback.plugin_name}: {e}")

        return results

    def execute_until(self, hook_name: str, condition: Callable, *args, **kwargs) -> Optional[Any]:
        """Execute hooks until condition is met"""
        if hook_name not in self.hooks:
            return None

        for hook_callback in self.hooks[hook_name]:
            try:
                result = hook_callback.callback(*args, **kwargs)
                if condition(result):
                    return result
            except Exception as e:
                self.logger.error(f"Error executing hook {hook_name} for {hook_callback.plugin_name}: {e}")

        return None

    def execute_first(self, hook_name: str, *args, **kwargs) -> Optional[Any]:
        """Execute first hook callback only"""
        if hook_name not in self.hooks or len(self.hooks[hook_name]) == 0:
            return None

        hook_callback = self.hooks[hook_name][0]
        try:
            return hook_callback.callback(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Error executing hook {hook_name} for {hook_callback.plugin_name}: {e}")
            return None

    # ============================================================
    # HOOK QUERIES
    # ============================================================
    def has_hooks(self, hook_name: str) -> bool:
        """Check if hook has callbacks"""
        return hook_name in self.hooks and len(self.hooks[hook_name]) > 0

    def get_hooks(self, hook_name: str) -> List[HookCallback]:
        """Get all callbacks for hook"""
        return self.hooks.get(hook_name, [])

    def list_hooks(self) -> List[str]:
        """List all hook names"""
        return list(self.hooks.keys())

    def count_hooks(self, hook_name: str) -> int:
        """Count callbacks for hook"""
        return len(self.hooks.get(hook_name, []))

    # ============================================================
    # STANDARD HOOKS
    # ============================================================
    @staticmethod
    def get_standard_hooks() -> List[str]:
        """Get list of standard hook names"""
        return [
            # Tag hooks
            "tag.pre_add", "tag.post_add",
            "tag.pre_remove", "tag.post_remove",
            "tag.pre_search", "tag.post_search",
            # Metadata hooks
            "meta.pre_extract", "meta.post_extract",
            # Rule hooks
            "rule.pre_apply", "rule.post_apply",
            # File hooks
            "file.pre_copy", "file.post_copy",
            "file.pre_move", "file.post_move",
            "file.pre_delete", "file.post_delete",
            # Sync hooks
            "sync.pre_push", "sync.post_push",
            "sync.pre_pull", "sync.post_pull",
            # Watch hooks
            "watch.on_change", "watch.on_create", "watch.on_delete",
            # AI hooks
            "ai.pre_classify", "ai.post_classify",
        ]
