"""
TerminalX Module Engine
Fully featured module manager with grouped commands (English-only).
Sebastian Januchowski - polsoft.ITS™ Dev

This is a self-contained engine implementing:

- ModuleRegistry
- ModuleManager (core ops)
- ModuleCommandDispatcher (text command interface)

You can wire this into your terminal loop by calling:
    dispatcher.dispatch("module list --full")
"""

from __future__ import annotations
import json
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass
class ModuleMeta:
    name: str
    version: str = "1.0.0"
    path: str = ""
    enabled: bool = True
    dependencies: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)
    docs: Dict[str, Any] = field(default_factory=dict)
    godmode: Dict[str, Any] = field(default_factory=dict)


class ModuleRegistry:
    """
    Registry of all modules, their metadata, and relationships.
    """

    def __init__(self):
        self._modules: Dict[str, ModuleMeta] = {}
        self._registry_file: Optional[str] = None

    # --- basic operations ---------------------------------------------------

    def add_module(self, meta: ModuleMeta) -> None:
        self._modules[meta.name] = meta

    def remove_module(self, name: str) -> bool:
        return self._modules.pop(name, None) is not None

    def get_module(self, name: str) -> Optional[ModuleMeta]:
        return self._modules.get(name)

    def list_modules(self) -> List[ModuleMeta]:
        return list(self._modules.values())

    def has_module(self, name: str) -> bool:
        return name in self._modules

    # --- registry commands (module registry ...) ----------------------------

    def rebuild(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": "Module registry rebuilt (mock).",
            "module_count": len(self._modules),
        }

    def verify(self) -> Dict[str, Any]:
        missing_deps = {}
        for m in self._modules.values():
            for dep in m.dependencies:
                if dep not in self._modules:
                    missing_deps.setdefault(m.name, []).append(dep)

        return {
            "status": "ok" if not missing_deps else "warning",
            "missing_dependencies": missing_deps,
        }

    def clean(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": "Module registry cleaned (mock).",
        }

    def export(self, filepath: str) -> Dict[str, Any]:
        data = [self._meta_to_dict(m) for m in self._modules.values()]
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self._registry_file = filepath
        return {
            "status": "ok",
            "message": f"Module registry exported to {filepath}",
        }

    def import_(self, filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            return {
                "status": "error",
                "message": f"File not found: {filepath}",
            }
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._modules.clear()
        for item in data:
            self.add_module(self._dict_to_meta(item))
        self._registry_file = filepath
        return {
            "status": "ok",
            "message": f"Module registry imported from {filepath}",
            "module_count": len(self._modules),
        }

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def _meta_to_dict(meta: ModuleMeta) -> Dict[str, Any]:
        return {
            "name": meta.name,
            "version": meta.version,
            "path": meta.path,
            "enabled": meta.enabled,
            "dependencies": meta.dependencies,
            "config": meta.config,
            "resources": meta.resources,
            "docs": meta.docs,
            "godmode": meta.godmode,
        }

    @staticmethod
    def _dict_to_meta(data: Dict[str, Any]) -> ModuleMeta:
        return ModuleMeta(
            name=data.get("name", ""),
            version=data.get("version", "1.0.0"),
            path=data.get("path", ""),
            enabled=data.get("enabled", True),
            dependencies=data.get("dependencies", []),
            config=data.get("config", {}),
            resources=data.get("resources", {}),
            docs=data.get("docs", {}),
            godmode=data.get("godmode", {}),
        )


# ---------------------------------------------------------------------------
# Module Manager (implements all module ... commands)
# ---------------------------------------------------------------------------

class ModuleManager:
    """
    High-level manager implementing all module-related commands.
    """

    def __init__(self, registry: Optional[ModuleRegistry] = None):
        self.registry = registry or ModuleRegistry()
        self._links: Dict[Tuple[str, str], bool] = {}
        self._compat: Dict[str, Dict[str, Any]] = {}

    # -----------------------------------------------------------------------
    # 1. Core module commands (module ...)
    # -----------------------------------------------------------------------

    def module_list(self, full: bool = False, tree: bool = False) -> Dict[str, Any]:
        modules = self.registry.list_modules()
        if tree:
            tree_data = {}
            for m in modules:
                tree_data[m.name] = {
                    "dependencies": m.dependencies,
                }
            return {
                "mode": "tree",
                "modules": tree_data,
            }

        if full:
            return {
                "mode": "full",
                "modules": [ModuleRegistry._meta_to_dict(m) for m in modules],
            }

        return {
            "mode": "simple",
            "modules": [m.name for m in modules],
        }

    def module_info(
        self,
        name: str,
        meta: bool = False,
        api: bool = False,
        commands: bool = False,
    ) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        result: Dict[str, Any] = {"status": "ok", "name": name}

        if not (meta or api or commands):
            result["info"] = {
                "version": module.version,
                "path": module.path,
                "enabled": module.enabled,
                "dependencies": module.dependencies,
            }
            return result

        if meta:
            result["meta"] = ModuleRegistry._meta_to_dict(module)
        if api:
            result["api"] = {
                "endpoints": ["run", "stop", "status"],
                "description": "Mock API description.",
            }
        if commands:
            result["commands"] = [
                f"{name} run",
                f"{name} stop",
                f"{name} status",
            ]

        return result

    def module_enable(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        module.enabled = True
        return {"status": "ok", "message": f"Module '{name}' enabled."}

    def module_disable(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        module.enabled = False
        return {"status": "ok", "message": f"Module '{name}' disabled."}

    def module_reload(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {"status": "ok", "message": f"Module '{name}' reloaded."}

    def module_restart(self, name: str) -> Dict[str, Any]:
        return self.module_reload(name)

    def module_install(self, source: str) -> Dict[str, Any]:
        name = os.path.splitext(os.path.basename(source))[0]
        if self.registry.has_module(name):
            return {
                "status": "error",
                "message": f"Module '{name}' already installed.",
            }
        meta = ModuleMeta(
            name=name,
            version="1.0.0",
            path=source,
            enabled=True,
            dependencies=[],
        )
        self.registry.add_module(meta)
        return {
            "status": "ok",
            "message": f"Module '{name}' installed from {source}.",
        }

    def module_uninstall(self, name: str) -> Dict[str, Any]:
        if not self.registry.remove_module(name):
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {"status": "ok", "message": f"Module '{name}' uninstalled."}

    def module_update(self, name: Optional[str] = None, all_: bool = False) -> Dict[str, Any]:
        if all_:
            updated = []
            for m in self.registry.list_modules():
                m.version = self._bump_version(m.version)
                updated.append(m.name)
            return {
                "status": "ok",
                "message": "All modules updated (mock).",
                "updated": updated,
            }

        if not name:
            return {
                "status": "error",
                "message": "Module name required unless --all is used.",
            }

        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        module.version = self._bump_version(module.version)
        return {
            "status": "ok",
            "message": f"Module '{name}' updated to {module.version}.",
        }

    def module_check(self, name: Optional[str] = None, all_: bool = False) -> Dict[str, Any]:
        if all_:
            results = {}
            for m in self.registry.list_modules():
                results[m.name] = self._check_module(m)
            return {
                "status": "ok",
                "results": results,
            }

        if not name:
            return {
                "status": "error",
                "message": "Module name required unless --all is used.",
            }

        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "result": self._check_module(module),
        }

    # -----------------------------------------------------------------------
    # 2. Registry commands (module registry ...)
    # -----------------------------------------------------------------------

    def module_registry_rebuild(self) -> Dict[str, Any]:
        return self.registry.rebuild()

    def module_registry_verify(self) -> Dict[str, Any]:
        return self.registry.verify()

    def module_registry_clean(self) -> Dict[str, Any]:
        return self.registry.clean()

    def module_registry_export(self, filepath: str) -> Dict[str, Any]:
        return self.registry.export(filepath)

    def module_registry_import(self, filepath: str) -> Dict[str, Any]:
        return self.registry.import_(filepath)

    # -----------------------------------------------------------------------
    # 3. Dependency commands (module deps ...)
    # -----------------------------------------------------------------------

    def module_deps(
        self,
        name: str,
        reverse: bool = False,
        missing: bool = False,
        install_missing: bool = False,
    ) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        if reverse:
            dependents = []
            for m in self.registry.list_modules():
                if name in m.dependencies:
                    dependents.append(m.name)
            return {
                "status": "ok",
                "mode": "reverse",
                "dependents": dependents,
            }

        if missing or install_missing:
            missing_deps = [
                dep for dep in module.dependencies
                if not self.registry.has_module(dep)
            ]
            result: Dict[str, Any] = {
                "status": "ok",
                "mode": "missing",
                "missing_dependencies": missing_deps,
            }
            if install_missing and missing_deps:
                installed = []
                for dep in missing_deps:
                    meta = ModuleMeta(
                        name=dep,
                        version="1.0.0",
                        path=f"/mock/path/{dep}",
                        enabled=True,
                        dependencies=[],
                    )
                    self.registry.add_module(meta)
                    installed.append(dep)
                result["installed"] = installed
            return result

        return {
            "status": "ok",
            "mode": "deps",
            "dependencies": module.dependencies,
        }

    # -----------------------------------------------------------------------
    # 4. Config commands (module config ...)
    # -----------------------------------------------------------------------

    def module_config_get(self, name: str, key: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "key": key,
            "value": module.config.get(key),
        }

    def module_config_set(self, name: str, key: str, value: Any) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        module.config[key] = value
        return {
            "status": "ok",
            "message": f"Config '{key}' set for module '{name}'.",
        }

    def module_config_reset(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        module.config.clear()
        return {
            "status": "ok",
            "message": f"Config reset for module '{name}'.",
        }

    def module_config_export(self, name: str, filepath: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(module.config, f, indent=2)
        return {
            "status": "ok",
            "message": f"Config for '{name}' exported to {filepath}.",
        }

    def module_config_import(self, name: str, filepath: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        if not os.path.exists(filepath):
            return {"status": "error", "message": f"File not found: {filepath}"}
        with open(filepath, "r", encoding="utf-8") as f:
            module.config = json.load(f)
        return {
            "status": "ok",
            "message": f"Config for '{name}' imported from {filepath}.",
        }

    # -----------------------------------------------------------------------
    # 5. Diagnostic commands (module diag ...)
    # -----------------------------------------------------------------------

    def module_diag(
        self,
        name: Optional[str] = None,
        full: bool = False,
        fix: bool = False,
        errors_only: bool = False,
        system: bool = False,
    ) -> Dict[str, Any]:
        if system:
            results = {}
            for m in self.registry.list_modules():
                results[m.name] = self._diag_module(m, full=full, fix=fix, errors_only=errors_only)
            return {
                "status": "ok",
                "mode": "system",
                "results": results,
            }

        if not name:
            return {
                "status": "error",
                "message": "Module name required unless --system is used.",
            }

        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        return {
            "status": "ok",
            "mode": "module",
            "result": self._diag_module(module, full=full, fix=fix, errors_only=errors_only),
        }

    # -----------------------------------------------------------------------
    # 6. Resource commands (module resources ...)
    # -----------------------------------------------------------------------

    def module_resources(
        self,
        name: str,
        mem: bool = False,
        cpu: bool = False,
        io: bool = False,
        threads: bool = False,
        all_: bool = False,
    ) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        if not module.resources:
            module.resources = {
                "mem": {"used_mb": 32},
                "cpu": {"percent": 5.0},
                "io": {"reads": 100, "writes": 50},
                "threads": {"count": 3},
            }

        result: Dict[str, Any] = {"status": "ok", "name": name}

        if all_ or (not any([mem, cpu, io, threads])):
            result["resources"] = module.resources
            return result

        if mem:
            result["mem"] = module.resources.get("mem")
        if cpu:
            result["cpu"] = module.resources.get("cpu")
        if io:
            result["io"] = module.resources.get("io")
        if threads:
            result["threads"] = module.resources.get("threads")

        return result

    # -----------------------------------------------------------------------
    # 7. Integration commands (module link / compat ...)
    # -----------------------------------------------------------------------

    def module_link(self, module_name: str, plugin_name: str) -> Dict[str, Any]:
        if not self.registry.has_module(module_name):
            return {"status": "error", "message": f"Module '{module_name}' not found."}
        self._links[(module_name, plugin_name)] = True
        return {
            "status": "ok",
            "message": f"Linked module '{module_name}' with plugin '{plugin_name}'.",
        }

    def module_unlink(self, module_name: str, plugin_name: str) -> Dict[str, Any]:
        if (module_name, plugin_name) in self._links:
            del self._links[(module_name, plugin_name)]
            return {
                "status": "ok",
                "message": f"Unlinked module '{module_name}' from plugin '{plugin_name}'.",
            }
        return {
            "status": "error",
            "message": f"Link between '{module_name}' and '{plugin_name}' not found.",
        }

    def module_compat(
        self,
        name: str,
        check_version: Optional[str] = None,
        list_all: bool = False,
    ) -> Dict[str, Any]:
        if list_all:
            return {
                "status": "ok",
                "compatibility": self._compat,
            }

        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        compat_info = self._compat.get(name, {"compatible": True, "notes": []})

        if check_version:
            compat_info["target_version"] = check_version
            compat_info["compatible"] = True  # Mock check

        return {
            "status": "ok",
            "compatibility": compat_info,
        }

    # -----------------------------------------------------------------------
    # 8. Docs commands (module docs ...)
    # -----------------------------------------------------------------------

    def module_docs(
        self,
        name: str,
        show: bool = False,
        list_docs: bool = False,
        export: Optional[str] = None,
    ) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        if list_docs:
            return {
                "status": "ok",
                "documents": list(module.docs.keys()),
            }

        if export:
            os.makedirs(os.path.dirname(export) or ".", exist_ok=True)
            with open(export, "w", encoding="utf-8") as f:
                json.dump(module.docs, f, indent=2)
            return {
                "status": "ok",
                "message": f"Documentation exported to {export}",
            }

        if show:
            return {
                "status": "ok",
                "documentation": module.docs,
            }

        return {
            "status": "ok",
            "documentation": module.docs,
        }

    # -----------------------------------------------------------------------
    # 9. Godmode commands (module godmode ...)
    # -----------------------------------------------------------------------

    def module_godmode(
        self,
        name: str,
        enable: bool = False,
        disable: bool = False,
        status: bool = False,
    ) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}

        if enable:
            module.godmode["enabled"] = True
            return {
                "status": "ok",
                "message": f"GODMODE enabled for module '{name}'.",
            }

        if disable:
            module.godmode["enabled"] = False
            return {
                "status": "ok",
                "message": f"GODMODE disabled for module '{name}'.",
            }

        return {
            "status": "ok",
            "godmode": module.godmode,
        }

    # -----------------------------------------------------------------------
    # 10. Snapshot commands (module snapshot ...)
    # -----------------------------------------------------------------------

    def module_snapshot(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        # Mock snapshot creation
        return {
            "status": "ok",
            "message": f"Snapshot created for {name}",
            "snapshot_id": f"snap_{name}_{int(time.time())}"
        }

    def module_snapshot_restore(self, snapshot_id: str) -> Dict[str, Any]:
        # Mock snapshot restore
        return {
            "status": "ok",
            "message": f"Snapshot restored: {snapshot_id}"
        }

    def module_snapshot_delete(self, snapshot_id: str) -> Dict[str, Any]:
        # Mock snapshot delete
        return {
            "status": "ok",
            "message": f"Snapshot deleted: {snapshot_id}"
        }

    def module_snapshot_list(self) -> Dict[str, Any]:
        # Mock snapshot list
        return {
            "status": "ok",
            "snapshots": []
        }

    # -----------------------------------------------------------------------
    # 11. Plugin commands (module plugin ...)
    # -----------------------------------------------------------------------

    def module_plugin_list(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "plugins": []
        }

    def module_plugin_run(self, name: str, plugin_name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "message": f"Plugin {plugin_name} run for {name}"
        }

    # -----------------------------------------------------------------------
    # 12. API commands (module api ...)
    # -----------------------------------------------------------------------

    def module_api_list(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "api": ["run", "stop", "status", "configure"]
        }

    def module_api_call(self, name: str, method: str, *args) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "result": f"API call {method} executed on {name} with args {args}"
        }

    # -----------------------------------------------------------------------
    # 13. Profile commands (module profile ...)
    # -----------------------------------------------------------------------

    def module_profile_set(self, name: str, profile_name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "message": f"Profile set for {name}: {profile_name}"
        }

    def module_profile_get(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "profile": "default"
        }

    def module_profile_delete(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "message": f"Profile deleted for {name}"
        }

    def module_profile_apply(self, name: str) -> Dict[str, Any]:
        module = self.registry.get_module(name)
        if not module:
            return {"status": "error", "message": f"Module '{name}' not found."}
        return {
            "status": "ok",
            "message": f"Profile applied to {name}"
        }

    # -----------------------------------------------------------------------
    # 14. Subsystem commands (module subsystem ...)
    # -----------------------------------------------------------------------

    def subsystem_list(self, core_engine) -> Dict[str, Any]:
        """List all loaded subsystems from core engine"""
        return {
            "status": "ok",
            "subsystems": list(core_engine.subsystems.keys())
        }

    def subsystem_info(self, name: str, core_engine) -> Dict[str, Any]:
        """Show subsystem information"""
        subsystem = core_engine.get_subsystem(name)
        if subsystem:
            return {
                "status": "ok",
                "name": name,
                "type": type(subsystem).__name__,
            }
        else:
            return {"status": "error", "message": f"Subsystem '{name}' not found"}

    def subsystem_status(self, core_engine) -> Dict[str, Any]:
        """Show subsystem status"""
        status = {}
        for name, subsystem in core_engine.subsystems.items():
            status[name] = {
                'loaded': True,
                'type': type(subsystem).__name__,
            }
        return {
            "status": "ok",
            "subsystems": status
        }

    # -----------------------------------------------------------------------
    # 15. Manager-level commands
    # -----------------------------------------------------------------------

    def manager_start(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": "Module Manager started"
        }

    def manager_stop(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": "Module Manager stopped"
        }

    def manager_status(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "running": True,
            "module_count": len(self.registry.list_modules())
        }

    def manager_logs(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "logs": []
        }

    def manager_clear_logs(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": "Logs cleared"
        }

    def manager_export(self, path: str) -> Dict[str, Any]:
        return self.registry.export(path)

    def manager_import(self, path: str) -> Dict[str, Any]:
        return self.registry.import_(path)

    def manager_config_get(self, key: str) -> Dict[str, Any]:
        return {
            "status": "ok",
            "key": key,
            "value": None
        }

    def manager_config_set(self, key: str, value: Any) -> Dict[str, Any]:
        return {
            "status": "ok",
            "message": f"Config set: {key} = {value}"
        }

    def manager_stats(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "modules": len(self.registry.list_modules()),
            "running": True
        }

    def manager_diagnose(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "health": "healthy",
            "issues": []
        }

    def manager_health_check(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "healthy": True
        }

    # -----------------------------------------------------------------------
    # Helper methods
    # -----------------------------------------------------------------------

    def _bump_version(self, version: str) -> str:
        """Mock version bumper - just adds .1 to version"""
        parts = version.split(".")
        if len(parts) >= 3:
            patch = int(parts[2]) + 1
            return f"{parts[0]}.{parts[1]}.{patch}"
        return f"{version}.1"

    def _check_module(self, module: ModuleMeta) -> Dict[str, Any]:
        """Mock module health check"""
        return {
            "name": module.name,
            "healthy": True,
            "issues": [],
            "warnings": [],
        }

    def _diag_module(
        self,
        module: ModuleMeta,
        full: bool = False,
        fix: bool = False,
        errors_only: bool = False,
    ) -> Dict[str, Any]:
        """Mock module diagnostic"""
        result = {
            "name": module.name,
            "status": "healthy",
            "errors": [],
            "warnings": [],
        }

        if full:
            result["full_report"] = {
                "version": module.version,
                "path": module.path,
                "enabled": module.enabled,
                "dependencies": module.dependencies,
            }

        if fix:
            result["fixes_applied"] = []

        if errors_only:
            result.pop("warnings", None)

        return result


# ---------------------------------------------------------------------------
# Module Command Dispatcher (text command interface)
# ---------------------------------------------------------------------------

class ModuleCommandDispatcher:
    """
    Text command dispatcher for module commands.
    Parses text commands and calls appropriate ModuleManager methods.
    """

    def __init__(self, manager: Optional[ModuleManager] = None, core_engine=None):
        self.manager = manager or ModuleManager()
        self.core_engine = core_engine

    def dispatch(self, command: str) -> Dict[str, Any]:
        """
        Dispatch a text command to the appropriate module manager method.
        
        Command syntax:
            module list [--full] [--tree]
            module info <name> [--meta] [--api] [--commands]
            module enable <name>
            module disable <name>
            module reload <name>
            module restart <name>
            module install <source>
            module uninstall <name>
            module update <name> | --all
            module check <name> | --all
            module registry rebuild
            module registry verify
            module registry clean
            module registry export <filepath>
            module registry import <filepath>
            module deps <name> [--reverse] [--missing] [--install-missing]
            module config get <name> <key>
            module config set <name> <key> <value>
            module config reset <name>
            module config export <name> <filepath>
            module config import <name> <filepath>
            module diag <name> [--full] [--fix] [--errors-only] | --system
            module resources <name> [--mem] [--cpu] [--io] [--threads] | --all
            module link <module_name> <plugin_name>
            module unlink <module_name> <plugin_name>
            module compat <name> [--check-version <ver>] | --list-all
            module docs <name> [--show] [--list-docs] [--export <path>]
            module godmode <name> [--enable] [--disable] | --status
            module snapshot create <name>
            module snapshot restore <snapshot_id>
            module snapshot delete <snapshot_id>
            module snapshot list
            module plugin list <name>
            module plugin run <name> <plugin_name>
            module api list <name>
            module api call <name> <method> [args...]
            module profile set <name> <profile_name>
            module profile get <name>
            module profile delete <name>
            module profile apply <name>
            module manager start
            module manager stop
            module manager status
            module manager logs
            module manager clear_logs
            module manager export <path>
            module manager import <path>
            module manager config get <key>
            module manager config set <key> <value>
            module manager stats
            module manager diagnose
            module manager health_check
            module subsystem list
            module subsystem info <name>
            module subsystem status
        """
        parts = command.split()
        if not parts or parts[0] != "module":
            return {"status": "error", "message": "Command must start with 'module'"}

        if len(parts) < 2:
            return {"status": "error", "message": "Module command required"}

        # Core commands
        if parts[1] == "list":
            return self._dispatch_list(parts[2:])
        elif parts[1] == "info":
            return self._dispatch_info(parts[2:])
        elif parts[1] == "enable":
            return self.manager.module_enable(parts[2])
        elif parts[1] == "disable":
            return self.manager.module_disable(parts[2])
        elif parts[1] == "reload":
            return self.manager.module_reload(parts[2])
        elif parts[1] == "restart":
            return self.manager.module_restart(parts[2])
        elif parts[1] == "install":
            return self.manager.module_install(parts[2])
        elif parts[1] == "uninstall":
            return self.manager.module_uninstall(parts[2])
        elif parts[1] == "update":
            return self._dispatch_update(parts[2:])
        elif parts[1] == "check":
            return self._dispatch_check(parts[2:])

        # Registry commands
        elif parts[1] == "registry":
            return self._dispatch_registry(parts[2:])

        # Dependency commands
        elif parts[1] == "deps":
            return self._dispatch_deps(parts[2:])

        # Config commands
        elif parts[1] == "config":
            return self._dispatch_config(parts[2:])

        # Diagnostic commands
        elif parts[1] == "diag":
            return self._dispatch_diag(parts[2:])

        # Resource commands
        elif parts[1] == "resources":
            return self._dispatch_resources(parts[2:])

        # Integration commands
        elif parts[1] == "link":
            return self.manager.module_link(parts[2], parts[3])
        elif parts[1] == "unlink":
            return self.manager.module_unlink(parts[2], parts[3])
        elif parts[1] == "compat":
            return self._dispatch_compat(parts[2:])

        # Docs commands
        elif parts[1] == "docs":
            return self._dispatch_docs(parts[2:])

        # Godmode commands
        elif parts[1] == "godmode":
            return self._dispatch_godmode(parts[2:])

        # Snapshot commands
        elif parts[1] == "snapshot":
            return self._dispatch_snapshot(parts[2:])

        # Plugin commands
        elif parts[1] == "plugin":
            return self._dispatch_plugin(parts[2:])

        # API commands
        elif parts[1] == "api":
            return self._dispatch_api(parts[2:])

        # Profile commands
        elif parts[1] == "profile":
            return self._dispatch_profile(parts[2:])

        # Manager commands
        elif parts[1] == "manager":
            return self._dispatch_manager(parts[2:])

        # Subsystem commands
        elif parts[1] == "subsystem":
            return self._dispatch_subsystem(parts[2:])

        else:
            return {"status": "error", "message": f"Unknown module command: {parts[1]}"}

    def _dispatch_list(self, args: List[str]) -> Dict[str, Any]:
        full = "--full" in args
        tree = "--tree" in args
        result = self.manager.module_list(full=full, tree=tree)
        # Ensure result has proper status
        if "status" not in result:
            result["status"] = "ok"
        return result

    def _dispatch_info(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        meta = "--meta" in args
        api = "--api" in args
        commands = "--commands" in args
        return self.manager.module_info(name, meta=meta, api=api, commands=commands)

    def _dispatch_update(self, args: List[str]) -> Dict[str, Any]:
        all_ = "--all" in args
        name = None
        for arg in args:
            if not arg.startswith("--"):
                name = arg
                break
        return self.manager.module_update(name=name, all_=all_)

    def _dispatch_check(self, args: List[str]) -> Dict[str, Any]:
        all_ = "--all" in args
        name = None
        for arg in args:
            if not arg.startswith("--"):
                name = arg
                break
        return self.manager.module_check(name=name, all_=all_)

    def _dispatch_registry(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Registry command required"}
        if args[0] == "rebuild":
            return self.manager.module_registry_rebuild()
        elif args[0] == "verify":
            return self.manager.module_registry_verify()
        elif args[0] == "clean":
            return self.manager.module_registry_clean()
        elif args[0] == "export":
            return self.manager.module_registry_export(args[1])
        elif args[0] == "import":
            return self.manager.module_registry_import(args[1])
        else:
            return {"status": "error", "message": f"Unknown registry command: {args[0]}"}

    def _dispatch_deps(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        reverse = "--reverse" in args
        missing = "--missing" in args
        install_missing = "--install-missing" in args
        return self.manager.module_deps(name, reverse=reverse, missing=missing, install_missing=install_missing)

    def _dispatch_config(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Config command required"}
        if args[0] == "get":
            return self.manager.module_config_get(args[1], args[2])
        elif args[0] == "set":
            return self.manager.module_config_set(args[1], args[2], args[3])
        elif args[0] == "reset":
            return self.manager.module_config_reset(args[1])
        elif args[0] == "export":
            return self.manager.module_config_export(args[1], args[2])
        elif args[0] == "import":
            return self.manager.module_config_import(args[1], args[2])
        else:
            return {"status": "error", "message": f"Unknown config command: {args[0]}"}

    def _dispatch_diag(self, args: List[str]) -> Dict[str, Any]:
        system = "--system" in args
        full = "--full" in args
        fix = "--fix" in args
        errors_only = "--errors-only" in args
        name = None
        for arg in args:
            if not arg.startswith("--"):
                name = arg
                break
        return self.manager.module_diag(name=name, full=full, fix=fix, errors_only=errors_only, system=system)

    def _dispatch_resources(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        mem = "--mem" in args
        cpu = "--cpu" in args
        io = "--io" in args
        threads = "--threads" in args
        all_ = "--all" in args
        return self.manager.module_resources(name, mem=mem, cpu=cpu, io=io, threads=threads, all_=all_)

    def _dispatch_compat(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        check_version = None
        list_all = "--list-all" in args
        for i, arg in enumerate(args):
            if arg == "--check-version" and i + 1 < len(args):
                check_version = args[i + 1]
        return self.manager.module_compat(name, check_version=check_version, list_all=list_all)

    def _dispatch_docs(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        show = "--show" in args
        list_docs = "--list-docs" in args
        export = None
        for i, arg in enumerate(args):
            if arg == "--export" and i + 1 < len(args):
                export = args[i + 1]
        return self.manager.module_docs(name, show=show, list_docs=list_docs, export=export)

    def _dispatch_godmode(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Module name required"}
        name = args[0]
        enable = "--enable" in args
        disable = "--disable" in args
        status = "--status" in args
        return self.manager.module_godmode(name, enable=enable, disable=disable, status=status)

    def _dispatch_snapshot(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Snapshot command required"}
        if args[0] == "create":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_snapshot(args[1])
        elif args[0] == "restore":
            if len(args) < 2:
                return {"status": "error", "message": "Snapshot ID required"}
            return self.manager.module_snapshot_restore(args[1])
        elif args[0] == "delete":
            if len(args) < 2:
                return {"status": "error", "message": "Snapshot ID required"}
            return self.manager.module_snapshot_delete(args[1])
        elif args[0] == "list":
            return self.manager.module_snapshot_list()
        else:
            return {"status": "error", "message": f"Unknown snapshot command: {args[0]}"}

    def _dispatch_plugin(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Plugin command required"}
        if args[0] == "list":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_plugin_list(args[1])
        elif args[0] == "run":
            if len(args) < 3:
                return {"status": "error", "message": "Module name and plugin name required"}
            return self.manager.module_plugin_run(args[1], args[2])
        else:
            return {"status": "error", "message": f"Unknown plugin command: {args[0]}"}

    def _dispatch_api(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "API command required"}
        if args[0] == "list":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_api_list(args[1])
        elif args[0] == "call":
            if len(args) < 3:
                return {"status": "error", "message": "Module name and method required"}
            method = args[2]
            method_args = args[3:]
            return self.manager.module_api_call(args[1], method, *method_args)
        else:
            return {"status": "error", "message": f"Unknown API command: {args[0]}"}

    def _dispatch_profile(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Profile command required"}
        if args[0] == "set":
            if len(args) < 3:
                return {"status": "error", "message": "Module name and profile name required"}
            return self.manager.module_profile_set(args[1], args[2])
        elif args[0] == "get":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_profile_get(args[1])
        elif args[0] == "delete":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_profile_delete(args[1])
        elif args[0] == "apply":
            if len(args) < 2:
                return {"status": "error", "message": "Module name required"}
            return self.manager.module_profile_apply(args[1])
        else:
            return {"status": "error", "message": f"Unknown profile command: {args[0]}"}

    def _dispatch_manager(self, args: List[str]) -> Dict[str, Any]:
        if not args:
            return {"status": "error", "message": "Manager command required"}
        if args[0] == "start":
            return self.manager.manager_start()
        elif args[0] == "stop":
            return self.manager.manager_stop()
        elif args[0] == "status":
            return self.manager.manager_status()
        elif args[0] == "logs":
            return self.manager.manager_logs()
        elif args[0] == "clear_logs":
            return self.manager.manager_clear_logs()
        elif args[0] == "export":
            if len(args) < 2:
                return {"status": "error", "message": "Path required"}
            return self.manager.manager_export(args[1])
        elif args[0] == "import":
            if len(args) < 2:
                return {"status": "error", "message": "Path required"}
            return self.manager.manager_import(args[1])
        elif args[0] == "config":
            if len(args) < 2:
                return {"status": "error", "message": "Config command required"}
            if args[1] == "get":
                if len(args) < 3:
                    return {"status": "error", "message": "Key required"}
                return self.manager.manager_config_get(args[2])
            elif args[1] == "set":
                if len(args) < 4:
                    return {"status": "error", "message": "Key and value required"}
                return self.manager.manager_config_set(args[2], args[3])
            else:
                return {"status": "error", "message": f"Unknown config command: {args[1]}"}
        elif args[0] == "stats":
            return self.manager.manager_stats()
        elif args[0] == "diagnose":
            return self.manager.manager_diagnose()
        elif args[0] == "health_check":
            return self.manager.manager_health_check()
        else:
            return {"status": "error", "message": f"Unknown manager command: {args[0]}"}

    def _dispatch_subsystem(self, args: List[str]) -> Dict[str, Any]:
        if not self.core_engine:
            return {"status": "error", "message": "Core engine not available"}
        if not args:
            return {"status": "error", "message": "Subsystem command required"}
        if args[0] == "list":
            return self.manager.subsystem_list(self.core_engine)
        elif args[0] == "info":
            if len(args) < 2:
                return {"status": "error", "message": "Subsystem name required"}
            return self.manager.subsystem_info(args[1], self.core_engine)
        elif args[0] == "status":
            return self.manager.subsystem_status(self.core_engine)
        else:
            return {"status": "error", "message": f"Unknown subsystem command: {args[0]}"}


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    dispatcher = ModuleCommandDispatcher()
    
    # Add some test modules
    dispatcher.manager.registry.add_module(ModuleMeta(
        name="core",
        version="1.0.0",
        path="/modules/core",
        dependencies=[],
    ))
    dispatcher.manager.registry.add_module(ModuleMeta(
        name="security",
        version="1.2.0",
        path="/modules/security",
        dependencies=["core"],
    ))
    
    # Test commands
    print("=== Module Commands Test ===")
    print("\nmodule list:")
    print(dispatcher.dispatch("module list"))
    
    print("\nmodule list --full:")
    print(dispatcher.dispatch("module list --full"))
    
    print("\nmodule info core:")
    print(dispatcher.dispatch("module info core"))
    
    print("\nmodule deps security:")
    print(dispatcher.dispatch("module deps security"))
    
    print("\nmodule registry verify:")
    print(dispatcher.dispatch("module registry verify"))
    
    print("\nmodule diag core --full:")
    print(dispatcher.dispatch("module diag core --full"))
