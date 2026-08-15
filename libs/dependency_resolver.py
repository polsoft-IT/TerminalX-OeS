"""
 ============================================================
  MODULE/PLUGIN NAME: DependencyResolver
  VERSION: 1.0.0
  MODULE CLASS: DependencyResolver
  DESCRIPTION:
       Module dependency resolution for TerminalX

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
import subprocess
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class DependencyType(Enum):
    """Dependency types"""
    PYTHON_PACKAGE = "python_package"
    SYSTEM_PACKAGE = "system_package"
    MODULE = "module"
    FILE = "file"


@dataclass
class Dependency:
    """Dependency information"""
    name: str
    version: Optional[str] = None
    dependency_type: DependencyType = DependencyType.PYTHON_PACKAGE
    required: bool = True
    alternatives: List[str] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []


class DependencyResolver:
    """Dependency resolution system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize dependency resolver
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("DependencyResolver", LogLevel.INFO)
        self.resolved: Dict[str, bool] = {}
        self.installed_packages: Set[str] = set()
        self._scan_installed_packages()
        
    def _scan_installed_packages(self) -> None:
        """Scan installed Python packages"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--format=freeze'],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if '==' in line:
                    package = line.split('==')[0].lower()
                    self.installed_packages.add(package)
                    
        except Exception as e:
            self.logger.warning(f"Failed to scan packages: {e}")
            # Add common packages as fallback
            self.installed_packages.update(['os', 'sys', 'json', 'pathlib', 'datetime'])
            
    def is_installed(self, dependency: Dependency) -> bool:
        """
        Check if dependency is installed
        
        Args:
            dependency: Dependency to check
            
        Returns:
            True if installed
        """
        if dependency.name in self.resolved:
            return self.resolved[dependency.name]
            
        # Check Python packages
        if dependency.dependency_type == DependencyType.PYTHON_PACKAGE:
            # First check if it's a built-in module
            try:
                __import__(dependency.name)
                self.resolved[dependency.name] = True
                return True
            except ImportError:
                pass
                
            # Then check pip packages
            installed = dependency.name.lower() in self.installed_packages
            
            # Check version if specified
            if installed and dependency.version:
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'show', dependency.name],
                        capture_output=True,
                        text=True
                    )
                    
                    for line in result.stdout.split('\n'):
                        if line.startswith('Version:'):
                            installed_version = line.split(':')[1].strip()
                            # Simple version check
                            if installed_version != dependency.version:
                                installed = False
                            break
                except:
                    pass
                    
            self.resolved[dependency.name] = installed
            return installed
            
        # Check system packages
        elif dependency.dependency_type == DependencyType.SYSTEM_PACKAGE:
            return self._check_system_package(dependency.name)
            
        # Check modules
        elif dependency.dependency_type == DependencyType.MODULE:
            try:
                __import__(dependency.name)
                self.resolved[dependency.name] = True
                return True
            except ImportError:
                self.resolved[dependency.name] = False
                return False
                
        # Check files
        elif dependency.dependency_type == DependencyType.FILE:
            import os
            exists = os.path.exists(dependency.name)
            self.resolved[dependency.name] = exists
            return exists
            
        return False
        
    def _check_system_package(self, name: str) -> bool:
        """
        Check if system package is installed
        
        Args:
            name: Package name
            
        Returns:
            True if installed
        """
        try:
            # Try common package managers
            for cmd in [['dpkg', '-l'], ['rpm', '-qa'], ['pacman', '-Q']]:
                try:
                    result = subprocess.run(cmd + [name], capture_output=True)
                    if result.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
        except Exception:
            pass
            
        return False
        
    def install(self, dependency: Dependency) -> bool:
        """
        Install dependency
        
        Args:
            dependency: Dependency to install
            
        Returns:
            True if installed successfully
        """
        if self.is_installed(dependency):
            self.logger.info(f"Dependency already installed: {dependency.name}")
            return True
            
        self.logger.info(f"Installing dependency: {dependency.name}")
        
        # Try alternatives if main fails
        packages_to_try = [dependency.name] + dependency.alternatives
        
        for package in packages_to_try:
            if self._install_package(package, dependency.dependency_type):
                self.resolved[dependency.name] = True
                self.installed_packages.add(package.lower())
                self.logger.info(f"Successfully installed: {package}")
                return True
                
        self.logger.error(f"Failed to install: {dependency.name}")
        return False
        
    def _install_package(self, name: str, dep_type: DependencyType) -> bool:
        """
        Install a single package
        
        Args:
            name: Package name
            dep_type: Dependency type
            
        Returns:
            True if installed successfully
        """
        try:
            if dep_type == DependencyType.PYTHON_PACKAGE:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', name],
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0
                
            elif dep_type == DependencyType.SYSTEM_PACKAGE:
                # Try different package managers
                for cmd in [['apt-get', 'install', '-y'], ['yum', 'install', '-y'], 
                           ['pacman', '-S', '--noconfirm']]:
                    try:
                        result = subprocess.run(cmd + [name], capture_output=True)
                        if result.returncode == 0:
                            return True
                    except FileNotFoundError:
                        continue
                        
        except Exception as e:
            self.logger.error(f"Installation error: {e}")
            
        return False
        
    def resolve_dependencies(self, dependencies: List[Dependency]) -> Tuple[List[str], List[str]]:
        """
        Resolve all dependencies
        
        Args:
            dependencies: List of dependencies to resolve
            
        Returns:
            Tuple of (satisfied, unsatisfied) dependency names
        """
        satisfied = []
        unsatisfied = []
        
        for dep in dependencies:
            if self.is_installed(dep):
                satisfied.append(dep.name)
            elif dep.required:
                if self.install(dep):
                    satisfied.append(dep.name)
                else:
                    unsatisfied.append(dep.name)
            else:
                unsatisfied.append(dep.name)
                
        return satisfied, unsatisfied
        
    def get_missing_dependencies(self, dependencies: List[Dependency]) -> List[Dependency]:
        """
        Get missing dependencies
        
        Args:
            dependencies: List of dependencies to check
            
        Returns:
            List of missing dependencies
        """
        missing = []
        
        for dep in dependencies:
            if not self.is_installed(dep):
                missing.append(dep)
                
        return missing
        
    def create_requirements_file(self, dependencies: List[Dependency], path: str) -> bool:
        """
        Create requirements.txt file
        
        Args:
            dependencies: List of dependencies
            path: Output file path
            
        Returns:
            True if created successfully
        """
        try:
            with open(path, 'w') as f:
                for dep in dependencies:
                    if dep.dependency_type == DependencyType.PYTHON_PACKAGE:
                        version_spec = f"=={dep.version}" if dep.version else ""
                        f.write(f"{dep.name}{version_spec}\n")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create requirements file: {e}")
            return False
            
    def load_from_requirements(self, path: str) -> List[Dependency]:
        """
        Load dependencies from requirements.txt
        
        Args:
            path: Requirements file path
            
        Returns:
            List of dependencies
        """
        dependencies = []
        
        try:
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '==' in line:
                            name, version = line.split('==', 1)
                        else:
                            name = line
                            version = None
                            
                        dependencies.append(Dependency(
                            name=name,
                            version=version,
                            dependency_type=DependencyType.PYTHON_PACKAGE
                        ))
        except Exception as e:
            self.logger.error(f"Failed to load requirements: {e}")
            
        return dependencies
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get resolver statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'resolved_count': sum(1 for v in self.resolved.values() if v),
            'total_checked': len(self.resolved),
            'installed_packages': len(self.installed_packages)
        }


# Global dependency resolver instance
dependency_resolver = DependencyResolver()
