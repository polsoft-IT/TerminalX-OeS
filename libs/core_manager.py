"""
 ============================================================
  MODULE/PLUGIN NAME: CoreManager
  VERSION: 1.0.0
  MODULE CLASS: CoreManager
  DESCRIPTION:
       Terminal core management for TerminalX

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
import sys
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class CoreState(Enum):
    """Core states"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class SubsystemInfo:
    """Subsystem information"""
    name: str
    instance: Any
    initialized: bool = False
    started: bool = False
    priority: int = 0


class CoreManager:
    """Terminal core management system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize core manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("CoreManager", LogLevel.INFO)
        self.state = CoreState.STOPPED
        self.subsystems: Dict[str, SubsystemInfo] = {}
        self.notification_callback: Optional[Callable] = None
        self.startup_tasks: List[Callable] = []
        self.shutdown_tasks: List[Callable] = []
        
    def set_notification_callback(self, callback: Callable) -> None:
        """
        Set notification callback
        
        Args:
            callback: Notification callback function
        """
        self.notification_callback = callback
        
    def _notify(self, title: str, message: str, level: str = "info") -> None:
        """
        Send notification
        
        Args:
            title: Notification title
            message: Notification message
            level: Notification level
        """
        if self.notification_callback:
            self.notification_callback(title, message, level, "normal")
            
    def register_subsystem(self, name: str, instance: Any, priority: int = 0) -> bool:
        """
        Register a subsystem
        
        Args:
            name: Subsystem name
            instance: Subsystem instance
            priority: Priority (higher = earlier initialization)
            
        Returns:
            True if registered successfully
        """
        if name in self.subsystems:
            self.logger.warning(f"Subsystem {name} already registered")
            return False
            
        self.subsystems[name] = SubsystemInfo(
            name=name,
            instance=instance,
            priority=priority
        )
        
        self.logger.info(f"Registered subsystem: {name}")
        return True
        
    def unregister_subsystem(self, name: str) -> bool:
        """
        Unregister a subsystem
        
        Args:
            name: Subsystem name
            
        Returns:
            True if unregistered successfully
        """
        if name not in self.subsystems:
            return False
            
        subsystem = self.subsystems[name]
        
        # Stop if running
        if subsystem.started:
            self._stop_subsystem(subsystem)
            
        del self.subsystems[name]
        self.logger.info(f"Unregistered subsystem: {name}")
        return True
        
    def get_subsystem(self, name: str) -> Optional[Any]:
        """
        Get subsystem instance
        
        Args:
            name: Subsystem name
            
        Returns:
            Subsystem instance or None
        """
        subsystem = self.subsystems.get(name)
        return subsystem.instance if subsystem else None
        
    async def initialize_all(self) -> bool:
        """
        Initialize all subsystems
        
        Returns:
            True if all initialized successfully
        """
        self.state = CoreState.STARTING
        self.logger.info("Initializing core subsystems...")
        
        # Sort by priority (higher first)
        sorted_subsystems = sorted(
            self.subsystems.values(),
            key=lambda x: x.priority,
            reverse=True
        )
        
        for subsystem in sorted_subsystems:
            if not subsystem.initialized:
                try:
                    if hasattr(subsystem.instance, 'initialize'):
                        await subsystem.instance.initialize()
                    subsystem.initialized = True
                    self.logger.info(f"Initialized: {subsystem.name}")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {subsystem.name}: {e}")
                    self.state = CoreState.ERROR
                    return False
                    
        self.state = CoreState.RUNNING
        self.logger.info("All subsystems initialized")
        return True
        
    async def start_all(self) -> bool:
        """
        Start all subsystems
        
        Returns:
            True if all started successfully
        """
        self.logger.info("Starting core subsystems...")
        
        for subsystem in self.subsystems.values():
            if subsystem.initialized and not subsystem.started:
                try:
                    if hasattr(subsystem.instance, 'start'):
                        await subsystem.instance.start()
                    subsystem.started = True
                    self.logger.info(f"Started: {subsystem.name}")
                except Exception as e:
                    self.logger.error(f"Failed to start {subsystem.name}: {e}")
                    
        # Run startup tasks
        for task in self.startup_tasks:
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
            except Exception as e:
                self.logger.error(f"Startup task failed: {e}")
                
        self.logger.info("All subsystems started")
        return True
        
    async def stop_all(self) -> bool:
        """
        Stop all subsystems
        
        Returns:
            True if all stopped successfully
        """
        self.state = CoreState.STOPPING
        self.logger.info("Stopping core subsystems...")
        
        # Run shutdown tasks
        for task in self.shutdown_tasks:
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
            except Exception as e:
                self.logger.error(f"Shutdown task failed: {e}")
                
        # Stop subsystems in reverse priority order
        sorted_subsystems = sorted(
            self.subsystems.values(),
            key=lambda x: x.priority
        )
        
        for subsystem in sorted_subsystems:
            if subsystem.started:
                try:
                    self._stop_subsystem(subsystem)
                except Exception as e:
                    self.logger.error(f"Failed to stop {subsystem.name}: {e}")
                    
        self.state = CoreState.STOPPED
        self.logger.info("All subsystems stopped")
        return True
        
    def _stop_subsystem(self, subsystem: SubsystemInfo) -> None:
        """
        Stop a single subsystem
        
        Args:
            subsystem: Subsystem info
        """
        if hasattr(subsystem.instance, 'stop'):
            if asyncio.iscoroutinefunction(subsystem.instance.stop):
                asyncio.create_task(subsystem.instance.stop())
            else:
                subsystem.instance.stop()
        subsystem.started = False
        self.logger.info(f"Stopped: {subsystem.name}")
        
    def add_startup_task(self, task: Callable) -> None:
        """
        Add startup task
        
        Args:
            task: Startup task function
        """
        self.startup_tasks.append(task)
        
    def add_shutdown_task(self, task: Callable) -> None:
        """
        Add shutdown task
        
        Args:
            task: Shutdown task function
        """
        self.shutdown_tasks.append(task)
        
    def get_state(self) -> CoreState:
        """
        Get current core state
        
        Returns:
            Current state
        """
        return self.state
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get core status
        
        Returns:
            Status dictionary
        """
        return {
            'state': self.state.value,
            'subsystems': {
                name: {
                    'initialized': info.initialized,
                    'started': info.started,
                    'priority': info.priority
                }
                for name, info in self.subsystems.items()
            },
            'startup_tasks': len(self.startup_tasks),
            'shutdown_tasks': len(self.shutdown_tasks)
        }
        
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check
        
        Returns:
            Health check results
        """
        results = {}
        
        for name, subsystem in self.subsystems.items():
            if subsystem.started and hasattr(subsystem.instance, 'health_check'):
                try:
                    results[name] = subsystem.instance.health_check()
                except Exception as e:
                    results[name] = {'status': 'error', 'error': str(e)}
            else:
                results[name] = {
                    'status': 'running' if subsystem.started else 'stopped'
                }
                
        return {
            'overall': self.state.value,
            'subsystems': results
        }
        
    def restart_subsystem(self, name: str) -> bool:
        """
        Restart a subsystem
        
        Args:
            name: Subsystem name
            
        Returns:
            True if restarted successfully
        """
        subsystem = self.subsystems.get(name)
        if not subsystem:
            return False
            
        try:
            # Stop
            if subsystem.started:
                self._stop_subsystem(subsystem)
                
            # Start
            if hasattr(subsystem.instance, 'start'):
                if asyncio.iscoroutinefunction(subsystem.instance.start):
                    asyncio.create_task(subsystem.instance.start())
                else:
                    subsystem.instance.start()
                    
            subsystem.started = True
            self.logger.info(f"Restarted: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to restart {name}: {e}")
            return False


# Global core manager instance
core_manager = CoreManager()
