"""
 ============================================================
  MODULE/PLUGIN NAME: PluginPermissions
  VERSION: 1.0.0
  MODULE CLASS: PluginPermissions
  DESCRIPTION:
       Permission system for TerminalX plugin system

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

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

from libs.clean_logger import CleanLogger, LogLevel


class Permission(Enum):
    """Plugin permissions"""
    TAG = "tag"
    META = "meta"
    RULE = "rule"
    FILE = "file"
    AI = "ai"
    OVERLAY = "overlay"
    WATCH = "watch"
    SYNC = "sync"
    NETWORK = "network"
    SYSTEM = "system"


@dataclass
class PermissionPolicy:
    """Permission policy"""
    allow: Set[str]
    deny: Set[str]
    log: bool = True


class PluginPermissions:
    """
    PLUGIN PERMISSION SYSTEM:
    - Check permissions
    - Grant permissions
    - Revoke permissions
    - Permission policies
    - Permission logging
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginPermissions", LogLevel.INFO)
        self.plugin_permissions: Dict[str, Dict[str, bool]] = {}
        self.policies: Dict[str, PermissionPolicy] = {}
        self.default_permissions: Dict[str, bool] = {
            "tag": False,
            "meta": False,
            "rule": False,
            "file": False,
            "ai": False,
            "overlay": False,
            "watch": False,
            "sync": False,
            "network": False,
            "system": False,
        }

    # ============================================================
    # PERMISSION MANAGEMENT
    # ============================================================
    def set_permissions(self, plugin_name: str, permissions: Dict[str, bool]) -> bool:
        """Set permissions for plugin"""
        try:
            # Validate permissions
            valid_permissions = set(self.default_permissions.keys())
            for perm in permissions:
                if perm not in valid_permissions:
                    self.logger.warning(f"Unknown permission: {perm}")

            self.plugin_permissions[plugin_name] = permissions
            self.logger.info(f"Permissions set for {plugin_name}: {permissions}")
            return True

        except Exception as e:
            self.logger.error(f"Error setting permissions: {e}")
            return False

    def get_permissions(self, plugin_name: str) -> Dict[str, bool]:
        """Get permissions for plugin"""
        return self.plugin_permissions.get(plugin_name, self.default_permissions.copy())

    def grant(self, plugin_name: str, permission: str) -> bool:
        """Grant permission to plugin"""
        if plugin_name not in self.plugin_permissions:
            self.plugin_permissions[plugin_name] = self.default_permissions.copy()

        if permission not in self.default_permissions:
            self.logger.error(f"Unknown permission: {permission}")
            return False

        self.plugin_permissions[plugin_name][permission] = True
        self.logger.info(f"Permission granted to {plugin_name}: {permission}")
        return True

    def revoke(self, plugin_name: str, permission: str) -> bool:
        """Revoke permission from plugin"""
        if plugin_name not in self.plugin_permissions:
            self.logger.error(f"Plugin not found: {plugin_name}")
            return False

        if permission not in self.plugin_permissions[plugin_name]:
            self.logger.error(f"Permission not found: {permission}")
            return False

        self.plugin_permissions[plugin_name][permission] = False
        self.logger.info(f"Permission revoked from {plugin_name}: {permission}")
        return True

    def has_permission(self, plugin_name: str, permission: str) -> bool:
        """Check if plugin has permission"""
        permissions = self.get_permissions(plugin_name)
        return permissions.get(permission, False)

    # ============================================================
    # PERMISSION POLICIES
    # ============================================================
    def set_policy(self, policy_name: str, allow: List[str], deny: List[str], log: bool = True) -> bool:
        """Set permission policy"""
        try:
            policy = PermissionPolicy(
                allow=set(allow),
                deny=set(deny),
                log=log
            )
            self.policies[policy_name] = policy
            self.logger.info(f"Policy set: {policy_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error setting policy: {e}")
            return False

    def apply_policy(self, plugin_name: str, policy_name: str) -> bool:
        """Apply policy to plugin"""
        if policy_name not in self.policies:
            self.logger.error(f"Policy not found: {policy_name}")
            return False

        policy = self.policies[policy_name]
        
        # Initialize permissions if not exists
        if plugin_name not in self.plugin_permissions:
            self.plugin_permissions[plugin_name] = self.default_permissions.copy()

        # Apply policy
        for perm in policy.allow:
            if perm in self.plugin_permissions[plugin_name]:
                self.plugin_permissions[plugin_name][perm] = True

        for perm in policy.deny:
            if perm in self.plugin_permissions[plugin_name]:
                self.plugin_permissions[plugin_name][perm] = False

        self.logger.info(f"Policy applied to {plugin_name}: {policy_name}")
        return True

    # ============================================================
    # PERMISSION CHECKING
    # ============================================================
    def check(self, plugin_name: str, permission: str, log: bool = True) -> bool:
        """Check permission with optional logging"""
        has_perm = self.has_permission(plugin_name, permission)
        
        if log:
            if has_perm:
                self.logger.info(f"Permission check passed: {plugin_name}.{permission}")
            else:
                self.logger.warning(f"Permission check failed: {plugin_name}.{permission}")

        return has_perm

    def check_multiple(self, plugin_name: str, permissions: List[str]) -> Dict[str, bool]:
        """Check multiple permissions"""
        results = {}
        for perm in permissions:
            results[perm] = self.has_permission(plugin_name, perm)
        return results

    def require_all(self, plugin_name: str, permissions: List[str]) -> bool:
        """Check if plugin has all required permissions"""
        for perm in permissions:
            if not self.has_permission(plugin_name, perm):
                self.logger.warning(f"Missing required permission: {plugin_name}.{perm}")
                return False
        return True

    def require_any(self, plugin_name: str, permissions: List[str]) -> bool:
        """Check if plugin has any of the required permissions"""
        for perm in permissions:
            if self.has_permission(plugin_name, perm):
                return True
        self.logger.warning(f"Missing all required permissions for: {plugin_name}")
        return False

    # ============================================================
    # PERMISSION QUERIES
    # ============================================================
    def list_permissions(self, plugin_name: str) -> List[str]:
        """List all granted permissions for plugin"""
        permissions = self.get_permissions(plugin_name)
        return [perm for perm, granted in permissions.items() if granted]

    def list_denied(self, plugin_name: str) -> List[str]:
        """List all denied permissions for plugin"""
        permissions = self.get_permissions(plugin_name)
        return [perm for perm, granted in permissions.items() if not granted]

    def get_all_plugins(self) -> List[str]:
        """List all plugins with permissions"""
        return list(self.plugin_permissions.keys())

    # ============================================================
    # PERMISSION RESET
    # ============================================================
    def reset_permissions(self, plugin_name: str) -> bool:
        """Reset plugin permissions to defaults"""
        if plugin_name in self.plugin_permissions:
            self.plugin_permissions[plugin_name] = self.default_permissions.copy()
            self.logger.info(f"Permissions reset for: {plugin_name}")
            return True
        return False

    def clear_permissions(self, plugin_name: str) -> bool:
        """Clear all permissions for plugin"""
        if plugin_name in self.plugin_permissions:
            del self.plugin_permissions[plugin_name]
            self.logger.info(f"Permissions cleared for: {plugin_name}")
            return True
        return False

    # ============================================================
    # PERMISSION VALIDATION
    # ============================================================
    def validate_manifest_permissions(self, permissions: Dict[str, bool]) -> bool:
        """Validate permissions from manifest"""
        valid_permissions = set(self.default_permissions.keys())
        
        for perm in permissions:
            if perm not in valid_permissions:
                self.logger.warning(f"Invalid permission in manifest: {perm}")
                return False

        return True

    # ============================================================
    # STATISTICS
    # ============================================================
    def get_stats(self) -> Dict[str, Any]:
        """Get permission statistics"""
        total_plugins = len(self.plugin_permissions)
        total_policies = len(self.policies)
        
        permission_counts = {}
        for perm in self.default_permissions.keys():
            count = sum(1 for perms in self.plugin_permissions.values() if perms.get(perm, False))
            permission_counts[perm] = count

        return {
            "total_plugins": total_plugins,
            "total_policies": total_policies,
            "permission_counts": permission_counts,
        }
