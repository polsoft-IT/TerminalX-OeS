"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleIntegration
  VERSION: 1.0.0
  MODULE CLASS: ModuleIntegration
  DESCRIPTION:
       Module integration system for TerminalX

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

import sys
import importlib
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from pathlib import Path
from libs.clean_logger import CleanLogger, LogLevel
from libs.dependency_resolver import DependencyResolver, Dependency, DependencyType


@dataclass
class ModuleInfo:
    """Module information"""
    name: str
    version: str
    path: str
    dependencies: List[Dependency]
    enabled: bool = False
    loaded: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ModuleIntegration:
    """Module integration system"""
    
    def __init__(self, dependency_resolver: Optional[DependencyResolver] = None,
                 logger: Optional[CleanLogger] = None):
        """
        Initialize module integration
        
        Args:
            dependency_resolver: Dependency resolver instance
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ModuleIntegration", LogLevel.INFO)
        self.dependency_resolver = dependency_resolver or DependencyResolver()
        self.modules: Dict[str, ModuleInfo] = {}
        self.module_paths: List[str] = []
        self.integration_hooks: Dict[str, List[Callable]] = {}
        
    def add_module_path(self, path: str) -> bool:
        """
        Add module search path
        
        Args:
            path: Path to add
            
        Returns:
            True if added successfully
        """
        if path not in self.module_paths:
            self.module_paths.append(path)
            if path not in sys.path:
                sys.path.insert(0, path)
            self.logger.info(f"Added module path: {path}")
            return True
        return False
        
    def register_module(self, module_info: ModuleInfo) -> bool:
        """
        Register a module
        
        Args:
            module_info: Module information
            
        Returns:
            True if registered successfully
        """
        if module_info.name in self.modules:
            self.logger.warning(f"Module {module_info.name} already registered")
            return False
            
        self.modules[module_info.name] = module_info
        self.logger.info(f"Registered module: {module_info.name}")
        return True
        
    def unregister_module(self, name: str) -> bool:
        """
        Unregister a module
        
        Args:
            name: Module name
            
        Returns:
            True if unregistered successfully
        """
        if name in self.modules:
            del self.modules[name]
            self.logger.info(f"Unregistered module: {name}")
            return True
        return False
        
    def load_module(self, name: str) -> bool:
        """
        Load a module
        
        Args:
            name: Module name
            
        Returns:
            True if loaded successfully
        """
        if name not in self.modules:
            self.logger.error(f"Module {name} not registered")
            return False
            
        module_info = self.modules[name]
        
        # Check dependencies
        if module_info.dependencies:
            satisfied, unsatisfied = self.dependency_resolver.resolve_dependencies(
                module_info.dependencies
            )
            
            if unsatisfied:
                self.logger.error(f"Missing dependencies for {name}: {unsatisfied}")
                return False
                
        try:
            # Import module
            module = importlib.import_module(name)
            
            # Call integration hooks
            if name in self.integration_hooks:
                for hook in self.integration_hooks[name]:
                    try:
                        hook(module, 'load')
                    except Exception as e:
                        self.logger.error(f"Integration hook failed: {e}")
                        
            module_info.loaded = True
            self.logger.info(f"Loaded module: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load module {name}: {e}")
            return False
            
    def unload_module(self, name: str) -> bool:
        """
        Unload a module
        
        Args:
            name: Module name
            
        Returns:
            True if unloaded successfully
        """
        if name not in self.modules:
            return False
            
        module_info = self.modules[name]
        
        if not module_info.loaded:
            return True
            
        try:
            # Call integration hooks
            if name in self.integration_hooks:
                for hook in self.integration_hooks[name]:
                    try:
                        hook(sys.modules[name], 'unload')
                    except Exception as e:
                        self.logger.error(f"Integration hook failed: {e}")
                        
            # Remove from sys.modules
            if name in sys.modules:
                del sys.modules[name]
                
            module_info.loaded = False
            self.logger.info(f"Unloaded module: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload module {name}: {e}")
            return False
            
    def enable_module(self, name: str) -> bool:
        """
        Enable a module
        
        Args:
            name: Module name
            
        Returns:
            True if enabled successfully
        """
        if name not in self.modules:
            return False
            
        self.modules[name].enabled = True
        self.logger.info(f"Enabled module: {name}")
        return True
        
    def disable_module(self, name: str) -> bool:
        """
        Disable a module
        
        Args:
            name: Module name
            
        Returns:
            True if disabled successfully
        """
        if name not in self.modules:
            return False
            
        # Unload if loaded
        if self.modules[name].loaded:
            self.unload_module(name)
            
        self.modules[name].enabled = False
        self.logger.info(f"Disabled module: {name}")
        return True
        
    def add_integration_hook(self, module_name: str, hook: Callable) -> None:
        """
        Add integration hook for module
        
        Args:
            module_name: Module name
            hook: Hook function
        """
        if module_name not in self.integration_hooks:
            self.integration_hooks[module_name] = []
        self.integration_hooks[module_name].append(hook)
        
    def remove_integration_hook(self, module_name: str, hook: Callable) -> bool:
        """
        Remove integration hook
        
        Args:
            module_name: Module name
            hook: Hook function
            
        Returns:
            True if removed
        """
        if module_name in self.integration_hooks:
            if hook in self.integration_hooks[module_name]:
                self.integration_hooks[module_name].remove(hook)
                return True
        return False
        
    def get_module(self, name: str) -> Optional[ModuleInfo]:
        """
        Get module information
        
        Args:
            name: Module name
            
        Returns:
            Module info or None
        """
        return self.modules.get(name)
        
    def list_modules(self, enabled_only: bool = False, 
                    loaded_only: bool = False) -> List[ModuleInfo]:
        """
        List modules
        
        Args:
            enabled_only: Only enabled modules
            loaded_only: Only loaded modules
            
        Returns:
            List of module info
        """
        modules = list(self.modules.values())
        
        if enabled_only:
            modules = [m for m in modules if m.enabled]
            
        if loaded_only:
            modules = [m for m in modules if m.loaded]
            
        return modules
        
    def discover_modules(self, path: str) -> List[ModuleInfo]:
        """
        Discover modules in path
        
        Args:
            path: Path to search
            
        Returns:
            List of discovered modules
        """
        discovered = []
        path_obj = Path(path)
        
        if not path_obj.exists():
            return discovered
            
        for item in path_obj.iterdir():
            if item.is_dir() and (item / '__init__.py').exists():
                module_name = item.name
                module_info = ModuleInfo(
                    name=module_name,
                    version="unknown",
                    path=str(item),
                    dependencies=[]
                )
                discovered.append(module_info)
                
        return discovered
        
    def check_dependencies(self, name: str) -> Dict[str, bool]:
        """
        Check module dependencies
        
        Args:
            name: Module name
            
        Returns:
            Dictionary of dependency name -> satisfied
        """
        if name not in self.modules:
            return {}
            
        module_info = self.modules[name]
        results = {}
        
        for dep in module_info.dependencies:
            results[dep.name] = self.dependency_resolver.is_installed(dep)
            
        return results
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get integration statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_modules': len(self.modules),
            'enabled_modules': sum(1 for m in self.modules.values() if m.enabled),
            'loaded_modules': sum(1 for m in self.modules.values() if m.loaded),
            'module_paths': len(self.module_paths),
            'integration_hooks': sum(len(hooks) for hooks in self.integration_hooks.values())
        }


# Global module integration instance
module_integration = ModuleIntegration()
