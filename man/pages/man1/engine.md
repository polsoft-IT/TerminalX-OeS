# engine - Engine Commands

## NAME

engine - Engine commands (reload, debug, modules, kernel events, kernel hooks)

## DESCRIPTION

The engine command provides access to TerminalX's core engine management. Reload system components, debug engine operations, manage modules, and interact with kernel events and hooks with 26 available commands.

## SYNOPSIS

```
engine reload
engine reload <component>
engine debug start
engine debug stop
engine debug status
engine debug log <level>
engine modules list
engine modules status
engine modules load <module>
engine modules unload <module>
engine kernel events list
engine kernel events subscribe <event>
engine kernel events unsubscribe <event>
engine kernel hooks list
engine kernel hooks enable <hook>
engine kernel hooks disable <hook>
engine config show
engine config set <key> <value>
engine config reset
engine health
engine metrics
engine version
```

## OPTIONS

- `reload` - Reload entire engine
- `reload <component>` - Reload specific component
- `debug start` - Start engine debugging
- `debug stop` - Stop engine debugging
- `debug status` - Show debug status
- `modules list` - List engine modules
- `modules status` - Show module status
- `kernel events list` - List kernel events
- `kernel hooks list` - List kernel hooks
- `kernel hooks enable <hook>` - Enable kernel hook
- `kernel hooks disable <hook>` - Disable kernel hook

## EXAMPLES

```
engine reload
engine reload ai_module
engine debug start
engine modules status
engine kernel hooks list
```

## SEE ALSO

man(1), kernel(1), modman(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
