# developer - Developer Command Handlers
# VERSION: 1.0.6
# UPDATED: 2026-08-14

## NAME

developer - Developer command handlers for module development (alias for dev)

## DESCRIPTION

The developer command provides comprehensive development tools for module management,
building, testing, debugging, and optimization. Includes 39 commands across
10 categories: build & clean, run & debug, testing, dependencies, API, logging,
versioning, documentation, system-level operations, and AI features.
This is an alias for the dev command.

## SYNOPSIS
```
🟦 1. BUILD & CLEAN COMMANDS
developer build <module>              — build module
developer rebuild <module>            — full rebuild + clean
developer clean <module>               — remove cache + artifacts
developer export <module>             — export module as package
developer import <file>               — import module package

🟦 2. RUN & DEBUG COMMANDS
developer run <module>                — run module in dev mode
developer debug <module>              — debug mode with extended logs
developer sandbox <module>            — isolated sandbox execution
developer profile <module>            — CPU/RAM/IO profiling

🟦 3. TESTING COMMANDS
developer test <module>               — run unit + integration tests
developer test-all                    — test all modules + plugins
developer compat <module>             — compatibility check

🟦 4. DEPENDENCY COMMANDS
developer deps <module>               — show dependencies
developer deps-install <module>       — install missing deps
developer deps-tree <module>          — dependency tree

🟦 5. API COMMANDS
developer api <module>                — show module API
developer api-call <module> <function> [args] — call API function
developer api-doc <module>            — generate API documentation

🟦 6. LOGGING COMMANDS
developer logs <module>               — show logs
developer logs-clear <module>         — clear logs
developer logs-watch <module>         — live log stream

🟦 7. VERSIONING COMMANDS
developer version <module>            — show version
developer version-set <module> <x.y.z> — set version
developer version-history <module>    — version history

🟦 8. DOCUMENTATION COMMANDS
developer doc <module>                — generate docs
developer doc-export <module>         — export docs
developer doc-open <module>           — open docs viewer

🟦 9. SYSTEM-LEVEL COMMANDS
developer system diag                 — full system diagnostics
developer system fix                  — auto-repair
developer system reset                — reset developer environment
developer system profile              — system-wide profiling
developer system hooks                — list hooks
developer system events               — list events

🟦 10. AI COMMANDS
developer ai-optimize <module/plugin> — AI code optimization
developer ai-profile <module/plugin>  — AI profiling
developer ai-hooks <module/plugin>    — AI hook analysis
developer ai-memory <module/plugin>   — memory usage analysis
developer ai-reasoning <module/plugin> — logic flow analysis
```

## OPTIONS

**BUILD & CLEAN COMMANDS**
- `build <module>` - Build module with current configuration
- `rebuild <module>` - Full rebuild including cache cleanup
- `clean <module>` - Remove cache and build artifacts
- `export <module>` - Export module as distributable package
- `import <file>` - Import module package from file

**RUN & DEBUG COMMANDS**
- `run <module>` - Run module in development mode
- `debug <module>` - Run with extended debug logging
- `sandbox <module>` - Execute in isolated sandbox environment
- `profile <module>` - Profile CPU, RAM, and I/O usage

**TESTING COMMANDS**
- `test <module>` - Run unit and integration tests
- `test-all` - Test all modules and plugins
- `compat <module>` - Check compatibility with system

**DEPENDENCY COMMANDS**
- `deps <module>` - Show module dependencies
- `deps-install <module>` - Install missing dependencies
- `deps-tree <module>` - Display dependency tree structure

**API COMMANDS**
- `api <module>` - Show available module API functions
- `api-call <module> <function> [args]` - Call API function with arguments
- `api-doc <module>` - Generate API documentation

**LOGGING COMMANDS**
- `logs <module>` - Show module logs
- `logs-clear <module>` - Clear module logs
- `logs-watch <module>` - Live stream module logs

**VERSIONING COMMANDS**
- `version <module>` - Show current module version
- `version-set <module> <x.y.z>` - Set module version
- `version-history <module>` - Show version history

**DOCUMENTATION COMMANDS**
- `doc <module>` - Generate module documentation
- `doc-export <module>` - Export documentation to file
- `doc-open <module>` - Open documentation viewer

**SYSTEM-LEVEL COMMANDS**
- `system diag` - Full system diagnostics
- `system fix` - Auto-repair detected issues
- `system reset` - Reset developer environment
- `system profile` - System-wide performance profiling
- `system hooks` - List registered hooks
- `system events` - List system events

**AI COMMANDS**
- `ai-optimize <module/plugin>` - AI-powered code optimization
- `ai-profile <module/plugin>` - AI performance profiling
- `ai-hooks <module/plugin>` - AI hook analysis
- `ai-memory <module/plugin>` - AI memory usage analysis
- `ai-reasoning <module/plugin>` - AI logic flow analysis

## EXAMPLES
```
# Build and clean
developer build mymodule
developer rebuild mymodule
developer clean mymodule
developer export mymodule
developer import mymodule-1.0.0.tar.gz

# Run and debug
developer run mymodule
developer debug mymodule
developer sandbox mymodule
developer profile mymodule

# Testing
developer test mymodule
developer test-all
developer compat mymodule

# Dependencies
developer deps mymodule
developer deps-install mymodule
developer deps-tree mymodule

# API
developer api mymodule
developer api-call mymodule initialize
developer api-doc mymodule

# Logging
developer logs mymodule
developer logs-clear mymodule
developer logs-watch mymodule

# Versioning
developer version mymodule
developer version-set mymodule 2.0.0
developer version-history mymodule

# Documentation
developer doc mymodule
developer doc-export mymodule
developer doc-open mymodule

# System-level
developer system diag
developer system fix
developer system reset
developer system profile
developer system hooks
developer system events

# AI
developer ai-optimize mymodule
developer ai-profile mymodule
developer ai-hooks mymodule
developer ai-memory mymodule
developer ai-reasoning mymodule
```

## SEE ALSO

dev(1), module(1), build(1), python(1), sys(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
