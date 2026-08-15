"""
 ============================================================
  MODULE/PLUGIN NAME: DependencyInstaller
  VERSION: 1.0.0
  MODULE CLASS: DependencyInstaller
  DESCRIPTION:
       Dependency installer for TerminalX build system

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

import asyncio
import subprocess
from enum import Enum
from typing import List, Dict, Optional


class DepType(Enum):
    """Dependency types"""
    PIP = "pip"
    NPM = "npm"
    GIT = "git"
    LOCAL = "local"


class DependencyInstaller:
    """Dependency installer for TerminalX"""
    
    def __init__(self):
        self.installed_dependencies: Dict[str, List[str]] = {}
        
    async def install_dependencies(self, project_path: str, dep_type: DepType) -> Dict[str, Any]:
        """Install dependencies for a project"""
        result = {
            'success': False,
            'installed': [],
            'failed': [],
            'errors': []
        }
        
        try:
            if dep_type == DepType.PIP:
                # Install Python dependencies
                requirements_file = f"{project_path}/requirements.txt"
                try:
                    process = await asyncio.create_subprocess_exec(
                        'pip', 'install', '-r', requirements_file,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    
                    if process.returncode == 0:
                        result['success'] = True
                        result['installed'] = ['requirements.txt']
                    else:
                        result['errors'].append(stderr.decode())
                        
                except Exception as e:
                    result['errors'].append(str(e))
            
            return result
            
        except Exception as e:
            result['errors'].append(str(e))
            return result
    
    def add_dependency(self, project_path: str, dependency: str, dep_type: DepType):
        """Add a dependency to the project"""
        if project_path not in self.installed_dependencies:
            self.installed_dependencies[project_path] = []
        
        self.installed_dependencies[project_path].append(dependency)
    
    def get_dependencies(self, project_path: str) -> List[str]:
        """Get dependencies for a project"""
        return self.installed_dependencies.get(project_path, [])
