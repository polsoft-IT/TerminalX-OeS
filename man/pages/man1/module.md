# module - Module System [GODMODE]

## NAME

module [mod] - Module System [GODMODE] - Module loading, dependencies, configuration, diagnostics, resources, integration, GODMODE

## DESCRIPTION

The module command provides access to TerminalX's advanced module system. This GODMODE system allows for dynamic module loading, dependency management, configuration control, diagnostic features, resource monitoring, plugin integration, and GODMODE capabilities.

## SYNOPSIS

```
module list [--full] [--tree]
module info <name> [--meta] [--api] [--commands]
module enable <name>
module disable <name>
module reload <name>
module restart <name>
module install <source>
module uninstall <name>
module update <name> | --all
module check <name> | --all
module registry rebuild
module registry verify
module registry clean
module registry export <filepath>
module registry import <filepath>
module deps <name> [--reverse] [--missing] [--install-missing]
module config get <name> <key>
module config set <name> <key> <value>
module config reset <name>
module config export <name> <filepath>
module config import <name> <filepath>
module diag <name> [--full] [--fix] [--errors-only] | --system
module resources <name> [--mem] [--cpu] [--io] [--threads] | --all
module link <module_name> <plugin_name>
module unlink <module_name> <plugin_name>
module compat <name> [--check-version <ver>] | --list-all
module docs <name> [--show] [--list-docs] [--export <path>]
module godmode <name> [--enable] [--disable] | --status
```

## OPTIONS

### CORE COMMANDS

- `list [--full] [--tree]` - List modules (simple, full, or tree view)
- `info <name> [--meta] [--api] [--commands]` - Show module information
- `enable <name>` - Enable module
- `disable <name>` - Disable module
- `reload <name>` - Reload module
- `restart <name>` - Restart module
- `install <source>` - Install module from source
- `uninstall <name>` - Uninstall module
- `update <name>` - Update specific module
- `update --all` - Update all modules
- `check <name>` - Check module health
- `check --all` - Check all modules

### REGISTRY COMMANDS

- `registry rebuild` - Rebuild module registry
- `registry verify` - Verify module registry
- `registry clean` - Clean module registry
- `registry export <filepath>` - Export registry to file
- `registry import <filepath>` - Import registry from file

### DEPENDENCY COMMANDS

- `deps <name>` - Show module dependencies
- `deps <name> --reverse` - Show modules that depend on this module
- `deps <name> --missing` - Show missing dependencies
- `deps <name> --install-missing` - Install missing dependencies

### CONFIG COMMANDS

- `config get <name> <key>` - Get configuration value
- `config set <name> <key> <value>` - Set configuration value
- `config reset <name>` - Reset module configuration
- `config export <name> <filepath>` - Export configuration
- `config import <name> <filepath>` - Import configuration

### DIAGNOSTIC COMMANDS

- `diag <name>` - Basic module diagnostic
- `diag <name> --full` - Full diagnostic report
- `diag <name> --fix` - Diagnostic with automatic fixes
- `diag <name> --errors-only` - Show only errors
- `diag --system` - System-wide diagnostic

### RESOURCE COMMANDS

- `resources <name> --mem` - Show memory usage
- `resources <name> --cpu` - Show CPU usage
- `resources <name> --io` - Show I/O statistics
- `resources <name> --threads` - Show thread count
- `resources <name> --all` - Show all resources

### INTEGRATION COMMANDS

- `link <module_name> <plugin_name>` - Link module with plugin
- `unlink <module_name> <plugin_name>` - Unlink module from plugin
- `compat <name>` - Show module compatibility
- `compat <name> --check-version <ver>` - Check compatibility with version
- `compat --list-all` - List all compatibility information

### DOCS COMMANDS

- `docs <name> --show` - Show module documentation
- `docs <name> --list-docs` - List available documents
- `docs <name> --export <path>` - Export documentation

### GODMODE COMMANDS

- `godmode <name> --enable` - Enable GODMODE for module
- `godmode <name> --disable` - Disable GODMODE for module
- `godmode <name> --status` - Show GODMODE status

## EXAMPLES

### Core Commands

```
module list
module list --full
module list --tree
module info core
module info core --meta
module info core --api
module info core --commands
module enable security
module disable security
module reload core
module restart core
module install /path/to/module
module uninstall security
module update core
module update --all
module check core
module check --all
```

### Registry Commands

```
module registry rebuild
module registry verify
module registry clean
module registry export /path/to/registry.json
module registry import /path/to/registry.json
```

### Dependency Commands

```
module deps security
module deps security --reverse
module deps security --missing
module deps security --install-missing
```

### Config Commands

```
module config get core timeout
module config set core timeout 30
module config reset core
module config export core /path/to/config.json
module config import core /path/to/config.json
```

### Diagnostic Commands

```
module diag core
module diag core --full
module diag core --fix
module diag core --errors-only
module diag --system
```

### Resource Commands

```
module resources core --mem
module resources core --cpu
module resources core --io
module resources core --threads
module resources core --all
```

### Integration Commands

```
module link security logger_plugin
module unlink security logger_plugin
module compat security
module compat security --check-version 2.0.0
module compat --list-all
```

### Docs Commands

```
module docs core --show
module docs core --list-docs
module docs core --export /path/to/docs/
```

### GODMODE Commands

```
module godmode core --enable
module godmode core --disable
module godmode core --status
```

## GROUPS

### 🟩 Core Commands
- Module listing and information
- Enable/disable operations
- Install/uninstall/update
- Health checking

### 🔹 Registry Commands
- Registry management
- Import/export operations
- Verification and cleaning

### 🟧 Dependency Commands
- Dependency tracking
- Reverse dependency lookup
- Missing dependency handling

### 🟦 Config Commands
- Configuration management
- Get/set/reset operations
- Import/export

### 🟩 Diagnostic Commands
- Module health checks
- System-wide diagnostics
- Automatic fixing

### 🟧 Resource Commands
- Memory monitoring
- CPU usage tracking
- I/O statistics
- Thread monitoring

### 🟦 Integration Commands
- Plugin linking
- Compatibility checking
- Version management

### 🟩 Docs Commands
- Documentation access
- Document listing
- Export operations

### 🟧 GODMODE Commands
- GODMODE enable/disable
- Status checking
- Advanced features

## SEE ALSO

man(1), plugin(1), modman(1), system(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
