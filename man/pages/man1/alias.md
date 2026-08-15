# alias - Alias Management System v5.0.0

## NAME

alias - Advanced GODMODE v5 alias management system for TerminalX OeS

## DESCRIPTION

The alias command provides comprehensive alias management capabilities for TerminalX. It allows creating, editing, deleting, handling, managing, and registering aliases throughout the system. The system includes project scanning for available commands, testing functionality, statistics, import/export capabilities, and full integration with the TerminalX command system.

## SYNOPSIS

```
alias list [--disabled]
alias cmd [project_dir]
alias add <command> ; <alias> [description] [category]
alias del <alias>
alias edit <old_alias> ; <new_alias>
alias reg <alias>
alias reg all
alias unreg <alias>
alias unreg all
alias test <alias>
alias test_all
alias stats
alias export <file_path>
alias import <file_path> [--overwrite]
alias clear
alias search <pattern>
alias info <alias>
```

## OPTIONS

- `list [--disabled]` - List all aliases (include disabled with --disabled)
- `cmd [project_dir]` - Scan project directory for available commands
- `add <command> ; <alias> [description] [category]` - Add a new alias
- `del <alias>` - Delete an alias
- `edit <old_alias> ; <new_alias>` - Edit an alias name
- `reg <alias>` - Register a specific alias
- `reg all` - Register all aliases
- `unreg <alias>` - Unregister a specific alias
- `unreg all` - Unregister all aliases
- `test <alias>` - Test a specific alias
- `test_all` - Test all aliases
- `stats` - Show alias statistics
- `export <file_path>` - Export aliases to file
- `import <file_path> [--overwrite]` - Import aliases from file
- `clear` - Clear all aliases
- `search <pattern>` - Search aliases by pattern
- `info <alias>` - Show detailed alias information

## EXAMPLES

```
# List all aliases
alias list

# Scan project for available commands
alias cmd

# Add a new alias
alias add "network list" ; "netlist" "Quick network list" "network"

# Delete an alias
alias del netlist

# Edit an alias name
alias edit netlist ; nl

# Register all aliases
alias reg all

# Test an alias
alias test netlist

# Show statistics
alias stats

# Export aliases
alias export /tmp/aliases.json

# Import aliases
alias import /tmp/aliases.json --overwrite

# Search aliases
alias search network

# Show alias information
alias info netlist
```

## FEATURES

- **Project Scanning**: Automatically scan project directories for available commands
- **Alias Management**: Create, edit, delete, and manage aliases
- **Registration System**: Register/unregister aliases for system-wide use
- **Testing**: Test individual or all aliases for functionality
- **Statistics**: Comprehensive usage statistics and analytics
- **Import/Export**: Backup and restore alias configurations
- **Search**: Search aliases by name, command, or description
- **Categories**: Organize aliases into custom categories
- **Usage Tracking**: Track alias usage counts for analytics
- **Persistence**: Automatic saving and loading of alias configurations

## CONFIGURATION

Aliases are stored in `~/.terminalx/aliases/aliases.json` with the following structure:

```json
{
  "alias_name": {
    "name": "alias_name",
    "command": "target_command",
    "created": "2026-08-15T00:00:00",
    "modified": "2026-08-15T00:00:00",
    "enabled": true,
    "description": "Alias description",
    "usage_count": 0,
    "category": "custom"
  }
}
```

## COMMAND SCANNING

The `alias cmd` command scans the project directory for available commands:

- Scans `commands/` directory for command classes
- Scans `libs/` directory for command-like modules
- Extracts class names and file locations
- Saves command information to `~/.terminalx/aliases/commands.json`

## TESTING

The alias system includes comprehensive testing:

- `alias test <alias>` - Tests a single alias
- `alias test_all` - Tests all aliases and reports status
- Tests check if aliases are enabled and resolve correctly

## STATISTICS

The `alias stats` command provides:

- Total number of aliases
- Registered vs disabled aliases
- Total usage count
- Category breakdown
- Available commands count

## FILES

- `~/.terminalx/aliases/aliases.json` - Alias storage
- `~/.terminalx/aliases/commands.json` - Command scan results
- `core/alias_engine.py` - Alias engine implementation
- `commands/alias.py` - Alias command handlers

## SEE ALSO

help(1), commands(1), terminal(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev

## VERSION

5.0.0 - 2026-08-15
