"""
 ============================================================
  MODULE/PLUGIN NAME: BuildModule
  VERSION: 1.0.0
  MODULE CLASS: BuildModule
  DESCRIPTION:
       Main build system integrating all build components for TerminalX

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
from typing import Dict, List, Any, Optional
from datetime import datetime

from .build_engine import ParallelBuildEngine, BuildStatus
from .dependency_installer import DependencyInstaller, DepType
from .plugin_build import PluginBuildSystem, PluginStatus


class BuildModule:
    """Main build system for TerminalX"""
    
    def __init__(self):
        self.build_engine = ParallelBuildEngine()
        self.dependency_installer = DependencyInstaller()
        self.plugin_build = PluginBuildSystem()
        self.build_history: List[Dict] = []
        self.initialized = False
        self.logger = None
        self.notification_callback = None
        
    def set_logger(self, logger):
        """Set the logger for the build module"""
        self.logger = logger
        
    def set_notification_callback(self, callback):
        """Set the notification callback"""
        self.notification_callback = callback
        
    async def initialize(self, config: Optional[Dict] = None):
        """Initialize the build module"""
        self.initialized = True
        return True
        
    async def build_project(self, project_path: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """Build a TerminalX project"""
        result = {
            'status': 'started',
            'start_time': datetime.now().isoformat(),
            'project_path': project_path,
            'config': config or {}
        }
        
        try:
            # Install dependencies
            await self.dependency_installer.install_dependencies(project_path, DepType.PIP)
            
            # Build project
            build_result = await self.build_engine.build(project_path, config or {})
            
            result['status'] = build_result
            result['end_time'] = datetime.now().isoformat()
            
            self.build_history.append(result)
            return result
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['end_time'] = datetime.now().isoformat()
            self.build_history.append(result)
            return result
    
    async def build_plugin(self, plugin_path: str) -> Dict[str, Any]:
        """Build a plugin"""
        return await self.plugin_build.build_plugin(plugin_path)
    
    def get_build_history(self) -> List[Dict]:
        """Get build history"""
        return self.build_history
    
    def clear_build_history(self):
        """Clear build history"""
        self.build_history.clear()
