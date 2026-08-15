"""
 ============================================================
  MODULE/PLUGIN NAME: CommandRegistry
  VERSION: 1.0.0
  MODULE CLASS: CommandRegistry
  DESCRIPTION:
       Terminal command registry for TerminalX

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

from typing import Dict, Callable, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class CommandCategory(Enum):
    """Command categories"""
    SYSTEM = "system"
    FILE = "file"
    NETWORK = "network"
    AI = "ai"
    GUI = "gui"
    DEV = "dev"
    SECURITY = "security"
    MISC = "misc"


@dataclass
class CommandInfo:
    """Command information"""
    name: str
    description: str
    category: CommandCategory
    handler: Callable
    aliases: List[str]
    requires_auth: bool = False
    admin_only: bool = False


class CommandRegistry:
    """Registry for terminal commands"""
    
    def __init__(self):
        """Initialize command registry"""
        self.commands: Dict[str, CommandInfo] = {}
        self.aliases: Dict[str, str] = {}  # alias -> command name
        
    def register(self, command: CommandInfo) -> bool:
        """
        Register a command
        
        Args:
            command: Command information
            
        Returns:
            True if registered successfully
        """
        if command.name in self.commands:
            return False
            
        self.commands[command.name] = command
        
        # Register aliases
        for alias in command.aliases:
            self.aliases[alias] = command.name
            
        return True
        
    def unregister(self, name: str) -> bool:
        """
        Unregister a command
        
        Args:
            name: Command name
            
        Returns:
            True if unregistered successfully
        """
        if name not in self.commands:
            return False
            
        # Remove aliases
        command = self.commands[name]
        for alias in command.aliases:
            if alias in self.aliases:
                del self.aliases[alias]
                
        del self.commands[name]
        return True
        
    def get(self, name: str) -> Optional[CommandInfo]:
        """
        Get command by name or alias
        
        Args:
            name: Command name or alias
            
        Returns:
            Command info or None
        """
        # Check if it's an alias
        if name in self.aliases:
            name = self.aliases[name]
            
        return self.commands.get(name)
        
    def list_commands(self, category: Optional[CommandCategory] = None) -> List[CommandInfo]:
        """
        List all commands, optionally filtered by category
        
        Args:
            category: Optional category filter
            
        Returns:
            List of command info
        """
        if category:
            return [cmd for cmd in self.commands.values() if cmd.category == category]
        return list(self.commands.values())
        
    def search(self, query: str) -> List[CommandInfo]:
        """
        Search commands by name or description
        
        Args:
            query: Search query
            
        Returns:
            List of matching commands
        """
        query = query.lower()
        results = []
        
        for cmd in self.commands.values():
            if (query in cmd.name.lower() or 
                query in cmd.description.lower() or
                any(query in alias.lower() for alias in cmd.aliases)):
                results.append(cmd)
                
        return results
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics
        
        Returns:
            Statistics dictionary
        """
        category_counts = {}
        for cmd in self.commands.values():
            category = cmd.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
        return {
            'total_commands': len(self.commands),
            'total_aliases': len(self.aliases),
            'categories': category_counts
        }


# Global command registry instance
command_registry = CommandRegistry()
