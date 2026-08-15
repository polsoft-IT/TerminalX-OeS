"""
 ============================================================
  MODULE/PLUGIN NAME: ReportCommands
  VERSION: 1.0.0
  MODULE CLASS: ReportCommands
  DESCRIPTION:
       Report command handlers for TerminalX report engine system

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
import os
from typing import Dict, Any


class ReportCommands:
    """Report command handlers"""
    
    def __init__(self, report_engine):
        self.report_engine = report_engine
        self.reports = {}  # Store created reports by ID
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a report command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown report command: {command}',
            }
            
    async def cmd_create(self, *args) -> Dict[str, Any]:
        """Create a new report"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: report create <title>',
            }
        
        title = ' '.join(args)
        
        try:
            report = self.report_engine.create_report(title)
            self.reports[report.id] = report
            return {
                'success': True,
                'output': f'Report created: {report.id} - {title}',
                'report_id': report.id,
                'title': title,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_template(self, *args) -> Dict[str, Any]:
        """Generate report from template"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: report template <template_name> [json_data]',
            }
        
        template_name = args[0]
        data = {}
        
        # Try to load JSON data from argument or file
        if len(args) > 1:
            json_arg = ' '.join(args[1:])
            if os.path.isfile(json_arg):
                try:
                    with open(json_arg, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception as e:
                    return {
                        'success': False,
                        'error': f'Failed to load JSON file: {e}',
                    }
            else:
                try:
                    data = json.loads(json_arg)
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': 'Invalid JSON data provided',
                    }
        
        try:
            report = self.report_engine.from_template(template_name, data)
            self.reports[report.id] = report
            return {
                'success': True,
                'output': f'Report generated from template: {report.id} - {report.title}',
                'report_id': report.id,
                'title': report.title,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_render(self, *args) -> Dict[str, Any]:
        """Render report to specific format"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: report render <report_id> <format> (txt, md, json)',
            }
        
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: report render <report_id> <format> (txt, md, json)',
            }
        
        report_id = args[0]
        fmt = args[1]
        
        if report_id not in self.reports:
            return {
                'success': False,
                'error': f'Report not found: {report_id}',
            }
        
        report = self.reports[report_id]
        
        try:
            output_bytes = self.report_engine.render(report, fmt)
            output = output_bytes.decode('utf-8')
            
            return {
                'success': True,
                'output': f'Report rendered to {fmt} format',
                'report_id': report_id,
                'format': fmt,
                'content': output,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_save(self, *args) -> Dict[str, Any]:
        """Save report to file"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: report save <report_id> <filepath> [format]',
            }
        
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: report save <report_id> <filepath> [format]',
            }
        
        report_id = args[0]
        filepath = args[1]
        fmt = args[2] if len(args) > 2 else None
        
        if report_id not in self.reports:
            return {
                'success': False,
                'error': f'Report not found: {report_id}',
            }
        
        report = self.reports[report_id]
        
        try:
            saved_path = self.report_engine.save_to_file(report, filepath, fmt)
            return {
                'success': True,
                'output': f'Report saved to: {saved_path}',
                'report_id': report_id,
                'filepath': saved_path,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_display(self, *args) -> Dict[str, Any]:
        """Display report in terminal"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: report display <report_id> [format]',
            }
        
        report_id = args[0]
        fmt = args[1] if len(args) > 1 else None
        
        if report_id not in self.reports:
            return {
                'success': False,
                'error': f'Report not found: {report_id}',
            }
        
        report = self.reports[report_id]
        
        try:
            self.report_engine.display_in_terminal(report, fmt=fmt)
            return {
                'success': True,
                'output': f'Report displayed: {report.title}',
                'report_id': report_id,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_plugins(self, *args) -> Dict[str, Any]:
        """List available plugins"""
        try:
            output_lines = ['Available plugins:']
            
            # Template plugins
            template_plugins = self.report_engine.registry.get_template_plugins()
            if template_plugins:
                output_lines.append('\nTemplate Plugins:')
                for plugin in template_plugins:
                    output_lines.append(f'  - {plugin.name} v{plugin.version}: {plugin.description}')
            
            # Output plugins
            output_plugins = self.report_engine.registry.get_output_plugins()
            if output_plugins:
                output_lines.append('\nOutput Plugins:')
                for plugin in output_plugins:
                    formats = ', '.join(plugin.supported_formats())
                    output_lines.append(f'  - {plugin.name} v{plugin.version}: {plugin.description} (formats: {formats})')
            
            # Filter plugins
            filter_plugins = self.report_engine.registry.get_filter_plugins()
            if filter_plugins:
                output_lines.append('\nFilter Plugins:')
                for plugin in filter_plugins:
                    output_lines.append(f'  - {plugin.name} v{plugin.version}: {plugin.description}')
            
            # Post-process plugins
            postprocess_plugins = self.report_engine.registry.get_postprocess_plugins()
            if postprocess_plugins:
                output_lines.append('\nPost-Process Plugins:')
                for plugin in postprocess_plugins:
                    output_lines.append(f'  - {plugin.name} v{plugin.version}: {plugin.description}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_formats(self, *args) -> Dict[str, Any]:
        """List supported output formats"""
        try:
            output_plugins = self.report_engine.registry.get_output_plugins()
            formats = set()
            
            for plugin in output_plugins:
                formats.update(plugin.supported_formats())
            
            output_lines = ['Supported output formats:']
            for fmt in sorted(formats):
                output_lines.append(f'  - {fmt}')
            
            output_lines.append(f'\nDefault format: {self.report_engine.config.default_format}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'formats': sorted(formats),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List all created reports"""
        try:
            if not self.reports:
                return {
                    'success': True,
                    'output': 'No reports created yet',
                    'reports': [],
                }
            
            output_lines = ['Created reports:']
            for report_id, report in self.reports.items():
                output_lines.append(f'  - {report_id}: {report.title}')
                output_lines.append(f'    Created: {report.created_at}')
                output_lines.append(f'    Sections: {len(report.sections)}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'reports': list(self.reports.keys()),
                'count': len(self.reports),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_add_section(self, *args) -> Dict[str, Any]:
        """Add section to existing report"""
        if len(args) < 3:
            return {
                'success': False,
                'error': 'Usage: report add_section <report_id> <title> <content> [level]',
            }
        
        report_id = args[0]
        title = args[1]
        content = ' '.join(args[2:-1]) if len(args) > 3 else args[2]
        level = int(args[-1]) if len(args) > 3 and args[-1].isdigit() else 1
        
        if report_id not in self.reports:
            return {
                'success': False,
                'error': f'Report not found: {report_id}',
            }
        
        report = self.reports[report_id]
        
        try:
            section = report.add_section(title, content, level=level)
            return {
                'success': True,
                'output': f'Section added to report: {section.id}',
                'section_id': section.id,
                'report_id': report_id,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_enable(self, *args) -> Dict[str, Any]:
        """Enable report engine"""
        try:
            await self.report_engine.enable()
            return {
                'success': True,
                'output': 'Report engine enabled',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_disable(self, *args) -> Dict[str, Any]:
        """Disable report engine"""
        try:
            await self.report_engine.disable()
            return {
                'success': True,
                'output': 'Report engine disabled',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_commands(self, *args) -> Dict[str, Any]:
        """Display list of available report commands"""
        try:
            commands = self.report_engine.get_commands()
            output_lines = ['Available report commands:']
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
