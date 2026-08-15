# task - Task Commands

## NAME

task - Task commands (add, run, stats, history)

## DESCRIPTION

The task command provides access to TerminalX's task management system. Add, run, monitor, and manage background tasks with 20 available commands.

## SYNOPSIS

```
task add <command>
task run <id>
task list
task stop <id>
task pause <id>
task resume <id>
task stats
task history
task priority <id> <level>
task dependencies <id> <deps>
task schedule <time> <command>
task repeat <id> <interval>
task logs <id>
task clean
task export <file>
task import <file>
```

## OPTIONS

- `add <command>` - Add a new task
- `run <id>` - Run a specific task
- `list` - List all tasks
- `stop <id>` - Stop a running task
- `stats` - Show task statistics
- `history` - Show task execution history
- `priority <id> <level>` - Set task priority
- `dependencies <id> <deps>` - Set task dependencies

## EXAMPLES

```
task add "python script.py"
task run 1
task list
task stats
task history
```

## SEE ALSO

man(1), build(1), modules(1), report(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
