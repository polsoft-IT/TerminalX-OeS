"""
 ============================================================
  MODULE/PLUGIN NAME: AliasCommands
  VERSION: 5.0.0
  MODULE CLASS: AliasCommands
  DESCRIPTION:
       Command handlers for AliasEngine - GODMODE v5 alias management
       system for TerminalX OeS.

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
from typing import Dict, Any, Optional, List
from core import ANSI
from core.alias_engine import AliasEngine


class AliasCommands:
    """Alias command handlers for TerminalX"""
    
    def __init__(self, alias_engine: AliasEngine):
        """
        Initialize AliasCommands
        
        Args:
            alias_engine: AliasEngine instance
        """
        self.alias_engine = alias_engine
        self.version = "5.0.0"
    
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute an alias command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown alias command: {command}',
            }
    
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List all aliases"""
        show_disabled = '--disabled' in args or '-d' in args
        
        aliases = self.alias_engine.list_aliases(show_disabled=show_disabled)
        
        if not aliases:
            return {
                'success': True,
                'output': f'{ANSI.YELLOW}No aliases found.{ANSI.RESET}'
            }
        
        output = [f'{ANSI.CYAN}=== ALIAS LIST ({len(aliases)} total) ==={ANSI.RESET}\n']
        
        for alias in aliases:
            status = f'{ANSI.GREEN}✓{ANSI.RESET}' if alias.enabled else f'{ANSI.RED}✗{ANSI.RESET}'
            output.append(f'{status} {ANSI.BOLD}{alias.name}{ANSI.RESET} → {alias.command}')
            if alias.description:
                output.append(f'   {ANSI.BRIGHT_BLACK}└─ {alias.description}{ANSI.RESET}')
            output.append(f'   {ANSI.BRIGHT_BLACK}└─ Category: {alias.category} | Usage: {alias.usage_count}{ANSI.RESET}')
            output.append('')
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_cmd(self, *args) -> Dict[str, Any]:
        """Scan project and list all available commands"""
        project_dir = args[0] if args else None
        commands = self.alias_engine.scan_project_commands(project_dir)
        
        if not commands:
            return {
                'success': True,
                'output': f'{ANSI.YELLOW}No commands found.{ANSI.RESET}'
            }
        
        output = [f'{ANSI.CYAN}=== AVAILABLE COMMANDS ({len(commands)} total) ==={ANSI.RESET}\n']
        
        for cmd_name, cmd_info in commands.items():
            output.append(f'{ANSI.BOLD}{cmd_name}{ANSI.RESET}')
            output.append(f'   {ANSI.BRIGHT_BLACK}└─ Module: {cmd_info.module}{ANSI.RESET}')
            output.append(f'   {ANSI.BRIGHT_BLACK}└─ File: {cmd_info.file_path}:{cmd_info.line_number}{ANSI.RESET}')
            if cmd_info.description:
                output.append(f'   {ANSI.BRIGHT_BLACK}└─ {cmd_info.description}{ANSI.RESET}')
            output.append('')
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_add(self, *args) -> Dict[str, Any]:
        """Add a new alias: alias add <command> ; <alias> [description] [category]"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: alias add <command> ; <alias> [description] [category]'
            }
        
        # Parse command and alias (separated by ;)
        parts = ' '.join(args).split(';')
        if len(parts) < 2:
            return {
                'success': False,
                'error': 'Command and alias must be separated by ;'
            }
        
        command = parts[0].strip()
        alias_name = parts[1].strip()
        description = parts[2].strip() if len(parts) > 2 else ""
        category = parts[3].strip() if len(parts) > 3 else "custom"
        
        if self.alias_engine.add_alias(command, alias_name, description, category):
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Alias added: {alias_name} → {command}{ANSI.RESET}'
            }
        else:
            return {
                'success': False,
                'error': f'Alias {alias_name} already exists'
            }
    
    async def cmd_del(self, *args) -> Dict[str, Any]:
        """Delete an alias: alias del <alias>"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias del <alias>'
            }
        
        alias_name = args[0]
        
        if self.alias_engine.delete_alias(alias_name):
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Alias deleted: {alias_name}{ANSI.RESET}'
            }
        else:
            return {
                'success': False,
                'error': f'Alias {alias_name} not found'
            }
    
    async def cmd_edit(self, *args) -> Dict[str, Any]:
        """Edit an alias: alias edit <old_alias> ; <new_alias>"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: alias edit <old_alias> ; <new_alias>'
            }
        
        # Parse old and new alias (separated by ;)
        parts = ' '.join(args).split(';')
        if len(parts) < 2:
            return {
                'success': False,
                'error': 'Old and new alias must be separated by ;'
            }
        
        old_alias = parts[0].strip()
        new_alias = parts[1].strip()
        
        if self.alias_engine.edit_alias(old_alias, new_alias):
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Alias renamed: {old_alias} → {new_alias}{ANSI.RESET}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to rename alias {old_alias} to {new_alias}'
            }
    
    async def cmd_reg(self, *args) -> Dict[str, Any]:
        """Register alias(es): alias reg <alias> or alias reg all"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias reg <alias> or alias reg all'
            }
        
        target = args[0]
        
        if target == 'all':
            count = self.alias_engine.register_all()
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Registered {count} aliases{ANSI.RESET}'
            }
        else:
            if self.alias_engine.register_alias(target):
                return {
                    'success': True,
                    'output': f'{ANSI.GREEN}✓ Registered alias: {target}{ANSI.RESET}'
                }
            else:
                return {
                    'success': False,
                    'error': f'Alias {target} not found'
                }
    
    async def cmd_unreg(self, *args) -> Dict[str, Any]:
        """Unregister alias(es): alias unreg <alias> or alias unreg all"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias unreg <alias> or alias unreg all'
            }
        
        target = args[0]
        
        if target == 'all':
            count = self.alias_engine.unregister_all()
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Unregistered {count} aliases{ANSI.RESET}'
            }
        else:
            if self.alias_engine.unregister_alias(target):
                return {
                    'success': True,
                    'output': f'{ANSI.GREEN}✓ Unregistered alias: {target}{ANSI.RESET}'
                }
            else:
                return {
                    'success': False,
                    'error': f'Alias {target} not found'
                }
    
    async def cmd_test(self, *args) -> Dict[str, Any]:
        """Test an alias: alias test <alias>"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias test <alias>'
            }
        
        alias_name = args[0]
        result = self.alias_engine.test_alias(alias_name)
        
        if result['success']:
            output = [
                f'{ANSI.CYAN}=== ALIAS TEST: {alias_name} ==={ANSI.RESET}',
                f'{ANSI.GREEN}✓ Status: OK{ANSI.RESET}',
                f'Command: {result["command"]}',
                f'Enabled: {result["enabled"]}',
                f'Usage Count: {result["usage_count"]}',
                f'Category: {result["category"]}'
            ]
            return {
                'success': True,
                'output': '\n'.join(output)
            }
        else:
            return {
                'success': False,
                'error': result['error']
            }
    
    async def cmd_test_all(self, *args) -> Dict[str, Any]:
        """Test all aliases"""
        results = self.alias_engine.test_all_aliases()
        
        output = [
            f'{ANSI.CYAN}=== ALIAS TEST RESULTS ==={ANSI.RESET}',
            f'Total: {results["total"]}',
            f'Enabled: {results["enabled"]}',
            f'Disabled: {results["disabled"]}',
            ''
        ]
        
        for alias_name, result in results['results'].items():
            if result['success']:
                output.append(f'{ANSI.GREEN}✓{ANSI.RESET} {alias_name} → {result["command"]}')
            else:
                output.append(f'{ANSI.RED}✗{ANSI.RESET} {alias_name}: {result.get("error", "Unknown error")}')
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Show alias statistics"""
        stats = self.alias_engine.get_statistics()
        
        output = [
            f'{ANSI.CYAN}=== ALIAS STATISTICS ==={ANSI.RESET}',
            f'Total Aliases: {stats["total_aliases"]}',
            f'Registered: {stats["registered_aliases"]}',
            f'Disabled: {stats["disabled_aliases"]}',
            f'Total Usage: {stats["total_usage"]}',
            f'Available Commands: {stats["available_commands"]}',
            ''
        ]
        
        if stats['categories']:
            output.append(f'{ANSI.BOLD}Categories:{ANSI.RESET}')
            for category, count in stats['categories'].items():
                output.append(f'  {category}: {count}')
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_export(self, *args) -> Dict[str, Any]:
        """Export aliases: alias export <file_path>"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias export <file_path>'
            }
        
        file_path = args[0]
        
        if self.alias_engine.export_aliases(file_path):
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Aliases exported to: {file_path}{ANSI.RESET}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to export aliases to {file_path}'
            }
    
    async def cmd_import(self, *args) -> Dict[str, Any]:
        """Import aliases: alias import <file_path> [--overwrite]"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias import <file_path> [--overwrite]'
            }
        
        file_path = args[0]
        overwrite = '--overwrite' in args or '-o' in args
        
        count = self.alias_engine.import_aliases(file_path, overwrite)
        
        if count > 0:
            return {
                'success': True,
                'output': f'{ANSI.GREEN}✓ Imported {count} aliases from: {file_path}{ANSI.RESET}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to import aliases from {file_path}'
            }
    
    async def cmd_clear(self, *args) -> Dict[str, Any]:
        """Clear all aliases"""
        count = self.alias_engine.clear_all_aliases()
        
        return {
            'success': True,
            'output': f'{ANSI.GREEN}✓ Cleared {count} aliases{ANSI.RESET}'
        }
    
    async def cmd_search(self, *args) -> Dict[str, Any]:
        """Search aliases: alias search <pattern>"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias search <pattern>'
            }
        
        pattern = args[0]
        results = self.alias_engine.search_aliases(pattern)
        
        if not results:
            return {
                'success': True,
                'output': f'{ANSI.YELLOW}No aliases matching pattern: {pattern}{ANSI.RESET}'
            }
        
        output = [f'{ANSI.CYAN}=== SEARCH RESULTS ({len(results)} matches) ==={ANSI.RESET}\n']
        
        for alias in results:
            status = f'{ANSI.GREEN}✓{ANSI.RESET}' if alias.enabled else f'{ANSI.RED}✗{ANSI.RESET}'
            output.append(f'{status} {ANSI.BOLD}{alias.name}{ANSI.RESET} → {alias.command}')
            if alias.description:
                output.append(f'   {ANSI.BRIGHT_BLACK}└─ {alias.description}{ANSI.RESET}')
            output.append('')
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
    
    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Show alias information: alias info <alias>"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: alias info <alias>'
            }
        
        alias_name = args[0]
        alias = self.alias_engine.get_alias(alias_name)
        
        if not alias:
            return {
                'success': False,
                'error': f'Alias {alias_name} not found'
            }
        
        output = [
            f'{ANSI.CYAN}=== ALIAS INFO: {alias_name} ==={ANSI.RESET}',
            f'Command: {alias.command}',
            f'Description: {alias.description or "None"}',
            f'Category: {alias.category}',
            f'Enabled: {alias.enabled}',
            f'Usage Count: {alias.usage_count}',
            f'Created: {alias.created}',
            f'Modified: {alias.modified}'
        ]
        
        return {
            'success': True,
            'output': '\n'.join(output)
        }
