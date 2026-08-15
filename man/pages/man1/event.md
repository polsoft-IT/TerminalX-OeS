# event - Event Bus v2 [GODMODE]

## NAME

event [eve] - Event Bus v2 [GODMODE] - Global event system for inter-module communication

## DESCRIPTION

The event command provides access to TerminalX's advanced event bus system v2. This GODMODE system offers event-driven communication between modules with async/sync modes, filters, hooks, logging, diagnostics, and state management.

## SYNOPSIS

```
event emit <event_name> [data]
event status
event config [key=value]
event flush
event metadata
event errors
event autofix
event export
event api
```

## OPTIONS

### Event Commands
- `emit <event_name> [data]` - Emit an event to subscribers
- `status` - Get event bus diagnostic status
- `config [key=value]` - Show or update configuration
- `flush` - Flush event queue
- `metadata` - Get event bus metadata
- `errors` - Get error logs
- `autofix` - Auto-fix common event bus issues
- `export` - Export event bus state
- `api` - List available API methods

## EXAMPLES

### Event Operations
```
event emit system.start
event emit user.login {"user": "admin"}
event status
event config mode=async
event flush
```

### Diagnostics
```
event metadata
event errors
event autofix
event export
event api
```

## EVENT BUS FEATURES

### Core Features
- **Async/Sync Modes**: Configurable event processing modes
- **Event Queue**: Async event queue with configurable size
- **Filters**: Global event filtering system
- **Hooks**: Event hooks for pre/post processing
- **Logging**: Comprehensive event logging
- **Diagnostics**: Built-in diagnostic tools

### Configuration
- `mode`: async/sync processing mode
- `log_level`: normal/verbose/silent
- `max_queue`: maximum queue size (default: 10000)
- `auto_flush`: auto-flush on shutdown

### API Methods
- `emit`: Emit events
- `subscribe`: Subscribe to events
- `unsubscribe`: Unsubscribe from events
- `flush`: Flush event queue
- `add_filter`: Add global filter
- `add_hook`: Add event hook
- `diagnose`: Get diagnostics
- `auto_fix`: Auto-fix issues

## COMPATIBILITY

The event bus is compatible with all TerminalX modules:
- shield: ✅
- sandbox: ✅
- kernel_hooks: ✅
- firewall: ✅
- threat_intel: ✅
- plugins: ✅
- modules: ✅

## SEE ALSO

man(1), help(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
