"""
 ============================================================
  MODULE/PLUGIN NAME: CDCommands
  VERSION: 1.0.0
  MODULE CLASS: CDCommands
  DESCRIPTION:
       CD command handlers for directory and context navigation

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
from typing import Dict, Any, List, Optional
from libs.clean_logger import CleanLogger, LogLevel


class CDCommands:
    """
    CD TERMINAL COMMANDS:
    - Standard filesystem navigation
    - Contextual navigation (modules/plugins/system)
    - Documentation navigation (help/info/docs/api)
    - Multi-context navigation
    - Bookmarks (@)
    - History management
    - Diagnostic features
    - AI-assisted navigation
    - Aliases and shortcuts
    - Teleportation (GODMODE)
    - Meta-commands
    """

    def __init__(self, terminal):
        self.terminal = terminal
        self.logger = CleanLogger("CDCommands", LogLevel.INFO)
        self.current_path = os.getcwd()
        self.previous_path = os.getcwd()
        self.current_context = "filesystem"  # filesystem, module, plugin, system
        self.current_module = None
        self.current_plugin = None
        self.history = []
        self.bookmarks = {}
        self.bookmarks_file = "cd_bookmarks.json"
        self.history_file = "cd_history.json"
        
        # Load saved data
        self._load_bookmarks()
        self._load_history()

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a CD command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            # Try to treat as default cd command
            return await self.cmd_default(*args)

    # ============================================================
    # STANDARD FILESYSTEM CD
    # ============================================================
    async def cmd_default(self, *args) -> Dict[str, Any]:
        """Default CD command for filesystem navigation"""
        if not args:
            # cd without args goes to home directory
            target = os.path.expanduser("~")
        else:
            target = args[0]
        
        # Handle special cases
        if target == ".":
            target = self.current_path
        elif target == "..":
            target = os.path.dirname(self.current_path)
        elif target == "../..":
            target = os.path.dirname(os.path.dirname(self.current_path))
        elif target == "\\":
            target = self.current_path
        elif target == "/":
            target = os.path.abspath(os.sep)
        elif target == "~":
            target = os.path.expanduser("~")
        elif target == "-":
            target = self.previous_path
        
        # Resolve relative/absolute paths
        if os.path.isabs(target):
            new_path = target
        else:
            new_path = os.path.join(self.current_path, target)
        
        # Try to change directory
        if os.path.isdir(new_path):
            self.previous_path = self.current_path
            self.current_path = os.path.abspath(new_path)
            self.current_context = "filesystem"
            self._add_to_history(self.current_path, "filesystem")
            
            try:
                os.chdir(self.current_path)
                return {
                    'success': True,
                    'output': f'Changed directory to: {self.current_path}'
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to change directory: {str(e)}'
                }
        else:
            return {
                'success': False,
                'error': f'Directory not found: {target}'
            }

    # ============================================================
    # CONTEXTUAL CD (MODULES/PLUGINS/SYSTEM)
    # ============================================================
    async def cmd_module(self, *args) -> Dict[str, Any]:
        """CD to module context: cd module:<name> or cd mod:<name>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd module:<name> or cd mod:<name>'}
        
        target = args[0]
        
        # Handle module: and mod: prefixes
        if target.startswith("module:"):
            module_name = target[7:]
        elif target.startswith("mod:"):
            module_name = target[4:]
        else:
            module_name = target
        
        # Check if module exists (placeholder logic)
        self.previous_path = self.current_path
        self.current_context = "module"
        self.current_module = module_name
        self._add_to_history(f"module:{module_name}", "module")
        
        return {
            'success': True,
            'output': f'Changed context to module: {module_name}'
        }

    async def cmd_plugin(self, *args) -> Dict[str, Any]:
        """CD to plugin context: cd plugin:<name> or cd plug:<name>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd plugin:<name> or cd plug:<name>'}
        
        target = args[0]
        
        # Handle plugin: and plug: prefixes
        if target.startswith("plugin:"):
            plugin_name = target[7:]
        elif target.startswith("plug:"):
            plugin_name = target[5:]
        else:
            plugin_name = target
        
        # Check if plugin exists (placeholder logic)
        self.previous_path = self.current_path
        self.current_context = "plugin"
        self.current_plugin = plugin_name
        self._add_to_history(f"plugin:{plugin_name}", "plugin")
        
        return {
            'success': True,
            'output': f'Changed context to plugin: {plugin_name}'
        }

    async def cmd_system(self, *args) -> Dict[str, Any]:
        """CD to system context: cd system, kernel, config, logs, etc."""
        if not args:
            return {'success': False, 'error': 'Usage: cd <system_context>'}
        
        target = args[0]
        valid_systems = ['system', 'kernel', 'config', 'logs', 'sandbox', 'ui', 'ansi', 'engine', 'registry']
        
        if target in valid_systems:
            self.previous_path = self.current_path
            self.current_context = "system"
            self._add_to_history(f"system:{target}", "system")
            
            return {
                'success': True,
                'output': f'Changed context to system: {target}'
            }
        else:
            return {
                'success': False,
                'error': f'Invalid system context. Valid: {", ".join(valid_systems)}'
            }

    # ============================================================
    # DOCUMENTATION CD
    # ============================================================
    async def cmd_help(self, *args) -> Dict[str, Any]:
        """CD to help context: cd help:<topic>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd help:<topic>'}
        
        target = args[0]
        if target.startswith("help:"):
            topic = target[5:]
        else:
            topic = target
        
        self.previous_path = self.current_path
        self.current_context = "help"
        self._add_to_history(f"help:{topic}", "help")
        
        return {
            'success': True,
            'output': f'Changed context to help: {topic}'
        }

    async def cmd_info(self, *args) -> Dict[str, Any]:
        """CD to info context: cd info:<node>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd info:<node>'}
        
        target = args[0]
        if target.startswith("info:"):
            node = target[5:]
        else:
            node = target
        
        self.previous_path = self.current_path
        self.current_context = "info"
        self._add_to_history(f"info:{node}", "info")
        
        return {
            'success': True,
            'output': f'Changed context to info: {node}'
        }

    async def cmd_docs(self, *args) -> Dict[str, Any]:
        """CD to docs context: cd docs:<module>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd docs:<module>'}
        
        target = args[0]
        if target.startswith("docs:"):
            module = target[5:]
        else:
            module = target
        
        self.previous_path = self.current_path
        self.current_context = "docs"
        self._add_to_history(f"docs:{module}", "docs")
        
        return {
            'success': True,
            'output': f'Changed context to docs: {module}'
        }

    async def cmd_api(self, *args) -> Dict[str, Any]:
        """CD to API context: cd api:<module>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd api:<module>'}
        
        target = args[0]
        if target.startswith("api:"):
            module = target[4:]
        else:
            module = target
        
        self.previous_path = self.current_path
        self.current_context = "api"
        self._add_to_history(f"api:{module}", "api")
        
        return {
            'success': True,
            'output': f'Changed context to API: {module}'
        }

    # ============================================================
    # MULTI-CONTEXT CD
    # ============================================================
    async def cmd_multi(self, *args) -> Dict[str, Any]:
        """Multi-context CD: cd <path>;<module>;<plugin>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd <path>;<module>;<plugin>'}
        
        target = args[0]
        contexts = target.split(';')
        
        results = []
        for ctx in contexts:
            ctx = ctx.strip()
            if not ctx:
                continue
            
            if ctx.startswith("module:") or ctx.startswith("mod:"):
                result = await self.cmd_module(ctx)
            elif ctx.startswith("plugin:") or ctx.startswith("plug:"):
                result = await self.cmd_plugin(ctx)
            elif ctx.startswith("system:"):
                result = await self.cmd_system(ctx[7:])
            elif os.path.isabs(ctx) or os.path.isdir(ctx):
                result = await self.cmd_default(ctx)
            else:
                results.append(f"Unknown context: {ctx}")
                continue
            
            if result.get('success'):
                results.append(result.get('output', ''))
            else:
                results.append(result.get('error', 'Failed'))
        
        return {
            'success': True,
            'output': 'Multi-context navigation:\n' + '\n'.join(results)
        }

    # ============================================================
    # BOOKMARKS (@)
    # ============================================================
    async def cmd_save(self, *args) -> Dict[str, Any]:
        """Save current context as bookmark: cd @save <name>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd @save <name>'}
        
        name = args[0]
        
        self.bookmarks[name] = {
            'path': self.current_path,
            'context': self.current_context,
            'module': self.current_module,
            'plugin': self.current_plugin
        }
        
        self._save_bookmarks()
        
        return {
            'success': True,
            'output': f'Bookmark saved: {name}'
        }

    async def cmd_load(self, *args) -> Dict[str, Any]:
        """Load bookmark: cd @load <name>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd @load <name>'}
        
        name = args[0]
        
        if name not in self.bookmarks:
            return {
                'success': False,
                'error': f'Bookmark not found: {name}'
            }
        
        bookmark = self.bookmarks[name]
        self.previous_path = self.current_path
        self.current_path = bookmark['path']
        self.current_context = bookmark['context']
        self.current_module = bookmark.get('module')
        self.current_plugin = bookmark.get('plugin')
        
        # Try to change directory if it's a filesystem path
        if self.current_context == "filesystem" and os.path.isdir(self.current_path):
            try:
                os.chdir(self.current_path)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to restore directory: {str(e)}'
                }
        
        self._add_to_history(f"@{name}", "bookmark")
        
        return {
            'success': True,
            'output': f'Bookmark loaded: {name} -> {self.current_path} ({self.current_context})'
        }

    async def cmd_list_bookmarks(self, *args) -> Dict[str, Any]:
        """List all bookmarks: cd @list"""
        if not self.bookmarks:
            return {
                'success': True,
                'output': 'No bookmarks saved'
            }
        
        output = "Saved bookmarks:\n"
        for name, data in self.bookmarks.items():
            output += f"  @{name}: {data['path']} ({data['context']})\n"
        
        return {
            'success': True,
            'output': output.strip()
        }

    async def cmd_del_bookmark(self, *args) -> Dict[str, Any]:
        """Delete bookmark: cd @del <name>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd @del <name>'}
        
        name = args[0]
        
        if name not in self.bookmarks:
            return {
                'success': False,
                'error': f'Bookmark not found: {name}'
            }
        
        del self.bookmarks[name]
        self._save_bookmarks()
        
        return {
            'success': True,
            'output': f'Bookmark deleted: {name}'
        }

    # ============================================================
    # HISTORY
    # ============================================================
    async def cmd_history(self, *args) -> Dict[str, Any]:
        """Show CD history: cd history [--dirs|--modules|--plugins|--clear]"""
        if not args:
            # Show full history
            if not self.history:
                return {
                    'success': True,
                    'output': 'No history recorded'
                }
            
            output = "CD history:\n"
            for i, entry in enumerate(self.history[-20:], 1):  # Last 20 entries
                output += f"  {i}. {entry['target']} ({entry['context']})\n"
            
            return {
                'success': True,
                'output': output.strip()
            }
        
        option = args[0]
        
        if option == "--dirs":
            filtered = [e for e in self.history if e['context'] == "filesystem"]
        elif option == "--modules":
            filtered = [e for e in self.history if e['context'] == "module"]
        elif option == "--plugins":
            filtered = [e for e in self.history if e['context'] == "plugin"]
        elif option == "--clear":
            self.history = []
            self._save_history()
            return {
                'success': True,
                'output': 'History cleared'
            }
        else:
            return {
                'success': False,
                'error': f'Invalid option: {option}. Use --dirs, --modules, --plugins, or --clear'
            }
        
        if not filtered:
            return {
                'success': True,
                'output': f'No history entries for {option}'
            }
        
        output = f"CD history ({option}):\n"
        for i, entry in enumerate(filtered[-20:], 1):
            output += f"  {i}. {entry['target']}\n"
        
        return {
            'success': True,
            'output': output.strip()
        }

    # ============================================================
    # DIAGNOSTIC
    # ============================================================
    async def cmd_diag(self, *args) -> Dict[str, Any]:
        """Diagnostic CD: cd diag [path] [--fix]"""
        fix_mode = False
        target_path = self.current_path
        
        if args:
            for arg in args:
                if arg == "--fix":
                    fix_mode = True
                else:
                    target_path = arg
        
        if not os.path.exists(target_path):
            return {
                'success': False,
                'error': f'Path not found: {target_path}'
            }
        
        # Perform diagnostics
        diagnostics = []
        
        if os.path.isdir(target_path):
            # Check if directory is accessible
            if not os.access(target_path, os.R_OK):
                diagnostics.append("[X] Directory not readable")
            else:
                diagnostics.append("[OK] Directory readable")
            
            if not os.access(target_path, os.W_OK):
                diagnostics.append("[X] Directory not writable")
            else:
                diagnostics.append("[OK] Directory writable")
            
            # Check for hidden files
            try:
                items = os.listdir(target_path)
                hidden = [i for i in items if i.startswith('.')]
                if hidden:
                    diagnostics.append(f"[!] Found {len(hidden)} hidden items")
            except Exception as e:
                diagnostics.append(f"[X] Error listing directory: {str(e)}")
        
        if fix_mode:
            diagnostics.append("[TOOL] Fix mode: No automatic fixes available (manual intervention required)")
        
        output = f"Diagnostic results for {target_path}:\n"
        output += "\n".join(diagnostics)
        
        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # AI FEATURES
    # ============================================================
    async def cmd_suggest(self, *args) -> Dict[str, Any]:
        """AI suggestions: cd ?"""
        suggestions = []
        
        # Suggest based on recent history
        if self.history:
            recent_contexts = [e['context'] for e in self.history[-5:]]
            if "filesystem" in recent_contexts:
                suggestions.append(f"Recent directory: {self.current_path}")
            if "module" in recent_contexts and self.current_module:
                suggestions.append(f"Recent module: {self.current_module}")
            if "plugin" in recent_contexts and self.current_plugin:
                suggestions.append(f"Recent plugin: {self.current_plugin}")
        
        # Suggest based on available contexts
        suggestions.append("Try: cd <relative/path>")
        suggestions.append("Try: cd module:<name>")
        suggestions.append("Try: cd plugin:<name>")
        suggestions.append("Try: cd @load <bookmark>")
        
        if not suggestions:
            suggestions.append("No suggestions available")
        
        return {
            'success': True,
            'output': "AI Suggestions:\n" + "\n".join(suggestions)
        }

    async def cmd_auto(self, *args) -> Dict[str, Any]:
        """AI auto-navigate: cd auto"""
        # Simple AI logic: go to most likely context based on history
        if not self.history:
            return {
                'success': False,
                'error': 'No history available for auto-navigation'
            }
        
        # Find most frequent context
        context_counts = {}
        for entry in self.history:
            ctx = entry['context']
            context_counts[ctx] = context_counts.get(ctx, 0) + 1
        
        most_likely = max(context_counts, key=context_counts.get)
        
        # Navigate to most recent entry of that context
        for entry in reversed(self.history):
            if entry['context'] == most_likely:
                target = entry['target']
                if most_likely == "filesystem" and os.path.isdir(target):
                    result = await self.cmd_default(target)
                elif most_likely == "module":
                    result = await self.cmd_module(target)
                elif most_likely == "plugin":
                    result = await self.cmd_plugin(target)
                else:
                    result = await self.cmd_system(target)
                
                result['output'] = f"AI auto-navigation to {most_likely}: {result.get('output', '')}"
                return result
        
        return {
            'success': False,
            'error': 'Could not determine auto-navigation target'
        }

    async def cmd_search(self, *args) -> Dict[str, Any]:
        """AI search: cd <keyword>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd <keyword>'}
        
        keyword = args[0].lower()
        matches = []
        
        # Search in history
        for entry in self.history:
            if keyword in entry['target'].lower():
                matches.append(f"[HISTORY] {entry['target']} ({entry['context']})")
        
        # Search in bookmarks
        for name, data in self.bookmarks.items():
            if keyword in name.lower() or keyword in data['path'].lower():
                matches.append(f"[BOOKMARK] @{name}: {data['path']} ({data['context']})")
        
        # Search in current directory
        if os.path.isdir(self.current_path):
            try:
                for item in os.listdir(self.current_path):
                    if keyword in item.lower():
                        item_path = os.path.join(self.current_path, item)
                        if os.path.isdir(item_path):
                            matches.append(f"[DIR] {item}")
            except Exception:
                pass
        
        if not matches:
            return {
                'success': True,
                'output': f'No matches found for: {keyword}'
            }
        
        return {
            'success': True,
            'output': f"Search results for '{keyword}':\n" + "\n".join(matches[:10])
        }

    # ============================================================
    # ALIASES AND SHORTCUTS
    # ============================================================
    async def cmd_root(self, *args) -> Dict[str, Any]:
        """Alias: cd root -> /"""
        return await self.cmd_default("/")

    async def cmd_home(self, *args) -> Dict[str, Any]:
        """Alias: cd home -> ~"""
        return await self.cmd_default("~")

    async def cmd_back(self, *args) -> Dict[str, Any]:
        """Alias: cd back -> cd -"""
        return await self.cmd_default("-")

    async def cmd_up(self, *args) -> Dict[str, Any]:
        """Alias: cd up -> cd .."""
        return await self.cmd_default("..")

    async def cmd_top(self, *args) -> Dict[str, Any]:
        """Alias: cd top -> highest project level"""
        # Navigate to highest level by going up until no more parent directories
        current = self.current_path
        previous = None
        
        while previous != current:
            previous = current
            current = os.path.dirname(current)
        
        return await self.cmd_default(previous if previous else "/")

    # ============================================================
    # TELEPORTATION (GODMODE)
    # ============================================================
    async def cmd_teleport(self, *args) -> Dict[str, Any]:
        """Teleport: cd teleport <target>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd teleport <target>'}
        
        target = args[0]
        
        # Check if it's a bookmark
        if target.startswith("@") and target[1:] in self.bookmarks:
            return await self.cmd_load(target[1:])
        
        # Check if it's a system context
        if target in ['system', 'kernel', 'config', 'logs', 'sandbox', 'ui', 'ansi', 'engine', 'registry']:
            return await self.cmd_system(target)
        
        # Check if it's a module
        if target.startswith("module:") or target.startswith("mod:"):
            return await self.cmd_module(target)
        
        # Check if it's a plugin
        if target.startswith("plugin:") or target.startswith("plug:"):
            return await self.cmd_plugin(target)
        
        # Treat as filesystem path
        return await self.cmd_default(target)

    async def cmd_warp(self, *args) -> Dict[str, Any]:
        """Warp: cd warp <module/plugin/system>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd warp <module/plugin/system>'}
        
        target = args[0]
        
        # Fast switch to common contexts
        if target == "module":
            return await self.cmd_module("core")
        elif target == "plugin":
            return await self.cmd_plugin("default")
        elif target == "system":
            return await self.cmd_system("system")
        else:
            return await self.cmd_teleport(target)

    async def cmd_jump(self, *args) -> Dict[str, Any]:
        """Jump: cd jump <bookmark>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd jump <bookmark>'}
        
        bookmark_name = args[0]
        return await self.cmd_load(bookmark_name)

    # ============================================================
    # META-COMMANDS
    # ============================================================
    async def cmd_where(self, *args) -> Dict[str, Any]:
        """Show current context: cd --where"""
        output = f"Current context:\n"
        output += f"  Path: {self.current_path}\n"
        output += f"  Context: {self.current_context}\n"
        
        if self.current_module:
            output += f"  Module: {self.current_module}\n"
        if self.current_plugin:
            output += f"  Plugin: {self.current_plugin}\n"
        
        return {
            'success': True,
            'output': output.strip()
        }

    async def cmd_prev(self, *args) -> Dict[str, Any]:
        """Show previous context: cd --prev"""
        output = f"Previous context:\n"
        output += f"  Path: {self.previous_path}\n"
        
        if self.history and len(self.history) > 1:
            prev_entry = self.history[-2]
            output += f"  Previous target: {prev_entry['target']} ({prev_entry['context']})\n"
        
        return {
            'success': True,
            'output': output.strip()
        }

    async def cmd_contexts(self, *args) -> Dict[str, Any]:
        """List available contexts: cd --contexts"""
        contexts = [
            "filesystem - Standard file system navigation",
            "module - Module context navigation",
            "plugin - Plugin context navigation",
            "system - System context navigation",
            "help - Help documentation",
            "info - Info pages",
            "docs - Module documentation",
            "api - API documentation"
        ]
        
        return {
            'success': True,
            'output': "Available contexts:\n" + "\n".join(f"  - {ctx}" for ctx in contexts)
        }

    async def cmd_resolve(self, *args) -> Dict[str, Any]:
        """Resolve target: cd --resolve <target>"""
        if not args:
            return {'success': False, 'error': 'Usage: cd --resolve <target>'}
        
        target = args[0]
        resolution = f"Target: {target}\n"
        
        # Determine how target would be interpreted
        if target.startswith("module:") or target.startswith("mod:"):
            resolution += "Type: Module context\n"
            module_name = target[7:] if target.startswith("module:") else target[4:]
            resolution += f"Module: {module_name}\n"
        elif target.startswith("plugin:") or target.startswith("plug:"):
            resolution += "Type: Plugin context\n"
            plugin_name = target[7:] if target.startswith("plugin:") else target[5:]
            resolution += f"Plugin: {plugin_name}\n"
        elif target.startswith("system:"):
            resolution += "Type: System context\n"
            resolution += f"System: {target[7:]}\n"
        elif target.startswith("@"):
            resolution += "Type: Bookmark\n"
            bookmark_name = target[1:]
            if bookmark_name in self.bookmarks:
                resolution += f"Bookmark: {bookmark_name} -> {self.bookmarks[bookmark_name]['path']}\n"
            else:
                resolution += f"Bookmark: {bookmark_name} (not found)\n"
        elif os.path.isabs(target):
            resolution += "Type: Absolute path\n"
            resolution += f"Path: {target}\n"
        else:
            resolution += "Type: Relative path\n"
            resolution += f"Base: {self.current_path}\n"
            resolution += f"Resolved: {os.path.join(self.current_path, target)}\n"
        
        return {
            'success': True,
            'output': resolution.strip()
        }

    # ============================================================
    # HELPER METHODS
    # ============================================================
    def _add_to_history(self, target: str, context: str):
        """Add entry to history"""
        self.history.append({
            'target': target,
            'context': context,
            'path': self.current_path
        })
        
        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self._save_history()

    def _save_bookmarks(self):
        """Save bookmarks to file"""
        try:
            with open(self.bookmarks_file, 'w') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            self.logger.error(f"Failed to save bookmarks: {str(e)}")

    def _load_bookmarks(self):
        """Load bookmarks from file"""
        try:
            if os.path.exists(self.bookmarks_file):
                with open(self.bookmarks_file, 'r') as f:
                    self.bookmarks = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load bookmarks: {str(e)}")
            self.bookmarks = {}

    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            self.logger.error(f"Failed to save history: {str(e)}")

    def _load_history(self):
        """Load history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load history: {str(e)}")
            self.history = []
