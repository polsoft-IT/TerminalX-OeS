# cd - Advanced Directory and Context Navigation

## NAME

cd - Advanced directory and context navigation for TerminalX

## DESCRIPTION

The cd command provides comprehensive directory and context navigation capabilities in TerminalX. It supports standard filesystem navigation, contextual navigation (modules/plugins/system), documentation access, multi-context switching, bookmarks, history management, diagnostic features, AI-assisted navigation, aliases, teleportation (GODMODE), and meta-commands.

## SYNOPSIS

```
cd <path>                    # Standard filesystem navigation
cd .                         # Current directory
cd ..                        # Parent directory
cd ../..                     # Two levels up
cd \                         # Current directory (Windows)
cd /                         # Root directory
cd ~                         # Home directory
cd -                         # Previous directory
cd module:<name>             # Module context
cd mod:<name>                # Module context (short)
cd plugin:<name>             # Plugin context
cd plug:<name>               # Plugin context (short)
cd system                    # System context
cd kernel                    # Kernel context
cd config                    # Config context
cd logs                      # Logs context
cd sandbox                   # Sandbox context
cd ui                        # UI context
cd ansi                      # ANSI context
cd engine                    # Engine context
cd registry                  # Registry context
cd help:<topic>              # Help documentation
cd info:<node>               # Info pages
cd docs:<module>             # Module documentation
cd api:<module>              # Module API
cd <path>;<module>;<plugin> # Multi-context navigation
cd @save <name>              # Save bookmark
cd @load <name>              # Load bookmark
cd @list                     # List bookmarks
cd @del <name>               # Delete bookmark
cd history                   # Show history
cd history --dirs            # Directory history
cd history --modules         # Module history
cd history --plugins         # Plugin history
cd history --clear           # Clear history
cd diag                      # Diagnose current directory
cd diag <path>               # Diagnose specific path
cd diag --fix                # Attempt fixes
cd ?                         # AI suggestions
cd auto                      # AI auto-navigation
cd <keyword>                 # AI search
cd root                      # Go to root
cd home                      # Go to home
cd back                      # Go to previous
cd up                        # Go to parent
cd top                       # Go to highest level
cd teleport <target>         # Teleport (GODMODE)
cd warp <target>             # Warp (GODMODE)
cd jump <bookmark>           # Jump to bookmark
cd --where                   # Show current context
cd --prev                    # Show previous context
cd --contexts                # List contexts
cd --resolve <target>        # Resolve target
```

## OPTIONS

### STANDARD FILESYSTEM NAVIGATION

- `<path>` - Change to specified directory (relative or absolute)
- `.` - Current directory (no change)
- `..` - Parent directory
- `../..` - Two levels up
- `\` - Current directory (Windows style)
- `/` - Root directory
- `~` - Home directory
- `-` - Previous directory (toggle)
- `<relative/path>` - Relative path from current location
- `<absolute/path>` - Absolute path from filesystem root

### CONTEXTUAL NAVIGATION (MODULES/PLUGINS/SYSTEM)

- `module:<name>` - Navigate to module context
- `mod:<name>` - Short form for module navigation
- `plugin:<name>` - Navigate to plugin context
- `plug:<name>` - Short form for plugin navigation
- `system` - System context navigation
- `kernel` - Kernel context
- `config` - Configuration context
- `logs` - Logs context
- `sandbox` - Sandbox context
- `ui` - User interface context
- `ansi` - ANSI context
- `engine` - Engine context
- `registry` - Registry context

### DOCUMENTATION NAVIGATION

- `help:<topic>` - Navigate to help documentation topic
- `info:<node>` - Navigate to info page node
- `docs:<module>` - Navigate to module documentation
- `api:<module>` - Navigate to module API documentation

### MULTI-CONTEXT NAVIGATION

- `<path>;<module>;<plugin>` - Navigate multiple contexts sequentially
- Example: `cd /etc;module:security;plugin:firewall`

### BOOKMARKS (@)

- `@save <name>` - Save current context as bookmark
- `@load <name>` - Load saved bookmark context
- `@list` - List all saved bookmarks
- `@del <name>` - Delete saved bookmark

Bookmarks can save: directories, modules, plugins, documentation, or system contexts.

### HISTORY MANAGEMENT

- `history` - Show full navigation history
- `history --dirs` - Show directory history only
- `history --modules` - Show module history only
- `history --plugins` - Show plugin history only
- `history --clear` - Clear navigation history

### DIAGNOSTIC FEATURES

- `diag` - Diagnose current directory for issues
- `diag <path>` - Diagnose specific path
- `diag --fix` - Attempt automatic fixes (manual intervention may be required)

### AI FEATURES

- `?` - Get AI suggestions based on recent activity
- `auto` - AI auto-navigation to most likely context
- `<keyword>` - AI search for similar directories, modules, or plugins

### ALIASES AND SHORTCUTS

- `root` - Alias for `/` (root directory)
- `home` - Alias for `~` (home directory)
- `back` - Alias for `-` (previous directory)
- `up` - Alias for `..` (parent directory)
- `top` - Navigate to highest project level

### TELEPORTATION (GODMODE)

- `teleport <target>` - Instant context switch to any target
- `warp <module/plugin/system>` - Fast jump to common contexts
- `jump <bookmark>` - Quick jump to saved bookmark

### META-COMMANDS

- `--where` - Show current context (path/module/plugin/system)
- `--prev` - Show previous context
- `--contexts` - List all available contexts
- `--resolve <target>` - Show how target will be interpreted

## EXAMPLES

### Standard Filesystem Navigation

```
cd /home/user/documents
cd ..
cd ../..
cd ~
cd -
cd /var/log
```

### Contextual Navigation

```
cd module:core
cd mod:security
cd plugin:logger
cd plug:auth
cd system
cd kernel
cd config
```

### Documentation Navigation

```
cd help:commands
cd info:filesystem
cd docs:network
cd api:kernel
```

### Multi-Context Navigation

```
cd /etc;module:security;plugin:firewall
cd module:core;plugin:logger
```

### Bookmarks

```
cd @save project_root
cd @load project_root
cd @list
cd @del old_bookmark
```

### History

```
cd history
cd history --dirs
cd history --clear
```

### Diagnostic

```
cd diag
cd diag /var/log
cd diag --fix
```

### AI Features

```
cd ?
cd auto
cd security
cd logs
```

### Aliases

```
cd root
cd home
cd back
cd up
cd top
```

### Teleportation

```
cd teleport module:security
cd warp plugin
cd jump project_root
```

### Meta-Commands

```
cd --where
cd --prev
cd --contexts
cd --resolve module:security
```

## GROUPS

### 🟩 Standard Filesystem Commands
- Basic directory navigation
- Relative and absolute paths
- Special directories (., .., ~, /, -)

### 🔹 Contextual Navigation
- Module contexts (module:, mod:)
- Plugin contexts (plugin:, plug:)
- System contexts (system, kernel, config, logs, etc.)

### 🟧 Documentation Navigation
- Help topics (help:)
- Info pages (info:)
- Module documentation (docs:)
- API documentation (api:)

### 🟦 Multi-Context Navigation
- Sequential context switching
- Complex navigation patterns
- Batch context operations

### 🟩 Bookmarks (@)
- Save/load contexts
- Bookmark management
- Persistent storage

### 🟧 History Management
- Full history tracking
- Filtered history views
- History clearing

### 🟦 Diagnostic Features
- Directory health checks
- Permission analysis
- Issue detection and fixing

### 🟩 AI Features
- Smart suggestions
- Auto-navigation
- Semantic search

### 🟧 Aliases and Shortcuts
- Common command shortcuts
- Convenient navigation aids
- Quick access commands

### 🟦 Teleportation (GODMODE)
- Instant context switching
- Fast navigation jumps
- Advanced features

### 🟩 Meta-Commands
- Context information
- Path resolution
- System introspection

## SEE ALSO

man(1), pwd(1), ls(1), module(1), plugin(1), system(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
