"""
 ============================================================
  MODULE/PLUGIN NAME: VersionCommands
  VERSION: 1.0.0
  MODULE CLASS: VersionCommands
  DESCRIPTION:
       Version command handlers for TerminalX version management system

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
from typing import Dict, Any


class VersionCommands:
    """Version command handlers"""
    
    def __init__(self, version_module):
        self.version_module = version_module
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a version command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown version command: {command}',
            }
            
    async def cmd_version(self, *args) -> Dict[str, Any]:
        """Display full version (semver + build + tag)"""
        try:
            version = self.version_module.get_full_version()
            return {
                'success': True,
                'output': version,
                'version': version,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_semver(self, *args) -> Dict[str, Any]:
        """Display semver version (major.minor.patch)"""
        try:
            semver = self.version_module.get_semver()
            return {
                'success': True,
                'output': semver,
                'semver': semver,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_short(self, *args) -> Dict[str, Any]:
        """Display short version form"""
        try:
            short = self.version_module.format_short()
            return {
                'success': True,
                'output': short,
                'short': short,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_banner(self, *args) -> Dict[str, Any]:
        """Display centered blue gradient banner"""
        try:
            banner = self.version_module.format_banner()
            return {
                'success': True,
                'output': banner,
                'banner': banner,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Display human-readable version information"""
        try:
            info = self.version_module.format_human()
            return {
                'success': True,
                'output': info,
                'info': info,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_json(self, *args) -> Dict[str, Any]:
        """Display version information in JSON format (pretty)"""
        try:
            json_output = self.version_module.format_json(pretty=True)
            return {
                'success': True,
                'output': json_output,
                'json': json_output,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_json_compact(self, *args) -> Dict[str, Any]:
        """Display version information in JSON format (compact)"""
        try:
            json_output = self.version_module.format_json(pretty=False)
            return {
                'success': True,
                'output': json_output,
                'json': json_output,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_all(self, *args) -> Dict[str, Any]:
        """Display all version information (human + JSON)"""
        try:
            human = self.version_module.format_human()
            json_output = self.version_module.format_json(pretty=True)
            output = f"{human}\n\n{json_output}"
            return {
                'success': True,
                'output': output,
                'human': human,
                'json': json_output,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_set_build(self, *args) -> Dict[str, Any]:
        """Set build number"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: version set-build <build_number>',
            }
        
        try:
            build = int(args[0])
            self.version_module.set_build(build)
            return {
                'success': True,
                'output': f'Build number set to: {build}',
                'build': build,
            }
        except ValueError:
            return {
                'success': False,
                'error': 'Build number must be an integer',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_set_tag(self, *args) -> Dict[str, Any]:
        """Set version tag"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: version set-tag <tag> (e.g., alpha, beta, rc, stable)',
            }
        
        try:
            tag = args[0]
            self.version_module.set_tag(tag)
            return {
                'success': True,
                'output': f'Tag set to: {tag}',
                'tag': tag,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_set_modules(self, *args) -> Dict[str, Any]:
        """Set module count (auto-increment patch if >99)"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: version set-modules <count>',
            }
        
        try:
            count = int(args[0])
            self.version_module.set_module_count(count)
            return {
                'success': True,
                'output': f'Module count set to: {count}',
                'module_count': count,
            }
        except ValueError:
            return {
                'success': False,
                'error': 'Module count must be an integer',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_set_plugins(self, *args) -> Dict[str, Any]:
        """Set plugin count (auto-increment patch if >99)"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: version set-plugins <count>',
            }
        
        try:
            count = int(args[0])
            self.version_module.set_plugin_count(count)
            return {
                'success': True,
                'output': f'Plugin count set to: {count}',
                'plugin_count': count,
            }
        except ValueError:
            return {
                'success': False,
                'error': 'Plugin count must be an integer',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_update_counts(self, *args) -> Dict[str, Any]:
        """Update both module and plugin counts"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: version update-counts <module_count> <plugin_count>',
            }
        
        try:
            module_count = int(args[0])
            plugin_count = int(args[1])
            self.version_module.update_counts(module_count, plugin_count)
            return {
                'success': True,
                'output': f'Updated: modules={module_count}, plugins={plugin_count}',
                'module_count': module_count,
                'plugin_count': plugin_count,
            }
        except ValueError:
            return {
                'success': False,
                'error': 'Counts must be integers',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_commands(self, *args) -> Dict[str, Any]:
        """Display list of available version commands"""
        try:
            commands = self.version_module.get_commands()
            output_lines = ['Available version commands:']
            for cmd, desc in commands.items():
                output_lines.append(f'  {cmd} - {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'commands': commands,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_enable(self, *args) -> Dict[str, Any]:
        """Enable version module"""
        try:
            await self.version_module.enable()
            return {
                'success': True,
                'output': 'Version module enabled',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_disable(self, *args) -> Dict[str, Any]:
        """Disable version module"""
        try:
            await self.version_module.disable()
            return {
                'success': True,
                'output': 'Version module disabled',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
