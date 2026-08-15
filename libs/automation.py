"""
 ============================================================
  MODULE/PLUGIN NAME: Automation
  VERSION: 1.0.0
  MODULE CLASS: Automation
  DESCRIPTION:
       Process and macro automation for TerminalX operations

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
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class Macro:
    """Macro definition"""
    name: str
    commands: List[str]
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()


@dataclass
class AutomationTask:
    """Automation task"""
    name: str
    command: str
    schedule: Optional[str] = None
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None


class AutomationEngine:
    """Process and macro automation engine"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize automation engine
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("AutomationEngine", LogLevel.INFO)
        self.macros: Dict[str, Macro] = {}
        self.tasks: Dict[str, AutomationTask] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.command_executor: Optional[Callable] = None
        
    def set_command_executor(self, executor: Callable) -> None:
        """
        Set command executor function
        
        Args:
            executor: Function to execute commands
        """
        self.command_executor = executor
        
    def create_macro(self, name: str, commands: List[str], description: str = "") -> bool:
        """
        Create a macro
        
        Args:
            name: Macro name
            commands: List of commands
            description: Macro description
            
        Returns:
            True if created successfully
        """
        if name in self.macros:
            self.logger.warning(f"Macro {name} already exists")
            return False
            
        self.macros[name] = Macro(
            name=name,
            commands=commands,
            description=description
        )
        
        self.logger.info(f"Created macro: {name}")
        return True
        
    def delete_macro(self, name: str) -> bool:
        """
        Delete a macro
        
        Args:
            name: Macro name
            
        Returns:
            True if deleted successfully
        """
        if name in self.macros:
            del self.macros[name]
            self.logger.info(f"Deleted macro: {name}")
            return True
        return False
        
    def get_macro(self, name: str) -> Optional[Macro]:
        """
        Get macro
        
        Args:
            name: Macro name
            
        Returns:
            Macro or None
        """
        return self.macros.get(name)
        
    def list_macros(self) -> List[Macro]:
        """
        List all macros
        
        Returns:
            List of macros
        """
        return list(self.macros.values())
        
    def execute_macro(self, name: str) -> bool:
        """
        Execute a macro
        
        Args:
            name: Macro name
            
        Returns:
            True if executed successfully
        """
        macro = self.macros.get(name)
        if not macro:
            self.logger.error(f"Macro {name} not found")
            return False
            
        if not self.command_executor:
            self.logger.error("No command executor set")
            return False
            
        try:
            for command in macro.commands:
                self.command_executor(command)
                
            macro.updated_at = datetime.now().isoformat()
            self.logger.info(f"Executed macro: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Macro execution failed: {e}")
            return False
            
    def create_task(self, name: str, command: str, schedule: Optional[str] = None) -> bool:
        """
        Create an automation task
        
        Args:
            name: Task name
            command: Command to execute
            schedule: Schedule (cron format or None for manual)
            
        Returns:
            True if created successfully
        """
        if name in self.tasks:
            self.logger.warning(f"Task {name} already exists")
            return False
            
        self.tasks[name] = AutomationTask(
            name=name,
            command=command,
            schedule=schedule
        )
        
        self.logger.info(f"Created task: {name}")
        return True
        
    def delete_task(self, name: str) -> bool:
        """
        Delete a task
        
        Args:
            name: Task name
            
        Returns:
            True if deleted successfully
        """
        if name in self.tasks:
            # Stop if running
            if name in self.running_tasks:
                self.running_tasks[name].cancel()
                del self.running_tasks[name]
                
            del self.tasks[name]
            self.logger.info(f"Deleted task: {name}")
            return True
        return False
        
    def enable_task(self, name: str) -> bool:
        """
        Enable a task
        
        Args:
            name: Task name
            
        Returns:
            True if enabled successfully
        """
        if name in self.tasks:
            self.tasks[name].enabled = True
            self.logger.info(f"Enabled task: {name}")
            return True
        return False
        
    def disable_task(self, name: str) -> bool:
        """
        Disable a task
        
        Args:
            name: Task name
            
        Returns:
            True if disabled successfully
        """
        if name in self.tasks:
            self.tasks[name].enabled = False
            self.logger.info(f"Disabled task: {name}")
            return True
        return False
        
    def execute_task(self, name: str) -> bool:
        """
        Execute a task
        
        Args:
            name: Task name
            
        Returns:
            True if executed successfully
        """
        task = self.tasks.get(name)
        if not task:
            self.logger.error(f"Task {name} not found")
            return False
            
        if not task.enabled:
            self.logger.warning(f"Task {name} is disabled")
            return False
            
        if not self.command_executor:
            self.logger.error("No command executor set")
            return False
            
        try:
            self.command_executor(task.command)
            task.last_run = datetime.now().isoformat()
            self.logger.info(f"Executed task: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            return False
            
    def list_tasks(self, enabled_only: bool = False) -> List[AutomationTask]:
        """
        List tasks
        
        Args:
            enabled_only: Only enabled tasks
            
        Returns:
            List of tasks
        """
        tasks = list(self.tasks.values())
        
        if enabled_only:
            tasks = [t for t in tasks if t.enabled]
            
        return tasks
        
    def import_macros(self, data: Dict[str, Any]) -> int:
        """
        Import macros from data
        
        Args:
            data: Macro data dictionary
            
        Returns:
            Number of imported macros
        """
        count = 0
        
        for name, macro_data in data.items():
            if name not in self.macros:
                self.macros[name] = Macro(
                    name=name,
                    commands=macro_data.get('commands', []),
                    description=macro_data.get('description', ''),
                    created_at=macro_data.get('created_at', datetime.now().isoformat()),
                    updated_at=macro_data.get('updated_at', datetime.now().isoformat())
                )
                count += 1
                
        self.logger.info(f"Imported {count} macros")
        return count
        
    def export_macros(self) -> Dict[str, Any]:
        """
        Export macros
        
        Returns:
            Macro data dictionary
        """
        return {name: {
            'commands': macro.commands,
            'description': macro.description,
            'created_at': macro.created_at,
            'updated_at': macro.updated_at
        } for name, macro in self.macros.items()}
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get automation statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'macros': len(self.macros),
            'tasks': len(self.tasks),
            'enabled_tasks': sum(1 for t in self.tasks.values() if t.enabled),
            'running_tasks': len(self.running_tasks)
        }


# Global automation engine instance
automation_engine = AutomationEngine()
