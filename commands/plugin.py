"""
 ============================================================
  MODULE/PLUGIN NAME: PluginCommands
  VERSION: 1.0.0
  MODULE CLASS: PluginCommands
  DESCRIPTION:
       Plugin command handlers for plugin management operations

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

from typing import Dict, Any, Optional
from libs.clean_logger import CleanLogger, LogLevel


class PluginCommands:
    """
    PLUGIN TERMINAL COMMANDS:
    - Plugin installation/removal
    - Plugin enable/disable
    - Plugin listing/info
    - Plugin reload
    - Hook management
    - Event management
    - Sandbox management
    - Permission management
    - AI plugin management (load, unload, reload, list)
    """

    def __init__(self, plugin_manager, ai_plugins=None):
        self.plugin_manager = plugin_manager
        self.ai_plugins = ai_plugins
        self.logger = CleanLogger("PluginCommands", LogLevel.INFO)

    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a plugin command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown plugin command: {command}',
            }

    # ============================================================
    # PLUGIN INSTALLATION
    # ============================================================
    async def cmd_install(self, *args) -> Dict[str, Any]:
        """Install plugin from file or directory"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin install <file_or_directory>'
            }

        plugin_path = args[0]
        plugin_info = None

        # Check if it's a directory or file
        import os
        if os.path.isdir(plugin_path):
            # Load from directory
            plugin_info = self.plugin_manager.loader.load_plugin(plugin_path)
        else:
            # Load from file (zip archive)
            plugin_info = self.plugin_manager.install_plugin(plugin_path)

        if plugin_info:
            # Register plugin
            self.plugin_manager.registry.register(plugin_info)
            
            return {
                'success': True,
                'output': f'Plugin installed: {plugin_info.name} v{plugin_info.version}'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to install plugin'
            }

    async def cmd_remove(self, *args) -> Dict[str, Any]:
        """Remove plugin"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin remove <name>'
            }

        name = args[0]
        if self.plugin_manager.uninstall_plugin(name):
            return {
                'success': True,
                'output': f'Plugin removed: {name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to remove plugin: {name}'
            }

    # ============================================================
    # PLUGIN ENABLE/DISABLE
    # ============================================================
    async def cmd_enable(self, *args) -> Dict[str, Any]:
        """Enable plugin"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin enable <name>'
            }

        name = args[0]
        if self.plugin_manager.enable_plugin(name):
            return {
                'success': True,
                'output': f'Plugin enabled: {name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to enable plugin: {name}'
            }

    async def cmd_disable(self, *args) -> Dict[str, Any]:
        """Disable plugin"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin disable <name>'
            }

        name = args[0]
        if self.plugin_manager.disable_plugin(name):
            return {
                'success': True,
                'output': f'Plugin disabled: {name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to disable plugin: {name}'
            }

    # ============================================================
    # PLUGIN LISTING
    # ============================================================
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List plugins"""
        plugins = self.plugin_manager.list_plugins()

        if not plugins:
            return {
                'success': True,
                'output': 'No plugins installed'
            }

        output = "Installed plugins:\n"
        for plugin in plugins:
            status = "enabled" if plugin.enabled else "disabled"
            output += f"  - {plugin.name} v{plugin.version} ({status}) by {plugin.author}\n"
            output += f"    {plugin.description}\n"

        return {
            'success': True,
            'output': output
        }

    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Show plugin information"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin info <name>'
            }

        name = args[0]
        plugin_info = self.plugin_manager.get_plugin_info(name)

        if not plugin_info:
            return {
                'success': False,
                'error': f'Plugin not found: {name}'
            }

        output = f"""
Plugin: {plugin_info.name}
Version: {plugin_info.version}
Author: {plugin_info.author}
Description: {plugin_info.description}
Status: {'enabled' if plugin_info.enabled else 'disabled'}
Installed: {plugin_info.installed_at}
Last Updated: {plugin_info.last_updated}
Path: {plugin_info.path or 'N/A'}
Permissions: {plugin_info.permissions}
Hooks: {plugin_info.hooks}
Events: {plugin_info.events}
        """.strip()

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # PLUGIN RELOAD
    # ============================================================
    async def cmd_reload(self, *args) -> Dict[str, Any]:
        """Reload plugin"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin reload <name> | plugin reload all'
            }

        if args[0] == 'all':
            reloaded = self.plugin_manager.loader.reload_all()
            return {
                'success': True,
                'output': f'Reloaded {len(reloaded)} plugins'
            }

        name = args[0]
        plugin_info = self.plugin_manager.reload_plugin(name)

        if plugin_info:
            return {
                'success': True,
                'output': f'Plugin reloaded: {name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to reload plugin: {name}'
            }

    # ============================================================
    # HOOKS
    # ============================================================
    async def cmd_hooks(self, *args) -> Dict[str, Any]:
        """List hooks"""
        hooks = self.plugin_manager.list_hooks()

        if not hooks:
            return {
                'success': True,
                'output': 'No hooks registered'
            }

        output = "Registered hooks:\n"
        for hook in hooks:
            count = self.plugin_manager.hooks.count_hooks(hook)
            output += f"  - {hook} ({count} callbacks)\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # EVENTS
    # ============================================================
    async def cmd_events(self, *args) -> Dict[str, Any]:
        """List events"""
        events = self.plugin_manager.list_events()

        if not events:
            return {
                'success': True,
                'output': 'No events subscribed'
            }

        output = "Subscribed events:\n"
        for event in events:
            count = self.plugin_manager.events.count_subscribers(event)
            output += f"  - {event} ({count} subscribers)\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # SANDBOX
    # ============================================================
    async def cmd_sandbox(self, *args) -> Dict[str, Any]:
        """Show sandbox status"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin sandbox <name>'
            }

        name = args[0]
        status = self.plugin_manager.get_sandbox_status(name)

        output = f"""
Sandbox Status for {name}:
  Exists: {status['exists']}
  Path: {status['path'] or 'N/A'}
  Restrictions: {status['restrictions']}
  Resource Usage: {status['resource_usage']}
        """.strip()

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # PERMISSIONS
    # ============================================================
    async def cmd_permissions(self, *args) -> Dict[str, Any]:
        """Show plugin permissions"""
        if not args:
            # List all plugins with their permissions
            plugins = self.plugin_manager.list_plugins()
            if not plugins:
                return {
                    'success': True,
                    'output': 'No plugins installed'
                }
            
            output = "Plugin permissions:\n"
            for plugin in plugins:
                permissions = self.plugin_manager.permissions.get_permissions(plugin.name)
                perm_count = len([p for p, g in permissions.items() if g])
                output += f"  - {plugin.name}: {perm_count} permissions granted\n"
            
            return {
                'success': True,
                'output': output
            }

        name = args[0]
        permissions = self.plugin_manager.permissions.get_permissions(name)

        output = f"Permissions for {name}:\n"
        for perm, granted in permissions.items():
            status = "granted" if granted else "denied"
            output += f"  - {perm}: {status}\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # STATUS
    # ============================================================
    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Show plugin manager status"""
        stats = self.plugin_manager.get_stats()

        output = f"""
Plugin Manager Status:
  Enabled: {stats['enabled']}
  Loaded: {stats['loaded']}
  Total Plugins: {stats['total_plugins']}
  Enabled Plugins: {stats['enabled_plugins']}
  Disabled Plugins: {stats['disabled_plugins']}
  Loaded Plugins: {stats['loaded_plugins']}
  Total Hooks: {stats['total_hooks']}
  Total Events: {stats['total_events']}
        """.strip()

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # START/STOP
    # ============================================================
    async def cmd_start(self, *args) -> Dict[str, Any]:
        """Start plugin manager"""
        if self.plugin_manager.start():
            return {
                'success': True,
                'output': 'Plugin manager started'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to start plugin manager'
            }

    async def cmd_stop(self, *args) -> Dict[str, Any]:
        """Stop plugin manager"""
        if self.plugin_manager.stop():
            return {
                'success': True,
                'output': 'Plugin manager stopped'
            }
        else:
            return {
                'success': False,
                'error': 'Failed to stop plugin manager'
            }

    # ============================================================
    # AI PLUGIN COMMANDS
    # ============================================================
    async def cmd_ai_list(self, *args) -> Dict[str, Any]:
        """List all loaded AI plugins"""
        if not self.ai_plugins:
            return {
                'success': False,
                'error': 'AI plugins system not available'
            }

        plugins = await self.ai_plugins.list_plugins()

        return {
            'success': True,
            'output': plugins
        }

    async def cmd_ai_load(self, *args) -> Dict[str, Any]:
        """Load an AI plugin"""
        if not self.ai_plugins:
            return {
                'success': False,
                'error': 'AI plugins system not available'
            }

        if not args:
            return {'success': False, 'error': 'Usage: plugin ai_load <plugin_name>'}

        success = await self.ai_plugins.load(args[0])

        return {
            'success': success,
            'output': f'Loaded AI plugin {args[0]}' if success else 'Failed to load AI plugin'
        }

    async def cmd_ai_unload(self, *args) -> Dict[str, Any]:
        """Unload an AI plugin"""
        if not self.ai_plugins:
            return {
                'success': False,
                'error': 'AI plugins system not available'
            }

        if not args:
            return {'success': False, 'error': 'Usage: plugin ai_unload <plugin_name>'}

        success = await self.ai_plugins.unload(args[0])

        return {
            'success': success,
            'output': f'Unloaded AI plugin {args[0]}' if success else 'Failed to unload AI plugin'
        }

    async def cmd_ai_reload(self, *args) -> Dict[str, Any]:
        """Reload an AI plugin"""
        if not self.ai_plugins:
            return {
                'success': False,
                'error': 'AI plugins system not available'
            }

        if not args:
            return {'success': False, 'error': 'Usage: plugin ai_reload <plugin_name>'}

        success = await self.ai_plugins.reload(args[0])

        return {
            'success': success,
            'output': f'Reloaded AI plugin {args[0]}' if success else 'Failed to reload AI plugin'
        }

    # ============================================================
    # PLUGIN VERIFICATION
    # ============================================================
    async def cmd_verify(self, *args) -> Dict[str, Any]:
        """Verify plugin signature and integrity"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin verify <name>'
            }

        name = args[0]
        verification = self.plugin_manager.verify_plugin(name)

        if verification['valid']:
            return {
                'success': True,
                'output': f'Plugin {name} verification passed: {verification['message']}'
            }
        else:
            return {
                'success': False,
                'error': f'Plugin {name} verification failed: {verification['message']}'
            }

    # ============================================================
    # PLUGIN UPDATE
    # ============================================================
    async def cmd_update(self, *args) -> Dict[str, Any]:
        """Update plugin to latest version"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin update <name>'
            }

        name = args[0]
        updated = self.plugin_manager.update_plugin(name)

        if updated:
            return {
                'success': True,
                'output': f'Plugin {name} updated successfully'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to update plugin: {name}'
            }

    # ============================================================
    # PLUGIN SEARCH
    # ============================================================
    async def cmd_search(self, *args) -> Dict[str, Any]:
        """Search for available plugins"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin search <query>'
            }

        query = args[0]
        results = self.plugin_manager.search_plugins(query)

        if not results:
            return {
                'success': True,
                'output': f'No plugins found matching: {query}'
            }

        output = f"Search results for '{query}':\n"
        for plugin in results:
            output += f"  - {plugin['name']} v{plugin['version']}: {plugin['description']}\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # PLUGIN DEPENDENCIES
    # ============================================================
    async def cmd_dependencies(self, *args) -> Dict[str, Any]:
        """Show plugin dependencies"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin dependencies <name>'
            }

        name = args[0]
        deps = self.plugin_manager.get_dependencies(name)

        if not deps:
            return {
                'success': True,
                'output': f'Plugin {name} has no dependencies'
            }

        output = f"Dependencies for {name}:\n"
        for dep in deps:
            status = "installed" if dep['installed'] else "not installed"
            output += f"  - {dep['name']} ({dep['version']}) - {status}\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # PLUGIN MIGRATION
    # ============================================================
    async def cmd_migrate(self, *args) -> Dict[str, Any]:
        """Migrate plugin data to new version"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin migrate <name> <target_version>'
            }

        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: plugin migrate <name> <target_version>'
            }

        name = args[0]
        target_version = args[1]
        migrated = self.plugin_manager.migrate_plugin(name, target_version)

        if migrated:
            return {
                'success': True,
                'output': f'Plugin {name} migrated to version {target_version}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to migrate plugin: {name}'
            }

    # ============================================================
    # PLUGIN EXPORT/IMPORT
    # ============================================================
    async def cmd_export(self, *args) -> Dict[str, Any]:
        """Export plugin configuration"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin export <name> [output_file]'
            }

        name = args[0]
        output_file = args[1] if len(args) > 1 else f"{name}_config.json"

        exported = self.plugin_manager.export_config(name, output_file)

        if exported:
            return {
                'success': True,
                'output': f'Plugin {name} configuration exported to {output_file}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to export plugin configuration: {name}'
            }

    async def cmd_import(self, *args) -> Dict[str, Any]:
        """Import plugin configuration"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin import <config_file>'
            }

        config_file = args[0]
        imported = self.plugin_manager.import_config(config_file)

        if imported:
            return {
                'success': True,
                'output': f'Plugin configuration imported from {config_file}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to import plugin configuration from {config_file}'
            }

    # ============================================================
    # PLUGIN CLEANUP
    # ============================================================
    async def cmd_clean(self, *args) -> Dict[str, Any]:
        """Clean plugin cache and temporary files"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin clean <name> | plugin clean all'
            }

        if args[0] == 'all':
            cleaned = self.plugin_manager.clean_all()
            return {
                'success': True,
                'output': f'Cleaned {len(cleaned)} plugins'
            }

        name = args[0]
        cleaned = self.plugin_manager.clean_plugin(name)

        if cleaned:
            return {
                'success': True,
                'output': f'Plugin {name} cleaned successfully'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to clean plugin: {name}'
            }

    # ============================================================
    # PLUGIN RESET
    # ============================================================
    async def cmd_reset(self, *args) -> Dict[str, Any]:
        """Reset plugin to default state"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin reset <name>'
            }

        name = args[0]
        reset = self.plugin_manager.reset_plugin(name)

        if reset:
            return {
                'success': True,
                'output': f'Plugin {name} reset to default state'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to reset plugin: {name}'
            }

    # ============================================================
    # PLUGIN TESTING
    # ============================================================
    async def cmd_test(self, *args) -> Dict[str, Any]:
        """Test plugin functionality"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin test <name>'
            }

        name = args[0]
        test_results = self.plugin_manager.test_plugin(name)

        if test_results['passed']:
            return {
                'success': True,
                'output': f'Plugin {name} tests passed: {test_results['message']}'
            }
        else:
            return {
                'success': False,
                'error': f'Plugin {name} tests failed: {test_results['message']}'
            }

    # ============================================================
    # PLUGIN CONFIGURATION
    # ============================================================
    async def cmd_config(self, *args) -> Dict[str, Any]:
        """Show or set plugin configuration"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin config <name> [key] [value]'
            }

        name = args[0]
        
        if len(args) == 1:
            # Show all config
            config = self.plugin_manager.get_config(name)
            if not config:
                return {
                    'success': False,
                    'error': f'Plugin {name} not found or has no configuration'
                }
            
            output = f"Configuration for {name}:\n"
            for key, value in config.items():
                output += f"  {key}: {value}\n"
            
            return {
                'success': True,
                'output': output
            }
        
        elif len(args) == 2:
            # Show specific config key
            key = args[1]
            config = self.plugin_manager.get_config(name)
            if not config or key not in config:
                return {
                    'success': False,
                    'error': f'Configuration key {key} not found for plugin {name}'
                }
            
            return {
                'success': True,
                'output': f"{name}.{key} = {config[key]}"
            }
        else:
            # Set config value
            key = args[1]
            value = args[2]
            set_result = self.plugin_manager.set_config(name, key, value)
            
            if set_result:
                return {
                    'success': True,
                    'output': f'Configuration updated: {name}.{key} = {value}'
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to set configuration: {name}.{key}'
                }

    # ============================================================
    # PLUGIN LOGS
    # ============================================================
    async def cmd_logs(self, *args) -> Dict[str, Any]:
        """Show plugin logs"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin logs <name> [lines]'
            }

        name = args[0]
        lines = int(args[1]) if len(args) > 1 else 50
        
        logs = self.plugin_manager.get_logs(name, lines)

        if not logs:
            return {
                'success': True,
                'output': f'No logs available for plugin: {name}'
            }

        output = f"Last {len(logs)} log entries for {name}:\n"
        for log in logs:
            output += f"  [{log['timestamp']}] {log['level']}: {log['message']}\n"

        return {
            'success': True,
            'output': output
        }

    # ============================================================
    # PLUGIN BACKUP
    # ============================================================
    async def cmd_backup(self, *args) -> Dict[str, Any]:
        """Create plugin backup"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin backup <name> [backup_name]'
            }

        name = args[0]
        backup_name = args[1] if len(args) > 1 else f"{name}_backup"

        backup = self.plugin_manager.create_backup(name, backup_name)

        if backup:
            return {
                'success': True,
                'output': f'Backup created: {backup_name} for plugin {name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to create backup for plugin: {name}'
            }

    async def cmd_restore(self, *args) -> Dict[str, Any]:
        """Restore plugin from backup"""
        if not args:
            return {
                'success': False,
                'error': 'Usage: plugin restore <name> <backup_name>'
            }

        if len(args) < 2:
            return {
                'success': False,
                'error': 'Usage: plugin restore <name> <backup_name>'
            }

        name = args[0]
        backup_name = args[1]
        restored = self.plugin_manager.restore_backup(name, backup_name)

        if restored:
            return {
                'success': True,
                'output': f'Plugin {name} restored from backup: {backup_name}'
            }
        else:
            return {
                'success': False,
                'error': f'Failed to restore plugin {name} from backup: {backup_name}'
            }
