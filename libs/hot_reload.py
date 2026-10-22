"""
 ============================================================
  MODULE/PLUGIN NAME: HotReload
  VERSION: 1.0.0
  MODULE CLASS: HotReload
  DESCRIPTION:
       Module reloading without restart for TerminalX

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
import os
import time
from typing import Dict, Set, Optional, Callable, List
from pathlib import Path
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class ReloadResult:
    """Module reload result"""
    module_name: str
    success: bool
    error: Optional[str] = None
    reload_time: float = 0.0


class HotReloadManager:
    """Hot reload manager for modules"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize hot reload manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("HotReloadManager", LogLevel.INFO)
        self.watched_modules: Set[str] = set()
        self.module_timestamps: Dict[str, float] = {}
        self.reload_callbacks: Dict[str, Set[Callable]] = {}
        self.auto_reload_enabled = False
        self.check_interval = 1.0
        
    def watch_module(self, module_name: str) -> bool:
        """
        Watch a module for changes
        
        Args:
            module_name: Module name
            
        Returns:
            True if watching started
        """
        if module_name not in sys.modules:
            self.logger.warning(f"Module {module_name} not loaded")
            return False
            
        self.watched_modules.add(module_name)
        
        # Record initial timestamp
        module = sys.modules[module_name]
        if hasattr(module, '__file__') and module.__file__:
            self.module_timestamps[module_name] = os.path.getmtime(module.__file__)
            
        self.logger.info(f"Watching module: {module_name}")
        return True
        
    def unwatch_module(self, module_name: str) -> bool:
        """
        Stop watching a module
        
        Args:
            module_name: Module name
            
        Returns:
            True if unwatched successfully
        """
        if module_name in self.watched_modules:
            self.watched_modules.remove(module_name)
            if module_name in self.module_timestamps:
                del self.module_timestamps[module_name]
            self.logger.info(f"Stopped watching: {module_name}")
            return True
        return False
        
    def reload_module(self, module_name: str) -> ReloadResult:
        """
        Reload a module
        
        Args:
            module_name: Module name
            
        Returns:
            Reload result
        """
        start_time = time.time()
        
        if module_name not in sys.modules:
            return ReloadResult(
                module_name=module_name,
                success=False,
                error="Module not loaded"
            )
            
        try:
            module = importlib.reload(sys.modules[module_name])
            reload_time = time.time() - start_time
            
            # Update timestamp
            if hasattr(module, '__file__') and module.__file__:
                self.module_timestamps[module_name] = os.path.getmtime(module.__file__)
                
            # Call callbacks
            if module_name in self.reload_callbacks:
                for callback in self.reload_callbacks[module_name]:
                    try:
                        callback(module_name, module)
                    except Exception as e:
                        self.logger.error(f"Reload callback failed: {e}")
                        
            self.logger.info(f"Reloaded module: {module_name} ({reload_time:.3f}s)")
            
            return ReloadResult(
                module_name=module_name,
                success=True,
                reload_time=reload_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to reload {module_name}: {e}")
            return ReloadResult(
                module_name=module_name,
                success=False,
                error=str(e)
            )
            
    def check_changes(self) -> List[ReloadResult]:
        """
        Check for module changes and reload if needed
        
        Returns:
            List of reload results
        """
        results = []
        
        for module_name in self.watched_modules:
            if module_name not in sys.modules:
                continue
                
            module = sys.modules[module_name]
            if not hasattr(module, '__file__') or not module.__file__:
                continue
                
            try:
                current_time = os.path.getmtime(module.__file__)
                last_time = self.module_timestamps.get(module_name, 0)
                
                if current_time > last_time:
                    result = self.reload_module(module_name)
                    results.append(result)
                    
            except Exception as e:
                self.logger.error(f"Error checking {module_name}: {e}")
                
        return results
        
    def add_reload_callback(self, module_name: str, callback: Callable) -> None:
        """
        Add callback for module reload
        
        Args:
            module_name: Module name
            callback: Callback function
        """
        if module_name not in self.reload_callbacks:
            self.reload_callbacks[module_name] = set()
        self.reload_callbacks[module_name].add(callback)
        
    def remove_reload_callback(self, module_name: str, callback: Callable) -> bool:
        """
        Remove reload callback
        
        Args:
            module_name: Module name
            callback: Callback function
            
        Returns:
            True if removed
        """
        if module_name in self.reload_callbacks:
            self.reload_callbacks[module_name].discard(callback)
            if not self.reload_callbacks[module_name]:
                del self.reload_callbacks[module_name]
            return True
        return False
        
    def enable_auto_reload(self, interval: float = 1.0) -> None:
        """
        Enable automatic reload
        
        Args:
            interval: Check interval in seconds
        """
        self.auto_reload_enabled = True
        self.check_interval = interval
        self.logger.info(f"Auto-reload enabled (interval: {interval}s)")
        
    def disable_auto_reload(self) -> None:
        """Disable automatic reload"""
        self.auto_reload_enabled = False
        self.logger.info("Auto-reload disabled")
        
    def reload_all(self) -> List[ReloadResult]:
        """
        Reload all watched modules
        
        Returns:
            List of reload results
        """
        results = []
        
        for module_name in list(self.watched_modules):
            result = self.reload_module(module_name)
            results.append(result)
            
        return results
        
    def get_watched_modules(self) -> Set[str]:
        """
        Get list of watched modules
        
        Returns:
            Set of module names
        """
        return self.watched_modules.copy()
        
    def get_module_info(self, module_name: str) -> Optional[Dict]:
        """
        Get module information
        
        Args:
            module_name: Module name
            
        Returns:
            Module info or None
        """
        if module_name not in sys.modules:
            return None
            
        module = sys.modules[module_name]
        info = {
            'name': module_name,
            'file': getattr(module, '__file__', None),
            'watched': module_name in self.watched_modules,
            'has_callbacks': module_name in self.reload_callbacks
        }
        
        if module.__file__:
            try:
                info['modified'] = os.path.getmtime(module.__file__)
            except:
                pass
                
        return info
        
    def clear_watched(self) -> None:
        """Clear all watched modules"""
        self.watched_modules.clear()
        self.module_timestamps.clear()
        self.logger.info("Cleared all watched modules")
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get hot reload statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'watched_modules': len(self.watched_modules),
            'auto_reload_enabled': self.auto_reload_enabled,
            'check_interval': self.check_interval,
            'callbacks': sum(len(cbs) for cbs in self.reload_callbacks.values())
        }


# Global hot reload manager instance
hot_reload_manager = HotReloadManager()
