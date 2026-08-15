"""
 ============================================================
  MODULE/PLUGIN NAME: Completion
  VERSION: 1.0.0
  MODULE CLASS: Completion
  DESCRIPTION:
       Command autocompletion for TerminalX

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

from typing import List, Optional, Set
from dataclasses import dataclass
from libs.command_registry import command_registry, CommandInfo


@dataclass
class CompletionContext:
    """Completion context"""
    input: str
    cursor_position: int
    command_parts: List[str]
    current_part: str


class CommandCompletion:
    """Command autocompletion system"""
    
    def __init__(self):
        """Initialize completion system"""
        self.command_history: List[str] = []
        self.custom_completions: Dict[str, List[str]] = {}
        
    def complete(self, context: CompletionContext) -> List[str]:
        """
        Get completions for current input
        
        Args:
            context: Completion context
            
        Returns:
            List of completion suggestions
        """
        if not context.command_parts:
            return self._get_all_commands()
            
        # First word - complete command names
        if len(context.command_parts) == 1:
            return self._complete_command_name(context.current_part)
            
        # Subsequent words - complete arguments
        command_name = context.command_parts[0]
        return self._complete_arguments(command_name, context.current_part)
        
    def _get_all_commands(self) -> List[str]:
        """Get all registered commands"""
        return list(command_registry.commands.keys())
        
    def _complete_command_name(self, partial: str) -> List[str]:
        """
        Complete command name
        
        Args:
            partial: Partial command name
            
        Returns:
            List of matching commands
        """
        partial = partial.lower()
        all_names = list(command_registry.commands.keys()) + list(command_registry.aliases.keys())
        return [name for name in all_names if name.startswith(partial)]
        
    def _complete_arguments(self, command_name: str, partial: str) -> List[str]:
        """
        Complete command arguments
        
        Args:
            command_name: Command name
            partial: Partial argument
            
        Returns:
            List of argument suggestions
        """
        # Check for custom completions
        if command_name in self.custom_completions:
            completions = self.custom_completions[command_name]
            partial_lower = partial.lower()
            return [c for c in completions if c.lower().startswith(partial_lower)]
            
        # Default file system completions
        if command_name in ['fs', 'file']:
            return self._complete_files(partial)
            
        # Default network completions
        if command_name in ['net', 'network']:
            return self._complete_network_args(partial)
            
        return []
        
    def _complete_files(self, partial: str) -> List[str]:
        """
        Complete file paths
        
        Args:
            partial: Partial path
            
        Returns:
            List of file completions
        """
        import os
        try:
            directory = os.path.dirname(partial) or '.'
            filename = os.path.basename(partial)
            
            if not os.path.exists(directory):
                return []
                
            items = []
            for item in os.listdir(directory):
                if item.lower().startswith(filename.lower()):
                    full_path = os.path.join(directory, item)
                    if os.path.isdir(full_path):
                        items.append(item + '/')
                    else:
                        items.append(item)
                        
            return items
        except Exception:
            return []
            
    def _complete_network_args(self, partial: str) -> List[str]:
        """
        Complete network arguments
        
        Args:
            partial: Partial argument
            
        Returns:
            List of network argument completions
        """
        network_args = [
            'ping', 'traceroute', 'trace', 'nslookup', 'dig', 'whois',
            'curl', 'wget', 'http', 'tcping', 'speedtest', 'netinfo',
            'ipconfig', 'ifconfig', 'netstat', 'route', 'arp', 'scan',
            'portscan', 'wifi', 'lan', 'wlan', 'ethernet', 'ssh', 'scp',
            'ftp', 'sftp', 'telnet', 'mqtt', 'websocket', 'proxy',
            'vpn', 'dns', 'geoip', 'publicip', 'cloud'
        ]
        partial_lower = partial.lower()
        return [arg for arg in network_args if arg.startswith(partial_lower)]
        
    def add_custom_completion(self, command: str, completions: List[str]) -> None:
        """
        Add custom completions for a command
        
        Args:
            command: Command name
            completions: List of completion strings
        """
        self.custom_completions[command] = completions
        
    def add_to_history(self, command: str) -> None:
        """
        Add command to history
        
        Args:
            command: Command string
        """
        if command and command not in self.command_history[-10:]:
            self.command_history.append(command)
            
    def get_history_completions(self, partial: str) -> List[str]:
        """
        Get completions from history
        
        Args:
            partial: Partial command
            
        Returns:
            List of matching history commands
        """
        partial_lower = partial.lower()
        return [cmd for cmd in reversed(self.command_history) 
                if cmd.lower().startswith(partial_lower)]
        
    def get_stats(self) -> dict:
        """
        Get completion statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'history_size': len(self.command_history),
            'custom_completions': len(self.custom_completions)
        }


# Global completion instance
command_completion = CommandCompletion()
