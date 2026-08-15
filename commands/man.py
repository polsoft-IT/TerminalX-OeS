"""
 ============================================================
  MODULE/PLUGIN NAME: ManCommands
  VERSION: 2.0.0
  MODULE CLASS: ManCommands
  DESCRIPTION:
       Enhanced man page command handlers v2 with category support, usage statistics, cross-references, quick reference, and advanced search commands

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
from core import ANSI


class ManCommands:
    """Man page command handlers"""
    
    def __init__(self, man_engine):
        self.man_engine = man_engine
    
    def _rpg_header(self, text: str) -> str:
        """Apply RPG-style effect to header text"""
        # Gold/yellow gradient effect like RPG game titles
        rpg_text = ANSI.gradient_custom(text, (255, 215, 0), (255, 140, 0))
        # Add stars decoration
        return f"{ANSI.BOLD}★★ {rpg_text} ★★{ANSI.RESET}"
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a man command"""
        # If no command provided, treat first arg as page name for direct access
        if not command and args:
            return await self.cmd_show(*args)
        
        handler = getattr(self, f'cmd_{command}', None)

        if handler:
            return await handler(*args)
        else:
            # If command is not a known subcommand, treat it as a page name
            return await self.cmd_show(command, *args)
            
    async def cmd_show(self, *args) -> Dict[str, Any]:
        """Show a man page or subcommand details"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man show <page_name> [section] or man show <page_name> <subcommand>',
            }
            
        page_name = args[0]
        section = None
        subcommand = None
        
        if len(args) > 1:
            try:
                section = int(args[1])
            except ValueError:
                # If second argument is not a number, treat it as a subcommand
                subcommand = args[1]
        
        try:
            if subcommand:
                # Try to show subcommand details from the main page
                page_content = await self.man_engine.display_page(page_name, section)
                
                # Extract subcommand-specific information
                subcommand_info = self._extract_subcommand_info(page_content, subcommand)
                
                if subcommand_info:
                    return {
                        'success': True,
                        'output': subcommand_info,
                        'page': page_name,
                        'subcommand': subcommand,
                    }
                else:
                    # Subcommand not found, show full page with suggestion
                    return {
                        'success': True,
                        'output': f"Subcommand '{subcommand}' not found in {page_name} man page. Showing full page instead:\n\n{page_content}",
                        'page': page_name,
                        'subcommand': subcommand,
                    }
            else:
                # Show full page
                page_content = await self.man_engine.display_page(page_name, section)
                return {
                    'success': True,
                    'output': page_content,
                    'page': page_name,
                    'section': section,
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    def _extract_subcommand_info(self, page_content: str, subcommand: str) -> str:
        """Extract specific subcommand information from man page"""
        lines = page_content.split('\n')
        result_lines = []
        found_subcommand = False
        in_options = False
        
        for line in lines:
            # Look for the subcommand in OPTIONS section
            if 'OPTIONS' in line:
                in_options = True
                continue
            
            if in_options:
                # Check if this line contains our subcommand
                if subcommand in line.lower():
                    found_subcommand = True
                    result_lines.append(line)
                    return '\n'.join(result_lines)
                
                # If we've moved past the options section without finding the subcommand
                if line.strip() and not line.strip().startswith('-') and 'EXAMPLES' in line:
                    break
        
        return None if not found_subcommand else '\n'.join(result_lines)
    
    async def cmd_wildcard(self, *args) -> Dict[str, Any]:
        """Search using wildcard patterns"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man wildcard <pattern> (e.g., "net*", "*wifi*")',
            }
        
        pattern = args[0]
        
        try:
            results = await self.man_engine.search_wildcard(pattern)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No matches for wildcard pattern: {pattern}',
                    'pattern': pattern,
                    'results': {},
                }
            
            output_lines = [f'Matches for wildcard pattern: {pattern}']
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'pattern': pattern,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_fuzzy(self, *args) -> Dict[str, Any]:
        """Fuzzy search in names and descriptions"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man fuzzy <term>',
            }
        
        term = args[0]
        
        try:
            results = await self.man_engine.search_fuzzy(term)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No fuzzy matches for: {term}',
                    'term': term,
                    'results': {},
                }
            
            output_lines = [f'Fuzzy matches for: {term}']
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'term': term,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_rebuild(self, *args) -> Dict[str, Any]:
        """Rebuild cache from all sources"""
        try:
            await self.man_engine.rebuild_cache()
            
            return {
                'success': True,
                'output': 'Cache rebuilt successfully from all sources (META, PKG, MAN, INFO)',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_source_stats(self, *args) -> Dict[str, Any]:
        """Get statistics for all data sources"""
        try:
            stats = await self.man_engine.get_source_stats()
            
            output_lines = ['Source Statistics:']
            for source, stat in stats['sources'].items():
                if isinstance(stat, dict):
                    output_lines.append(f'  {source.upper()}: {stat.get("count", 0)} entries (load time: {stat.get("load_time", 0):.3f}s)')
            
            output_lines.append(f'\nTotal entries: {stats["total_entries"]}')
            output_lines.append(f'Source priority: {" > ".join(stats["source_priority"])}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'stats': stats,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_search(self, *args) -> Dict[str, Any]:
        """Search for man pages"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man search <query>',
            }
            
        query = ' '.join(args)
        
        try:
            results = await self.man_engine.search(query)
            return {
                'success': True,
                'output': f"Search results for '{query}' ({len(results)} found):\n" + "\n".join(f"  - {result}" for result in results),
                'query': query,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List available man pages"""
        section = None
        if args:
            try:
                section = int(args[0])
            except ValueError:
                return {
                    'success': False,
                    'error': f'Invalid section number: {args[0]}. Section must be an integer.',
                }
        
        try:
            pages = await self.man_engine.list_pages(section)
            
            # Format output in 3 columns
            num_columns = 3
            max_width = 30  # max width for each column
            
            # Calculate number of rows needed
            num_rows = (len(pages) + num_columns - 1) // num_columns
            
            # Build columns
            columns = []
            for i in range(num_columns):
                start_idx = i * num_rows
                end_idx = min(start_idx + num_rows, len(pages))
                column_pages = pages[start_idx:end_idx]
                columns.append(column_pages)
            
            # Format output with RPG effect
            header = self._rpg_header(f"Available man pages ({len(pages)}):")
            output_lines = [header]
            for row_idx in range(num_rows):
                row_items = []
                for col_idx in range(num_columns):
                    if row_idx < len(columns[col_idx]):
                        page_name = columns[col_idx][row_idx]
                        row_items.append(f"  - {page_name.ljust(max_width)}")
                    else:
                        row_items.append(" " * (max_width + 4))
                output_lines.append("".join(row_items))
            
            return {
                'success': True,
                'output': "\n".join(output_lines),
                'pages': pages,
                'count': len(pages),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_add(self, *args) -> Dict[str, Any]:
        """Add a custom man page"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: man add <name> <content_file> [section]',
            }
            
        name = args[0]
        content_file = args[1]
        section = int(args[2]) if len(args) > 2 else 1
        
        try:
            # Read content from file
            with open(content_file, 'r') as f:
                content = f.read()
                
            success = await self.man_engine.add_page(name, content, section)
            
            if success:
                return {
                    'success': True,
                    'output': f'Man page {name} added successfully',
                    'name': name,
                    'section': section,
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to add man page {name}',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_remove(self, *args) -> Dict[str, Any]:
        """Remove a custom man page"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man remove <page_name>',
            }
            
        page_name = args[0]
        
        try:
            success = await self.man_engine.remove_page(page_name)
            
            if success:
                return {
                    'success': True,
                    'output': f'Man page {page_name} removed successfully',
                    'name': page_name,
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to remove man page {page_name} (not found or not custom)',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_export(self, *args) -> Dict[str, Any]:
        """Export a man page to a file"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: man export <page_name> <output_file> [format]',
            }
            
        page_name = args[0]
        output_file = args[1]
        format = args[2] if len(args) > 2 else 'md'
        
        try:
            content = await self.man_engine.export_page(page_name, format)
            
            if content:
                with open(output_file, 'w') as f:
                    f.write(content)
                    
                return {
                    'success': True,
                    'output': f'Man page {page_name} exported to {output_file}',
                    'format': format,
                }
            else:
                return {
                    'success': False,
                    'error': f'Man page {page_name} not found',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Show man engine statistics"""
        try:
            stats = await self.man_engine.get_stats()
            output = f"Man Engine Statistics:\n"
            output += f"  Enabled: {stats['enabled']}\n"
            output += f"  Total pages: {stats['total_pages']}\n"
            output += f"  Custom pages: {stats['custom_pages']}\n"
            output += f"  Builtin pages: {stats['builtin_pages']}\n"
            output += f"  Cache hit rate: {stats['cache_stats']['hit_rate']}\n"
            output += f"  Index size: {stats['index_size']}"
            return {
                'success': True,
                'output': output,
                'stats': stats,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_refresh(self, *args) -> Dict[str, Any]:
        """Refresh man pages from sources"""
        try:
            await self.man_engine.refresh()
            return {
                'success': True,
                'output': 'Man pages refreshed successfully',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_cache_clear(self, *args) -> Dict[str, Any]:
        """Clear man page cache"""
        try:
            success = await self.man_engine.cache.clear()
            
            if success:
                return {
                    'success': True,
                    'output': 'Man page cache cleared successfully',
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to clear cache',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_cache_stats(self, *args) -> Dict[str, Any]:
        """Show cache statistics"""
        try:
            stats = await self.man_engine.cache.get_stats()
            output = f"Cache Statistics:\n"
            output += f"  Enabled: {stats['enabled']}\n"
            output += f"  Memory size: {stats['memory_size']}/{stats['max_memory_size']}\n"
            output += f"  Disk size: {stats['disk_size']}/{stats['max_disk_size']}\n"
            output += f"  Hits: {stats['hits']}\n"
            output += f"  Misses: {stats['misses']}\n"
            output += f"  Hit rate: {stats['hit_rate']}\n"
            output += f"  Policy: {stats['policy']}\n"
            output += f"  TTL: {stats['ttl']}s"
            return {
                'success': True,
                'output': output,
                'cache_stats': stats,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
            
    async def cmd_cleanup(self, *args) -> Dict[str, Any]:
        """Clean up expired cache entries"""
        try:
            cleaned = await self.man_engine.cache.cleanup_expired()
            return {
                'success': True,
                'output': f'Cleaned up {cleaned} expired cache entries',
                'cleaned': cleaned,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_whatis(self, *args) -> Dict[str, Any]:
        """Get short description for a module (like whatis command)"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man whatis <module_name>',
            }
        
        name = args[0]
        
        try:
            desc = await self.man_engine.whatis(name)
            
            if desc:
                return {
                    'success': True,
                    'output': f'{name} — {desc}',
                    'name': name,
                    'description': desc,
                }
            else:
                return {
                    'success': False,
                    'error': f'No whatis entry for {name}',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_whatis_all(self, *args) -> Dict[str, Any]:
        """Get all available whatis entries"""
        try:
            entries = await self.man_engine.whatis_all()
            
            output_lines = ['All WHATIS entries:']
            for name, desc in entries.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'entries': entries,
                'count': len(entries),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_search_source(self, *args) -> Dict[str, Any]:
        """Search only in specific source (meta, pkg, man, info)"""
        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: man search_source <pattern> <source> (meta, pkg, man, info)',
            }
        
        pattern = args[0]
        source = args[1]
        
        try:
            results = await self.man_engine.search_by_source(pattern, source)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No matches in {source.upper()} for: {pattern}',
                    'pattern': pattern,
                    'source': source,
                    'results': {},
                    'count': 0,
                }
            
            output_lines = [f'Matches in {source.upper()} for: {pattern}']
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'pattern': pattern,
                'source': source,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_search_tag(self, *args) -> Dict[str, Any]:
        """Search modules by tag (from PKG database)"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man search_tag <tag>',
            }
        
        tag = args[0]
        
        try:
            results = await self.man_engine.search_by_tag(tag)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No modules with tag: {tag}',
                    'tag': tag,
                    'results': {},
                    'count': 0,
                }
            
            output_lines = [f'Modules with tag: {tag}']
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'tag': tag,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_search_section(self, *args) -> Dict[str, Any]:
        """Search modules by man section"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man search_section <section_number>',
            }
        
        try:
            section = int(args[0])
        except ValueError:
            return {
                'success': False,
                'error': 'Section must be a number (1-9)',
            }
        
        try:
            results = await self.man_engine.search_by_section(section)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No modules in section {section}',
                    'section': section,
                    'results': {},
                    'count': 0,
                }
            
            output_lines = [f'Modules in section {section}:']
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'section': section,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_search_advanced(self, *args) -> Dict[str, Any]:
        """Advanced search with multiple filters"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man search_advanced <query> [options] --source <source> --section <num> --tag <tag> --exact --case',
            }
        
        query = args[0]
        options = {}
        
        # Parse options
        i = 1
        while i < len(args):
            if args[i] == '--source' and i + 1 < len(args):
                options['source'] = args[i + 1]
                i += 2
            elif args[i] == '--section' and i + 1 < len(args):
                try:
                    options['section'] = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif args[i] == '--tag' and i + 1 < len(args):
                options['tag'] = args[i + 1]
                i += 2
            elif args[i] == '--exact':
                options['exact'] = True
                i += 1
            elif args[i] == '--case':
                options['case_sensitive'] = True
                i += 1
            else:
                i += 1
        
        try:
            results = await self.man_engine.search_advanced(query, options)
            
            if not results:
                return {
                    'success': True,
                    'output': f'No matches for advanced search: {query}',
                    'query': query,
                    'options': options,
                    'results': {},
                    'count': 0,
                }
            
            output_lines = [f'Advanced search results for: {query}']
            if options:
                output_lines.append(f'Options: {options}')
            for name, desc in results.items():
                output_lines.append(f'  {name} — {desc}')
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'query': query,
                'options': options,
                'results': results,
                'count': len(results),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_export_db(self, *args) -> Dict[str, Any]:
        """Export entire database to file"""
        if len(args) < 1:
            return {
                'success': False,
                'error': 'Usage: man export_db <filepath> [format] (json, txt)',
            }
        
        filepath = args[0]
        format = args[1] if len(args) > 1 else 'json'
        
        try:
            success = await self.man_engine.export_database(filepath, format)
            
            if success:
                return {
                    'success': True,
                    'output': f'Database exported to {filepath} (format: {format})',
                    'filepath': filepath,
                    'format': format,
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to export database to {filepath}',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_import_db(self, *args) -> Dict[str, Any]:
        """Import database from file"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man import_db <filepath> [--merge|--replace]',
            }
        
        filepath = args[0]
        merge = '--replace' not in args
        
        try:
            success = await self.man_engine.import_database(filepath, merge)
            
            if success:
                mode = 'merge' if merge else 'replace'
                return {
                    'success': True,
                    'output': f'Database imported from {filepath} (mode: {mode})',
                    'filepath': filepath,
                    'mode': mode,
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to import database from {filepath}',
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_validate(self, *args) -> Dict[str, Any]:
        """Validate all entries and return issues"""
        try:
            issues = await self.man_engine.validate_entries()
            
            output_lines = ['Validation results:']
            
            for issue_type, entries in issues.items():
                if entries:
                    output_lines.append(f'  {issue_type.replace("_", " ").title()}: {len(entries)}')
                    for entry in entries[:5]:  # Show first 5
                        output_lines.append(f'    - {entry}')
                    if len(entries) > 5:
                        output_lines.append(f'    ... and {len(entries) - 5} more')
                else:
                    output_lines.append(f'  {issue_type.replace("_", " ").title()}: OK')
            
            total_issues = sum(len(entries) for entries in issues.values())
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'issues': issues,
                'total_issues': total_issues,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_history(self, *args) -> Dict[str, Any]:
        """Get search history"""
        limit = int(args[0]) if args else 10
        
        try:
            history = await self.man_engine.get_search_history(limit)
            
            if not history:
                return {
                    'success': True,
                    'output': 'No search history',
                    'history': [],
                    'count': 0,
                }
            
            output_lines = ['Search history:']
            for entry in history:
                output_lines.append(f"  {entry['timestamp']} - {entry['type']}: {entry['query']} ({entry['results_count']} results)")
            
            return {
                'success': True,
                'output': '\n'.join(output_lines),
                'history': history,
                'count': len(history),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_clear_history(self, *args) -> Dict[str, Any]:
        """Clear search history"""
        try:
            await self.man_engine.clear_search_history()
            return {
                'success': True,
                'output': 'Search history cleared',
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_readme(self, *args) -> Dict[str, Any]:
        """Display the man module README file"""
        import os
        
        try:
            # Path to the man README file
            readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'man', 'README.md')
            
            # Check if file exists
            if not os.path.exists(readme_path):
                return {
                    'success': False,
                    'error': f'README file not found: {readme_path}',
                }
            
            # Read the README file
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            return {
                'success': True,
                'output': readme_content,
                'file': readme_path,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_categories(self, *args) -> Dict[str, Any]:
        """List all categories and their pages"""
        try:
            categories = await self.man_engine.list_categories()
            output = "Man Page Categories:\n"
            for category, pages in categories.items():
                output += f"\n{category.upper()} ({len(pages)} pages):\n"
                for page in pages:
                    output += f"  - {page}\n"
            
            return {
                'success': True,
                'output': output,
                'categories': categories,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_category(self, *args) -> Dict[str, Any]:
        """Get pages in a specific category"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man category <category_name>',
            }
        
        category_name = args[0]
        try:
            pages = await self.man_engine.get_category_pages(category_name)
            
            if not pages:
                return {
                    'success': False,
                    'error': f'Category "{category_name}" not found or empty',
                }
            
            output = f"Category: {category_name.upper()} ({len(pages)} pages)\n"
            output += "\n".join(f"  - {page}" for page in pages)
            
            return {
                'success': True,
                'output': output,
                'category': category_name,
                'pages': pages,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_usage_stats(self, *args) -> Dict[str, Any]:
        """Display usage statistics"""
        try:
            stats = await self.man_engine.get_usage_stats()
            output = "Man Page Usage Statistics:\n"
            output += f"\nMost Viewed Pages:\n"
            for page, count in stats.get('most_viewed', []):
                output += f"  {page}: {count} views\n"
            
            output += f"\nMost Searched Terms:\n"
            for query, count in stats.get('most_searched', []):
                output += f"  {query}: {count} searches\n"
            
            output += f"\nTotal Page Views: {sum(stats['page_views'].values())}\n"
            output += f"Total Searches: {sum(stats['search_queries'].values())}\n"
            
            return {
                'success': True,
                'output': output,
                'stats': stats,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_cross_refs(self, *args) -> Dict[str, Any]:
        """Get cross-references for a page"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man cross_refs <page_name>',
            }
        
        page_name = args[0]
        try:
            refs = await self.man_engine.get_cross_references(page_name)
            
            if not refs:
                return {
                    'success': True,
                    'output': f"No cross-references found for {page_name}",
                    'references': [],
                }
            
            output = f"Cross-references for {page_name}:\n"
            output += "\n".join(f"  - {ref}" for ref in refs)
            
            return {
                'success': True,
                'output': output,
                'page': page_name,
                'references': refs,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    async def cmd_quick_ref(self, *args) -> Dict[str, Any]:
        """Get quick reference summary for a page"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: man quick_ref <page_name>',
            }
        
        page_name = args[0]
        try:
            quick_ref = await self.man_engine.get_quick_reference(page_name)
            
            if not quick_ref:
                return {
                    'success': False,
                    'error': f'Page "{page_name}" not found',
                }
            
            return {
                'success': True,
                'output': quick_ref,
                'page': page_name,
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }
