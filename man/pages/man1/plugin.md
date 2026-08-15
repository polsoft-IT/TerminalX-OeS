# plugin - Plugin System [GODMODE]

## NAME

plugin [plug] - Plugin System [GODMODE] - Plugin loading, hooks, events, sandbox, permissions, AI plugins

## DESCRIPTION

The plugin command provides access to TerminalX's advanced plugin system. This GODMODE system allows for dynamic plugin loading, event hooks, sandboxed execution, granular permission management, and AI plugin management.

## SYNOPSIS

```
plugin install <file_or_directory>
plugin remove <name>
plugin update <name>
plugin search <query>
plugin enable <name>
plugin disable <name>
plugin list
plugin info <name>
plugin reload <name> | reload all
plugin hooks
plugin events
plugin sandbox <name>
plugin permissions [name]
plugin status
plugin start
plugin stop
plugin verify <name>
plugin dependencies <name>
plugin migrate <name> <target_version>
plugin config <name> [key] [value]
plugin logs <name> [lines]
plugin backup <name> [backup_name]
plugin restore <name> <backup_name>
plugin export <name> [output_file]
plugin import <config_file>
plugin clean <name> | clean all
plugin reset <name>
plugin test <name>
plugin ai_list
plugin ai_load <plugin>
plugin ai_unload <plugin>
plugin ai_reload <plugin>
```

## OPTIONS

### INSTALLATION/REMOVAL

- `install <file_or_directory>` - Install plugin from file or directory
- `remove <name>` - Remove plugin
- `update <name>` - Update plugin to latest version
- `search <query>` - Search for available plugins

### ENABLE/DISABLE

- `enable <name>` - Enable plugin
- `disable <name>` - Disable plugin

### INFORMATION

- `list` - List all installed plugins
- `info <name>` - Show detailed plugin information
- `status` - Show plugin manager status
- `dependencies <name>` - Show plugin dependencies

### RELOAD

- `reload <name>` - Reload specific plugin
- `reload all` - Reload all plugins

### HOOKS/EVENTS

- `hooks` - List registered hooks
- `events` - List subscribed events

### SANDBOX/PERMISSIONS

- `sandbox <name>` - Show sandbox status for plugin
- `permissions [name]` - Show plugin permissions (all or specific)

### MANAGER CONTROL

- `start` - Start plugin manager
- `stop` - Stop plugin manager

### VERIFICATION

- `verify <name>` - Verify plugin signature and integrity

### MIGRATION

- `migrate <name> <target_version>` - Migrate plugin data to new version

### CONFIGURATION

- `config <name>` - Show all plugin configuration
- `config <name> <key>` - Show specific configuration key
- `config <name> <key> <value>` - Set configuration value

### LOGS

- `logs <name> [lines]` - Show plugin logs (default 50 lines)

### BACKUP/RESTORE

- `backup <name> [backup_name]` - Create plugin backup
- `restore <name> <backup_name>` - Restore plugin from backup

### EXPORT/IMPORT

- `export <name> [output_file]` - Export plugin configuration
- `import <config_file>` - Import plugin configuration

### CLEANUP

- `clean <name>` - Clean plugin cache and temporary files
- `clean all` - Clean all plugins
- `reset <name>` - Reset plugin to default state

### TESTING

- `test <name>` - Test plugin functionality

### AI PLUGINS

- `ai_list` - List all loaded AI plugins
- `ai_load <plugin>` - Load an AI plugin
- `ai_unload <plugin>` - Unload an AI plugin
- `ai_reload <plugin>` - Reload an AI plugin

## EXAMPLES

### Installation/Removal

```
plugin list
plugin install my_plugin.zip
plugin install /path/to/plugin_directory
plugin remove my_plugin
plugin update my_plugin
plugin search security
```

### Enable/Disable

```
plugin enable my_plugin
plugin disable my_plugin
```

### Information

```
plugin info my_plugin
plugin status
plugin dependencies my_plugin
```

### Reload

```
plugin reload my_plugin
plugin reload all
```

### Hooks/Events

```
plugin hooks
plugin events
```

### Sandbox/Permissions

```
plugin sandbox my_plugin
plugin permissions
plugin permissions my_plugin
```

### Manager Control

```
plugin start
plugin stop
```

### Verification

```
plugin verify my_plugin
```

### Migration

```
plugin migrate my_plugin 2.0.0
```

### Configuration

```
plugin config my_plugin
plugin config my_plugin timeout
plugin config my_plugin timeout 30
```

### Logs

```
plugin logs my_plugin
plugin logs my_plugin 100
```

### Backup/Restore

```
plugin backup my_plugin
plugin backup my_plugin backup_v1
plugin restore my_plugin backup_v1
```

### Export/Import

```
plugin export my_plugin my_plugin_config.json
plugin import my_plugin_config.json
```

### Cleanup

```
plugin clean my_plugin
plugin clean all
plugin reset my_plugin
```

### Testing

```
plugin test my_plugin
```

### AI Plugins

```
plugin ai_list
plugin ai_load security_plugin
plugin ai_unload auth_plugin
plugin ai_reload my_plugin
```

## GROUPS

### 🟩 Installation/Removal
- Plugin installation from files or directories
- Plugin removal and updates
- Plugin search functionality

### 🔹 Enable/Disable
- Plugin state management
- Enable/disable functionality
- Runtime control

### 🟧 Information
- Plugin listing and details
- Manager status
- Dependency tracking

### 🟦 Reload
- Hot-reload plugins
- Batch reloading
- Runtime updates

### 🟩 Hooks/Events
- Hook registration
- Event subscription
- System integration

### 🟧 Sandbox/Permissions
- Sandboxed execution
- Permission management
- Security controls

### 🟦 Manager Control
- Start/stop manager
- Lifecycle management
- System control

### 🟩 Verification
- Signature verification
- Integrity checking
- Security validation

### 🟧 Migration
- Data migration
- Version transitions
- Compatibility handling

### 🟦 Configuration
- Plugin configuration
- Runtime settings
- Parameter management

### 🟩 Logs
- Plugin logging
- Log viewing
- Debugging support

### 🟧 Backup/Restore
- Configuration backup
- State restoration
- Data preservation

### 🟦 Export/Import
- Configuration export
- Configuration import
- Portability

### 🟩 Cleanup
- Cache management
- Temporary file cleanup
- State reset

### 🟧 Testing
- Plugin testing
- Functionality verification
- Quality assurance

### 🟦 AI Plugins
- AI plugin management
- Load/unload operations
- Specialized AI features

## SEE ALSO

man(1), modman(1), cd(1), system(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
