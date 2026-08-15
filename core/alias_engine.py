"""
 ============================================================
  MODULE/PLUGIN NAME: AliasEngine
  VERSION: 5.0.0
  MODULE CLASS: AliasEngine
  DESCRIPTION:
       Advanced GODMODE v5 alias management system for TerminalX OeS.
       Provides comprehensive alias creation, editing, deletion, handling,
       management, and registration capabilities.

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

import os
import json
import re
import asyncio
from typing import Dict, List, Optional, Set, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from collections import defaultdict


@dataclass
class Alias:
    """Alias data structure"""
    name: str
    command: str
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    modified: str = field(default_factory=lambda: datetime.now().isoformat())
    enabled: bool = True
    description: str = ""
    usage_count: int = 0
    category: str = "custom"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Alias':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class CommandInfo:
    """Command information"""
    name: str
    module: str
    file_path: str
    line_number: int
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class AliasEngine:
    """Advanced GODMODE v5 Alias Management Engine"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize AliasEngine
        
        Args:
            config_dir: Configuration directory for alias storage
        """
        self.config_dir = config_dir or Path.home() / ".terminalx" / "aliases"
        self.aliases_file = self.config_dir / "aliases.json"
        self.commands_file = self.config_dir / "commands.json"
        
        self.aliases: Dict[str, Alias] = {}
        self.registered_aliases: Set[str] = set()
        self.available_commands: Dict[str, CommandInfo] = {}
        self.alias_handlers: Dict[str, Callable] = {}
        
        self._init_directories()
        self._load_aliases()
        
    def _init_directories(self) -> None:
        """Initialize configuration directories"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_aliases(self) -> None:
        """Load aliases from file"""
        if self.aliases_file.exists():
            try:
                with open(self.aliases_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for alias_name, alias_data in data.items():
                        self.aliases[alias_name] = Alias.from_dict(alias_data)
                        if alias_data.get('enabled', True):
                            self.registered_aliases.add(alias_name)
            except Exception as e:
                print(f"Error loading aliases: {e}")
    
    def _save_aliases(self) -> None:
        """Save aliases to file"""
        try:
            data = {name: alias.to_dict() for name, alias in self.aliases.items()}
            with open(self.aliases_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving aliases: {e}")
    
    def scan_project_commands(self, project_dir: Optional[str] = None) -> Dict[str, CommandInfo]:
        """
        Scan project directory for available commands
        
        Args:
            project_dir: Project directory to scan (defaults to current directory)
            
        Returns:
            Dictionary of command information
        """
        if project_dir is None:
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.available_commands = {}
        
        # Scan commands directory
        commands_dir = Path(project_dir) / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.py"):
                if cmd_file.name.startswith("_"):
                    continue
                    
                self._scan_command_file(cmd_file, "commands")
        
        # Scan libs directory for command-like modules
        libs_dir = Path(project_dir) / "libs"
        if libs_dir.exists():
            for lib_file in libs_dir.glob("*.py"):
                if lib_file.name.startswith("_"):
                    continue
                self._scan_command_file(lib_file, "libs")
        
        # Save commands to file
        self._save_commands()
        
        return self.available_commands
    
    def _scan_command_file(self, file_path: Path, module: str) -> None:
        """Scan a single command file for commands"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                content = ''.join(lines)
                
            # Find class definitions
            class_pattern = r'class\s+(\w+Commands?)'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                command_name = class_name.lower().replace('commands', '').replace('command', '')
                if command_name:
                    # Calculate line number from character position
                    char_pos = match.start()
                    line_number = content[:char_pos].count('\n') + 1
                    self.available_commands[command_name] = CommandInfo(
                        name=command_name,
                        module=module,
                        file_path=str(file_path),
                        line_number=line_number,
                        description=f"Command from {class_name}"
                    )
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
    
    def _save_commands(self) -> None:
        """Save available commands to file"""
        try:
            data = {name: cmd.to_dict() for name, cmd in self.available_commands.items()}
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving commands: {e}")
    
    def list_aliases(self, show_disabled: bool = False) -> List[Alias]:
        """
        List all aliases
        
        Args:
            show_disabled: Include disabled aliases
            
        Returns:
            List of aliases
        """
        if show_disabled:
            return list(self.aliases.values())
        return [alias for alias in self.aliases.values() if alias.enabled]
    
    def add_alias(self, command: str, alias_name: str, description: str = "", category: str = "custom") -> bool:
        """
        Add a new alias
        
        Args:
            command: Target command
            alias_name: Alias name
            description: Alias description
            category: Alias category
            
        Returns:
            True if successful
        """
        if alias_name in self.aliases:
            return False
            
        self.aliases[alias_name] = Alias(
            name=alias_name,
            command=command,
            description=description,
            category=category
        )
        
        if self.aliases[alias_name].enabled:
            self.registered_aliases.add(alias_name)
        
        self._save_aliases()
        return True
    
    def delete_alias(self, alias_name: str) -> bool:
        """
        Delete an alias
        
        Args:
            alias_name: Alias name to delete
            
        Returns:
            True if successful
        """
        if alias_name not in self.aliases:
            return False
            
        del self.aliases[alias_name]
        self.registered_aliases.discard(alias_name)
        self._save_aliases()
        return True
    
    def edit_alias(self, old_alias: str, new_alias: str) -> bool:
        """
        Edit an alias name
        
        Args:
            old_alias: Current alias name
            new_alias: New alias name
            
        Returns:
            True if successful
        """
        if old_alias not in self.aliases:
            return False
        if new_alias in self.aliases:
            return False
            
        # Move alias to new name
        alias_data = self.aliases[old_alias]
        alias_data.name = new_alias
        alias_data.modified = datetime.now().isoformat()
        
        self.aliases[new_alias] = alias_data
        del self.aliases[old_alias]
        
        # Update registered aliases
        self.registered_aliases.discard(old_alias)
        if alias_data.enabled:
            self.registered_aliases.add(new_alias)
        
        self._save_aliases()
        return True
    
    def register_alias(self, alias_name: str) -> bool:
        """
        Register a single alias
        
        Args:
            alias_name: Alias name to register
            
        Returns:
            True if successful
        """
        if alias_name not in self.aliases:
            return False
            
        self.aliases[alias_name].enabled = True
        self.registered_aliases.add(alias_name)
        self._save_aliases()
        return True
    
    def register_all(self) -> int:
        """
        Register all aliases
        
        Returns:
            Number of aliases registered
        """
        count = 0
        for alias_name in self.aliases:
            if alias_name not in self.registered_aliases:
                self.aliases[alias_name].enabled = True
                self.registered_aliases.add(alias_name)
                count += 1
        
        self._save_aliases()
        return count
    
    def unregister_alias(self, alias_name: str) -> bool:
        """
        Unregister a single alias
        
        Args:
            alias_name: Alias name to unregister
            
        Returns:
            True if successful
        """
        if alias_name not in self.aliases:
            return False
            
        self.aliases[alias_name].enabled = False
        self.registered_aliases.discard(alias_name)
        self._save_aliases()
        return True
    
    def unregister_all(self) -> int:
        """
        Unregister all aliases
        
        Returns:
            Number of aliases unregistered
        """
        count = 0
        for alias_name in list(self.registered_aliases):
            self.aliases[alias_name].enabled = False
            self.registered_aliases.remove(alias_name)
            count += 1
        
        self._save_aliases()
        return count
    
    def get_alias(self, alias_name: str) -> Optional[Alias]:
        """
        Get alias information
        
        Args:
            alias_name: Alias name
            
        Returns:
            Alias object or None
        """
        return self.aliases.get(alias_name)
    
    def resolve_alias(self, alias_name: str) -> Optional[str]:
        """
        Resolve alias to command
        
        Args:
            alias_name: Alias name
            
        Returns:
            Command string or None
        """
        alias = self.aliases.get(alias_name)
        if alias and alias.enabled:
            alias.usage_count += 1
            self._save_aliases()
            return alias.command
        return None
    
    def test_alias(self, alias_name: str) -> Dict[str, Any]:
        """
        Test an alias
        
        Args:
            alias_name: Alias name to test
            
        Returns:
            Test results
        """
        alias = self.aliases.get(alias_name)
        if not alias:
            return {
                'success': False,
                'error': f'Alias {alias_name} not found'
            }
        
        command = self.resolve_alias(alias_name)
        if not command:
            return {
                'success': False,
                'error': f'Alias {alias_name} is disabled or invalid'
            }
        
        return {
            'success': True,
            'alias': alias_name,
            'command': command,
            'enabled': alias.enabled,
            'usage_count': alias.usage_count,
            'category': alias.category
        }
    
    def test_all_aliases(self) -> Dict[str, Any]:
        """
        Test all aliases
        
        Returns:
            Test results for all aliases
        """
        results = {
            'total': len(self.aliases),
            'enabled': len(self.registered_aliases),
            'disabled': len(self.aliases) - len(self.registered_aliases),
            'results': {}
        }
        
        for alias_name in self.aliases:
            results['results'][alias_name] = self.test_alias(alias_name)
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get alias statistics
        
        Returns:
            Statistics dictionary
        """
        categories = defaultdict(int)
        total_usage = 0
        
        for alias in self.aliases.values():
            categories[alias.category] += 1
            total_usage += alias.usage_count
        
        return {
            'total_aliases': len(self.aliases),
            'registered_aliases': len(self.registered_aliases),
            'disabled_aliases': len(self.aliases) - len(self.registered_aliases),
            'total_usage': total_usage,
            'categories': dict(categories),
            'available_commands': len(self.available_commands)
        }
    
    def export_aliases(self, file_path: str) -> bool:
        """
        Export aliases to file
        
        Args:
            file_path: Export file path
            
        Returns:
            True if successful
        """
        try:
            data = {
                'aliases': {name: alias.to_dict() for name, alias in self.aliases.items()},
                'exported_at': datetime.now().isoformat(),
                'version': '5.0.0'
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting aliases: {e}")
            return False
    
    def import_aliases(self, file_path: str, overwrite: bool = False) -> int:
        """
        Import aliases from file
        
        Args:
            file_path: Import file path
            overwrite: Overwrite existing aliases
            
        Returns:
            Number of aliases imported
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            count = 0
            for alias_name, alias_data in data.get('aliases', {}).items():
                if alias_name not in self.aliases or overwrite:
                    self.aliases[alias_name] = Alias.from_dict(alias_data)
                    if self.aliases[alias_name].enabled:
                        self.registered_aliases.add(alias_name)
                    count += 1
            
            self._save_aliases()
            return count
        except Exception as e:
            print(f"Error importing aliases: {e}")
            return 0
    
    def clear_all_aliases(self) -> int:
        """
        Clear all aliases
        
        Returns:
            Number of aliases cleared
        """
        count = len(self.aliases)
        self.aliases.clear()
        self.registered_aliases.clear()
        self._save_aliases()
        return count
    
    def search_aliases(self, pattern: str) -> List[Alias]:
        """
        Search aliases by pattern
        
        Args:
            pattern: Search pattern
            
        Returns:
            List of matching aliases
        """
        pattern_lower = pattern.lower()
        results = []
        
        for alias in self.aliases.values():
            if (pattern_lower in alias.name.lower() or 
                pattern_lower in alias.command.lower() or
                pattern_lower in alias.description.lower()):
                results.append(alias)
        
        return results
    
    def set_handler(self, alias_name: str, handler: Callable) -> bool:
        """
        Set custom handler for alias
        
        Args:
            alias_name: Alias name
            handler: Handler function
            
        Returns:
            True if successful
        """
        if alias_name not in self.aliases:
            return False
        
        self.alias_handlers[alias_name] = handler
        return True
    
    def get_handler(self, alias_name: str) -> Optional[Callable]:
        """
        Get custom handler for alias
        
        Args:
            alias_name: Alias name
            
        Returns:
            Handler function or None
        """
        return self.alias_handlers.get(alias_name)
