"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleRegistry
  VERSION: 1.0.0
  MODULE CLASS: ModuleRegistry
  DESCRIPTION:
       Module registry system for TerminalX

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

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from libs.clean_logger import CleanLogger, LogLevel
from libs.dependency_resolver import Dependency, DependencyType


@dataclass
class ModuleManifest:
    """Module manifest"""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[Dict[str, Any]]
    entry_point: str
    enabled: bool = True
    installed_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.installed_at:
            self.installed_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()


class ModuleRegistry:
    """Module registry system"""
    
    def __init__(self, registry_path: Optional[Path] = None, logger: Optional[CleanLogger] = None):
        """
        Initialize module registry
        
        Args:
            registry_path: Path to registry file
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ModuleRegistry", LogLevel.INFO)
        self.registry_path = registry_path or Path.home() / ".terminalx" / "modules" / "registry.json"
        self.modules: Dict[str, ModuleManifest] = {}
        
        self._init_registry()
        self._load_registry()
        
    def _init_registry(self) -> None:
        """Initialize registry directory"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
    def _load_registry(self) -> None:
        """Load registry from file"""
        if not self.registry_path.exists():
            return
            
        try:
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                
            for name, manifest_data in data.items():
                self.modules[name] = ModuleManifest(**manifest_data)
                
        except Exception as e:
            self.logger.error(f"Failed to load registry: {e}")
            
    def _save_registry(self) -> None:
        """Save registry to file"""
        try:
            data = {name: asdict(manifest) for name, manifest in self.modules.items()}
            
            with open(self.registry_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save registry: {e}")
            
    def register(self, manifest: ModuleManifest) -> bool:
        """
        Register a module
        
        Args:
            manifest: Module manifest
            
        Returns:
            True if registered successfully
        """
        if manifest.name in self.modules:
            self.logger.warning(f"Module {manifest.name} already registered")
            return False
            
        self.modules[manifest.name] = manifest
        self._save_registry()
        self.logger.info(f"Registered module: {manifest.name}")
        return True
        
    def unregister(self, name: str) -> bool:
        """
        Unregister a module
        
        Args:
            name: Module name
            
        Returns:
            True if unregistered successfully
        """
        if name not in self.modules:
            return False
            
        del self.modules[name]
        self._save_registry()
        self.logger.info(f"Unregistered module: {name}")
        return True
        
    def get(self, name: str) -> Optional[ModuleManifest]:
        """
        Get module manifest
        
        Args:
            name: Module name
            
        Returns:
            Module manifest or None
        """
        return self.modules.get(name)
        
    def update(self, name: str, manifest: ModuleManifest) -> bool:
        """
        Update module manifest
        
        Args:
            name: Module name
            manifest: New manifest
            
        Returns:
            True if updated successfully
        """
        if name not in self.modules:
            return False
            
        manifest.updated_at = datetime.now().isoformat()
        self.modules[name] = manifest
        self._save_registry()
        self.logger.info(f"Updated module: {name}")
        return True
        
    def enable(self, name: str) -> bool:
        """
        Enable module
        
        Args:
            name: Module name
            
        Returns:
            True if enabled successfully
        """
        if name not in self.modules:
            return False
            
        self.modules[name].enabled = True
        self.modules[name].updated_at = datetime.now().isoformat()
        self._save_registry()
        self.logger.info(f"Enabled module: {name}")
        return True
        
    def disable(self, name: str) -> bool:
        """
        Disable module
        
        Args:
            name: Module name
            
        Returns:
            True if disabled successfully
        """
        if name not in self.modules:
            return False
            
        self.modules[name].enabled = False
        self.modules[name].updated_at = datetime.now().isoformat()
        self._save_registry()
        self.logger.info(f"Disabled module: {name}")
        return True
        
    def list_modules(self, enabled_only: bool = False) -> List[ModuleManifest]:
        """
        List modules
        
        Args:
            enabled_only: Only enabled modules
            
        Returns:
            List of module manifests
        """
        modules = list(self.modules.values())
        
        if enabled_only:
            modules = [m for m in modules if m.enabled]
            
        return modules
        
    def search(self, query: str) -> List[ModuleManifest]:
        """
        Search modules
        
        Args:
            query: Search query
            
        Returns:
            List of matching modules
        """
        query = query.lower()
        results = []
        
        for manifest in self.modules.values():
            if (query in manifest.name.lower() or
                query in manifest.description.lower() or
                query in manifest.author.lower()):
                results.append(manifest)
                
        return results
        
    def get_dependencies(self, name: str) -> List[Dependency]:
        """
        Get module dependencies
        
        Args:
            name: Module name
            
        Returns:
            List of dependencies
        """
        manifest = self.modules.get(name)
        if not manifest:
            return []
            
        dependencies = []
        for dep_data in manifest.dependencies:
            dep_type = DependencyType(dep_data.get('type', 'python_package'))
            dependencies.append(Dependency(
                name=dep_data['name'],
                version=dep_data.get('version'),
                dependency_type=dep_type,
                required=dep_data.get('required', True),
                alternatives=dep_data.get('alternatives', [])
            ))
            
        return dependencies
        
    def get_dependents(self, name: str) -> List[str]:
        """
        Get modules that depend on this module
        
        Args:
            name: Module name
            
        Returns:
            List of dependent module names
        """
        dependents = []
        
        for module_name, manifest in self.modules.items():
            for dep_data in manifest.dependencies:
                if dep_data['name'] == name:
                    dependents.append(module_name)
                    break
                    
        return dependents
        
    def check_conflicts(self, name: str) -> List[str]:
        """
        Check for module conflicts
        
        Args:
            name: Module name
            
        Returns:
            List of conflicting module names
        """
        conflicts = []
        manifest = self.modules.get(name)
        
        if not manifest:
            return conflicts
            
        # Check for name conflicts
        for other_name in self.modules:
            if other_name != name and other_name == name:
                conflicts.append(other_name)
                
        return conflicts
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get registry statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_modules': len(self.modules),
            'enabled_modules': sum(1 for m in self.modules.values() if m.enabled),
            'disabled_modules': sum(1 for m in self.modules.values() if not m.enabled),
            'registry_path': str(self.registry_path)
        }
        
    def export_registry(self, path: str) -> bool:
        """
        Export registry to file
        
        Args:
            path: Export path
            
        Returns:
            True if exported successfully
        """
        try:
            data = {name: asdict(manifest) for name, manifest in self.modules.items()}
            
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.info(f"Exported registry to {path}")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
            
    def import_registry(self, path: str, merge: bool = False) -> bool:
        """
        Import registry from file
        
        Args:
            path: Import path
            merge: Merge with existing registry
            
        Returns:
            True if imported successfully
        """
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            if not merge:
                self.modules.clear()
                
            for name, manifest_data in data.items():
                self.modules[name] = ModuleManifest(**manifest_data)
                
            self._save_registry()
            self.logger.info(f"Imported registry from {path}")
            return True
        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            return False


# Global module registry instance
module_registry = ModuleRegistry()
