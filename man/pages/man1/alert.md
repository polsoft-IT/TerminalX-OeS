# alert(1) - TerminalX Alert Commands

## NAME

alert - Alert module commands for system notifications and alerts

## DESCRIPTION

The alert command provides access to TerminalX's alert module for creating
and managing system alerts, notifications, and warnings with various priority
levels and types.

## SYNOPSIS

```
alert create <title> <message> [type] [priority]
alert list
alert show <id>
alert clear [id]
alert config [key=value]
alert stats
```

## OPTIONS

- `create` - Create a new alert
- `list` - List all alerts
- `show` - Show details of a specific alert
- `clear` - Clear alerts (all or specific)
- `config` - Show or update configuration
- `stats` - Show alert statistics

## ALERT TYPES

- `info` - Informational alert
- `warning` - Warning alert
- `error` - Error alert
- `critical` - Critical alert

## PRIORITY LEVELS

- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority
- `urgent` - Urgent priority

## EXAMPLES

```
alert create "System Update" "New update available" info medium
alert list
alert show 123
alert clear
alert stats
```

## SEE ALSO

notify(1), notification(1), shield(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev

