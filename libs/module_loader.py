"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleLoader
  VERSION: 1.0.0
  MODULE CLASS: ModuleLoader
  DESCRIPTION:
       Module loading system for TerminalX

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
import importlib.util
from typing import Dict, Optional, Any, List
from pathlib import Path
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class LoadResult:
    """Module load result"""
    module_name: str
    success: bool
    error: Optional[str] = None
    load_time: float = 0.0


class ModuleLoader:
    """Advanced module loading system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize module loader
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ModuleLoader", LogLevel.INFO)
        self.loaded_modules: Dict[str, Any] = {}
        self.load_paths: List[str] = []
        self.load_hooks: List[callable] = []
        
    def add_load_path(self, path: str) -> bool:
        """
        Add module load path
        
        Args:
            path: Path to add
            
        Returns:
            True if added successfully
        """
        path_obj = Path(path)
        
        if not path_obj.exists():
            self.logger.warning(f"Path does not exist: {path}")
            return False
            
        if str(path_obj) not in self.load_paths:
            self.load_paths.append(str(path_obj))
            if str(path_obj) not in sys.path:
                sys.path.insert(0, str(path_obj))
            self.logger.info(f"Added load path: {path}")
            return True
            
        return False
        
    def load_from_file(self, module_name: str, file_path: str) -> LoadResult:
        """
        Load module from file
        
        Args:
            module_name: Module name
            file_path: File path
            
        Returns:
            Load result
        """
        import time
        start_time = time.time()
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                return LoadResult(
                    module_name=module_name,
                    success=False,
                    error="Failed to create module spec"
                )
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            self.loaded_modules[module_name] = module
            load_time = time.time() - start_time
            
            # Call load hooks
            for hook in self.load_hooks:
                try:
                    hook(module_name, module, 'load')
                except Exception as e:
                    self.logger.error(f"Load hook failed: {e}")
                    
            self.logger.info(f"Loaded module from file: {module_name} ({load_time:.3f}s)")
            
            return LoadResult(
                module_name=module_name,
                success=True,
                load_time=load_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to load {module_name}: {e}")
            if module_name in sys.modules:
                del sys.modules[module_name]
            return LoadResult(
                module_name=module_name,
                success=False,
                error=str(e)
            )
            
    def load_from_package(self, package_name: str) -> LoadResult:
        """
        Load module from package
        
        Args:
            package_name: Package name
            
        Returns:
            Load result
        """
        import time
        start_time = time.time()
        
        try:
            module = importlib.import_module(package_name)
            self.loaded_modules[package_name] = module
            load_time = time.time() - start_time
            
            # Call load hooks
            for hook in self.load_hooks:
                try:
                    hook(package_name, module, 'load')
                except Exception as e:
                    self.logger.error(f"Load hook failed: {e}")
                    
            self.logger.info(f"Loaded package: {package_name} ({load_time:.3f}s)")
            
            return LoadResult(
                module_name=package_name,
                success=True,
                load_time=load_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to load package {package_name}: {e}")
            return LoadResult(
                module_name=package_name,
                success=False,
                error=str(e)
            )
            
    def reload(self, module_name: str) -> LoadResult:
        """
        Reload module
        
        Args:
            module_name: Module name
            
        Returns:
            Load result
        """
        import time
        start_time = time.time()
        
        if module_name not in sys.modules:
            return LoadResult(
                module_name=module_name,
                success=False,
                error="Module not loaded"
            )
            
        try:
            module = importlib.reload(sys.modules[module_name])
            self.loaded_modules[module_name] = module
            load_time = time.time() - start_time
            
            # Call load hooks
            for hook in self.load_hooks:
                try:
                    hook(module_name, module, 'reload')
                except Exception as e:
                    self.logger.error(f"Load hook failed: {e}")
                    
            self.logger.info(f"Reloaded module: {module_name} ({load_time:.3f}s)")
            
            return LoadResult(
                module_name=module_name,
                success=True,
                load_time=load_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to reload {module_name}: {e}")
            return LoadResult(
                module_name=module_name,
                success=False,
                error=str(e)
            )
            
    def unload(self, module_name: str) -> bool:
        """
        Unload module
        
        Args:
            module_name: Module name
            
        Returns:
            True if unloaded successfully
        """
        if module_name not in self.loaded_modules:
            return False
            
        try:
            # Call unload hooks
            for hook in self.load_hooks:
                try:
                    hook(module_name, self.loaded_modules[module_name], 'unload')
                except Exception as e:
                    self.logger.error(f"Unload hook failed: {e}")
                    
            # Remove from sys.modules
            if module_name in sys.modules:
                del sys.modules[module_name]
                
            del self.loaded_modules[module_name]
            self.logger.info(f"Unloaded module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload {module_name}: {e}")
            return False
            
    def get_module(self, name: str) -> Optional[Any]:
        """
        Get loaded module
        
        Args:
            name: Module name
            
        Returns:
            Module or None
        """
        return self.loaded_modules.get(name)
        
    def is_loaded(self, name: str) -> bool:
        """
        Check if module is loaded
        
        Args:
            name: Module name
            
        Returns:
            True if loaded
        """
        return name in self.loaded_modules
        
    def list_loaded(self) -> List[str]:
        """
        List loaded modules
        
        Returns:
            List of module names
        """
        return list(self.loaded_modules.keys())
        
    def add_load_hook(self, hook: callable) -> None:
        """
        Add load hook
        
        Args:
            hook: Hook function
        """
        self.load_hooks.append(hook)
        
    def remove_load_hook(self, hook: callable) -> bool:
        """
        Remove load hook
        
        Args:
            hook: Hook function
            
        Returns:
            True if removed
        """
        if hook in self.load_hooks:
            self.load_hooks.remove(hook)
            return True
        return False
        
    def discover_modules(self, path: str) -> List[str]:
        """
        Discover modules in path
        
        Args:
            path: Path to search
            
        Returns:
            List of module names
        """
        modules = []
        path_obj = Path(path)
        
        if not path_obj.exists():
            return modules
            
        for item in path_obj.iterdir():
            if item.is_file() and item.suffix == '.py' and item.name != '__init__.py':
                modules.append(item.stem)
            elif item.is_dir() and (item / '__init__.py').exists():
                modules.append(item.name)
                
        return modules
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get loader statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'loaded_modules': len(self.loaded_modules),
            'load_paths': len(self.load_paths),
            'load_hooks': len(self.load_hooks)
        }


# Global module loader instance
module_loader = ModuleLoader()
