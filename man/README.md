# TerminalX Manual Page System

## Overview

The TerminalX Manual Page System (ManEngine) provides comprehensive documentation for all TerminalX commands, modules, and features. It offers advanced search capabilities, caching, and multiple output formats.

## Features

- **Multi-source Integration**: Man pages from multiple sources (local files, embedded docs, external APIs)
- **Advanced Search**: Full-text search, wildcard patterns, and fuzzy matching
- **Caching System**: Intelligent caching for fast access to frequently used pages
- **Multiple Formats**: Support for Markdown, HTML, and plain text output
- **Custom Pages**: Ability to add custom man pages
- **Statistics**: Detailed statistics about man page usage and sources
- **Section Organization**: Traditional Unix-style section organization

## Commands

### Basic Commands

```
man show <page_name> [section]  - Display a specific man page
man search <query>               - Search for man pages matching query
man list [section]               - List all available man pages
man wildcard <pattern>           - Search using wildcard patterns
man fuzzy <query>                - Fuzzy search with approximate matching
```

### Management Commands

```
man add <name> <content_file> [section]  - Add custom man page
man remove <page_name>                    - Remove custom man page
man export <page_name> <output_file> [format]  - Export man page
```

### Cache Management

```
man stats           - Display man engine statistics
man refresh         - Refresh man pages from sources
man cache_clear     - Clear the man page cache
man cache_stats     - Display cache statistics
man cleanup         - Clean up expired cache entries
man rebuild         - Rebuild cache from all sources
man source_stats    - Display statistics about sources
```

### Special Commands

```
man readme          - Display this README file
```

## Sections

Man pages are organized into traditional Unix sections:

1. **General commands** - User commands
2. **System calls** - Kernel system calls
3. **Library functions** - Programming libraries
4. **Special files** - Device files and drivers
5. **File formats** - Configuration and data files
6. **Games** - Games and amusements
7. **Miscellaneous** - Miscellaneous topics
8. **System administration** - System admin commands
9. **Kernel** - Kernel internals

## Available Man Pages

The system includes man pages for the following modules:

### GODMODE Systems
- `kernel` - Kernel Hooks Engine
- `proc` - Process Monitor Engine
- `advshield` - Advanced Shield
- `modman` - Module Manager
- `plugin` - Plugin System
- `geo` - Geolocation Engine
- `sysopt` - System Optimizer v2

### Standard Systems
- `ai` - AI Commands
- `gui` - GUI Commands
- `network` - Network Commands
- `shield` - Security Commands
- `cloud` - Cloud Commands
- `modules` - Module Commands
- `metadata` - Metadata Commands
- `build` - Build Commands
- `task` - Task Commands
- `version` - Version Management
- `report` - Report Engine

### Library Systems
- `emoji` - Emoji Library
- `unicode` - Unicode Library
- `figlet` - FIGLET Engine
- `ansi` - ANSI Colors
- `anim` - Animations
- `widgets` - GUI Widgets

### Network Tools
- `wifi` - WiFi PRO Commands
- `lan` - LAN Commands
- `ethernet` - Ethernet Commands

### File System
- `fs` - File System Commands

### System
- `sys` - System Commands
- `auth` - Authentication Commands
- `archive` - Archive Commands
- `display` - Display Commands
- `dev` - Development Commands
- `python` - Python Commands
- `engine` - Engine Commands

### Documentation
- `man` - Manual Page System
- `help` - Help System

## Examples

### Displaying Man Pages

```bash
man show man
man show kernel
man show sysopt
man show man 1
```

### Searching

```bash
man search network
man search "pagefile"
man wildcard *net*
man fuzzy network
```

### Listing

```bash
man list
man list 1
```

### Custom Pages

```bash
man add mycommand mycommand.md 1
man remove mycommand
man export man man_output.html html
```

### Cache Management

```bash
man stats
man cache_clear
man rebuild
man source_stats
```

## Configuration

Man engine configuration is stored in:
- `~/.terminalx/config/man/man.json`

### Configuration Options

```json
{
  "cache_enabled": true,
  "cache_ttl": 3600,
  "auto_refresh": false,
  "sources": ["local", "embedded"],
  "default_section": 1
}
```

## Files

- `~/.terminalx/man/cache/` - Cache directory
- `~/.terminalx/config/man/man.json` - Configuration file
- `terminal/man/pages/man1/` - Section 1 man pages
- `terminal/man/README.md` - This file

## API Reference

### ManEngine Class

```python
from man import ManEngine

# Initialize
engine = ManEngine()
await engine.initialize()

# Show page
content = await engine.show_page("man", section=1)

# Search
results = await engine.search("network")

# List pages
pages = await engine.list_pages(section=1)

# Add custom page
await engine.add_page("mycommand", content, section=1)
```

## Tips

- Use `man search` for finding relevant pages
- Use `man wildcard` for pattern matching
- Use `man fuzzy` for approximate matching
- Clear cache if pages are outdated: `man cache_clear`
- Rebuild cache after updates: `man rebuild`
- Check statistics for usage insights: `man stats`

## See Also

- `help` - TerminalX help system
- `commands` - Command reference
- `terminal` - TerminalX main documentation

## Author

Sebastian Januchowski - polsoft.ITS™ Dev

## Version

ManEngine v1.0.0
