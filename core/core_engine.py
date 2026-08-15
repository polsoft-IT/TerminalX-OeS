"""
 ============================================================
  MODULE/PLUGIN NAME: CoreEngine
  VERSION: 1.0.0
  MODULE CLASS: CoreEngine
  DESCRIPTION:
       Main coordination engine for all TerminalX subsystems

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
from typing import Dict, Any, Optional
from .event_bus import EventBus
from .config import Config
from .logger import Logger
from .runtime import Runtime
from .scheduler import Scheduler
from .notification import NotificationSystem, NotificationType, NotificationPriority


class CoreEngine:
    """Main coordination engine for TerminalX"""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.config = Config()
        self.logger = Logger()
        self.runtime = Runtime()
        self.scheduler = Scheduler()
        self.notification_system = NotificationSystem()
        self.subsystems: Dict[str, Any] = {}
        self.running = False
        
    async def initialize(self):
        """Initialize core engine and load configuration"""
        self.logger.info("Initializing Core Engine...")
        
        # Load configuration
        await self.config.load()
        
        # Initialize event bus
        await self.event_bus.initialize()
        
        # Initialize scheduler
        await self.scheduler.initialize()
        
        # Initialize runtime
        await self.runtime.initialize()
        
        # Initialize notification system
        await self.notification_system.initialize()
        
        self.logger.info("Core Engine initialized successfully")
        
    async def register_subsystem(self, name: str, subsystem: Any):
        """Register a subsystem with the core engine"""
        self.subsystems[name] = subsystem
        await self.event_bus.emit('subsystem.registered', {'name': name})
        self.logger.info(f"Subsystem registered: {name}")
        
    async def get_subsystem(self, name: str) -> Optional[Any]:
        """Get a registered subsystem"""
        return self.subsystems.get(name)
        
    async def start(self):
        """Start the core engine and all subsystems"""
        self.logger.info("Starting Core Engine...")
        self.running = True
        
        # Start scheduler
        await self.scheduler.start()
        
        # Emit start event
        await self.event_bus.emit('core.started', {})
        
        self.logger.info("Core Engine started")
        
    async def stop(self):
        """Stop the core engine and all subsystems"""
        self.logger.info("Stopping Core Engine...")
        self.running = False
        
        # Stop scheduler
        await self.scheduler.stop()
        
        # Shutdown notification system
        await self.notification_system.shutdown()
        
        # Emit stop event
        await self.event_bus.emit('core.stopped', {})
        
        self.logger.info("Core Engine stopped")
        
    async def run(self):
        """Main run loop"""
        await self.initialize()
        await self.start()
        
        try:
            while self.running:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        finally:
            await self.stop()
