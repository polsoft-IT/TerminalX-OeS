"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleIsolation
  VERSION: 1.0.0
  MODULE CLASS: ModuleIsolation
  DESCRIPTION:
       Module isolation system for TerminalX

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
import builtins
from typing import Dict, Set, Optional, Any, List
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class IsolatedModule:
    """Isolated module information"""
    name: str
    module: Any
    restricted_globals: Set[str]
    allowed_imports: Set[str]
    sandbox_enabled: bool


class ModuleIsolator:
    """Module isolation system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize module isolator
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ModuleIsolator", LogLevel.INFO)
        self.isolated_modules: Dict[str, IsolatedModule] = {}
        self.global_restrictions: Set[str] = set()
        self.allowed_imports: Set[str] = set()
        
        # Default restricted globals
        self.global_restrictions.update([
            'eval', 'exec', 'compile', '__import__',
            'open', 'file', 'input'
        ])
        
    def set_global_restrictions(self, restrictions: List[str]) -> None:
        """
        Set global restricted identifiers
        
        Args:
            restrictions: List of restricted identifiers
        """
        self.global_restrictions = set(restrictions)
        self.logger.info(f"Set global restrictions: {restrictions}")
        
    def set_allowed_imports(self, imports: List[str]) -> None:
        """
        Set allowed imports
        
        Args:
            imports: List of allowed module names
        """
        self.allowed_imports = set(imports)
        self.logger.info(f"Set allowed imports: {imports}")
        
    def create_sandbox_globals(self, module_name: str, 
                              custom_restrictions: Optional[Set[str]] = None,
                              custom_imports: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        Create sandboxed globals for module
        
        Args:
            module_name: Module name
            custom_restrictions: Custom restricted identifiers
            custom_imports: Custom allowed imports
            
        Returns:
            Sandbox globals dictionary
        """
        restrictions = custom_restrictions or self.global_restrictions
        allowed = custom_imports or self.allowed_imports
        
        # Start with safe builtins
        safe_globals = {
            '__name__': module_name,
            '__file__': '',
            '__package__': module_name.rsplit('.', 1)[0] if '.' in module_name else '',
            '__builtins__': {}
        }
        
        # Add safe builtins
        for name, obj in builtins.__dict__.items():
            if name not in restrictions:
                safe_globals['__builtins__'][name] = obj
                
        # Add restricted import hook
        def safe_import(name, *args, **kwargs):
            if allowed and name not in allowed:
                raise ImportError(f"Import of '{name}' is not allowed")
            return __import__(name, *args, **kwargs)
            
        safe_globals['__import__'] = safe_import
        
        return safe_globals
        
    def load_isolated(self, module_name: str, module_path: str,
                     sandbox: bool = True,
                     restrictions: Optional[Set[str]] = None,
                     allowed_imports: Optional[Set[str]] = None) -> Optional[IsolatedModule]:
        """
        Load module in isolation
        
        Args:
            module_name: Module name
            module_path: Module file path
            sandbox: Enable sandbox
            restrictions: Custom restrictions
            allowed_imports: Custom allowed imports
            
        Returns:
            Isolated module or None
        """
        try:
            if sandbox:
                globals_dict = self.create_sandbox_globals(
                    module_name, restrictions, allowed_imports
                )
            else:
                globals_dict = {
                    '__name__': module_name,
                    '__file__': module_path
                }
                
            # Load module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None or spec.loader is None:
                self.logger.error(f"Failed to load spec for {module_name}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            
            # Execute in sandbox
            spec.loader.exec_module(module)
            
            # Create isolated module info
            isolated = IsolatedModule(
                name=module_name,
                module=module,
                restricted_globals=restrictions or self.global_restrictions,
                allowed_imports=allowed_imports or self.allowed_imports,
                sandbox_enabled=sandbox
            )
            
            self.isolated_modules[module_name] = isolated
            self.logger.info(f"Loaded isolated module: {module_name}")
            return isolated
            
        except Exception as e:
            self.logger.error(f"Failed to load isolated module {module_name}: {e}")
            if module_name in sys.modules:
                del sys.modules[module_name]
            return None
            
    def unload_isolated(self, module_name: str) -> bool:
        """
        Unload isolated module
        
        Args:
            module_name: Module name
            
        Returns:
            True if unloaded successfully
        """
        if module_name not in self.isolated_modules:
            return False
            
        try:
            # Remove from sys.modules
            if module_name in sys.modules:
                del sys.modules[module_name]
                
            del self.isolated_modules[module_name]
            self.logger.info(f"Unloaded isolated module: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload {module_name}: {e}")
            return False
            
    def get_isolated_module(self, name: str) -> Optional[IsolatedModule]:
        """
        Get isolated module
        
        Args:
            name: Module name
            
        Returns:
            Isolated module or None
        """
        return self.isolated_modules.get(name)
        
    def check_access(self, module_name: str, attribute: str) -> bool:
        """
        Check if attribute access is allowed
        
        Args:
            module_name: Module name
            attribute: Attribute name
            
        Returns:
            True if access allowed
        """
        isolated = self.isolated_modules.get(module_name)
        if not isolated:
            return True
            
        # Check if attribute is restricted
        if attribute in isolated.restricted_globals:
            return False
            
        return True
        
    def list_isolated(self) -> List[IsolatedModule]:
        """
        List all isolated modules
        
        Returns:
            List of isolated modules
        """
        return list(self.isolated_modules.values())
        
    def get_module_globals(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Get module globals
        
        Args:
            module_name: Module name
            
        Returns:
            Module globals or None
        """
        isolated = self.isolated_modules.get(module_name)
        if isolated:
            return isolated.module.__dict__
        return None
        
    def restrict_module(self, module_name: str, restrictions: Set[str]) -> bool:
        """
        Add restrictions to module
        
        Args:
            module_name: Module name
            restrictions: Restrictions to add
            
        Returns:
            True if restricted successfully
        """
        isolated = self.isolated_modules.get(module_name)
        if not isolated:
            return False
            
        isolated.restricted_globals.update(restrictions)
        self.logger.info(f"Added restrictions to {module_name}: {restrictions}")
        return True
        
    def allow_imports(self, module_name: str, imports: Set[str]) -> bool:
        """
        Allow additional imports for module
        
        Args:
            module_name: Module name
            imports: Imports to allow
            
        Returns:
            True if allowed successfully
        """
        isolated = self.isolated_modules.get(module_name)
        if not isolated:
            return False
            
        isolated.allowed_imports.update(imports)
        self.logger.info(f"Allowed imports for {module_name}: {imports}")
        return True
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get isolation statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'isolated_modules': len(self.isolated_modules),
            'global_restrictions': len(self.global_restrictions),
            'allowed_imports': len(self.allowed_imports),
            'sandboxed_count': sum(1 for m in self.isolated_modules.values() if m.sandbox_enabled)
        }


# Global module isolator instance
module_isolator = ModuleIsolator()
