# dev - Developer Command Handlers
# VERSION: 1.0.6
# UPDATED: 2026-08-14

## NAME

dev - Developer command handlers for module development

## DESCRIPTION

The dev command provides comprehensive development tools for module management,
building, testing, debugging, and optimization. Includes 39 commands across
10 categories: build & clean, run & debug, testing, dependencies, API, logging,
versioning, documentation, system-level operations, and AI features.

## SYNOPSIS
```
🟦 1. BUILD & CLEAN COMMANDS
dev build <module>              — build module
dev rebuild <module>            — full rebuild + clean
dev clean <module>               — remove cache + artifacts
dev export <module>             — export module as package
dev import <file>               — import module package

🟦 2. RUN & DEBUG COMMANDS
dev run <module>                — run module in dev mode
dev debug <module>              — debug mode with extended logs
dev sandbox <module>            — isolated sandbox execution
dev profile <module>            — CPU/RAM/IO profiling

🟦 3. TESTING COMMANDS
dev test <module>               — run unit + integration tests
dev test-all                    — test all modules + plugins
dev compat <module>             — compatibility check

🟦 4. DEPENDENCY COMMANDS
dev deps <module>               — show dependencies
dev deps-install <module>       — install missing deps
dev deps-tree <module>          — dependency tree

🟦 5. API COMMANDS
dev api <module>                — show module API
dev api-call <module> <function> [args] — call API function
dev api-doc <module>            — generate API documentation

🟦 6. LOGGING COMMANDS
dev logs <module>               — show logs
dev logs-clear <module>         — clear logs
dev logs-watch <module>         — live log stream

🟦 7. VERSIONING COMMANDS
dev version <module>            — show version
dev version-set <module> <x.y.z> — set version
dev version-history <module>    — version history

🟦 8. DOCUMENTATION COMMANDS
dev doc <module>                — generate docs
dev doc-export <module>         — export docs
dev doc-open <module>           — open docs viewer

🟦 9. SYSTEM-LEVEL COMMANDS
dev system diag                 — full system diagnostics
dev system fix                  — auto-repair
dev system reset                — reset developer environment
dev system profile              — system-wide profiling
dev system hooks                — list hooks
dev system events               — list events

🟦 10. AI COMMANDS
dev ai-optimize <module/plugin> — AI code optimization
dev ai-profile <module/plugin>  — AI profiling
dev ai-hooks <module/plugin>    — AI hook analysis
dev ai-memory <module/plugin>   — memory usage analysis
dev ai-reasoning <module/plugin> — logic flow analysis
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
dev build mymodule
dev rebuild mymodule
dev clean mymodule
dev export mymodule
dev import mymodule-1.0.0.tar.gz

# Run and debug
dev run mymodule
dev debug mymodule
dev sandbox mymodule
dev profile mymodule

# Testing
dev test mymodule
dev test-all
dev compat mymodule

# Dependencies
dev deps mymodule
dev deps-install mymodule
dev deps-tree mymodule

# API
dev api mymodule
dev api-call mymodule initialize
dev api-doc mymodule

# Logging
dev logs mymodule
dev logs-clear mymodule
dev logs-watch mymodule

# Versioning
dev version mymodule
dev version-set mymodule 2.0.0
dev version-history mymodule

# Documentation
dev doc mymodule
dev doc-export mymodule
dev doc-open mymodule

# System-level
dev system diag
dev system fix
dev system reset
dev system profile
dev system hooks
dev system events

# AI
dev ai-optimize mymodule
dev ai-profile mymodule
dev ai-hooks mymodule
dev ai-memory mymodule
dev ai-reasoning mymodule
```

## SEE ALSO

module(1), build(1), python(1), sys(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
