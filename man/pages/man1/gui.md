# gui - GUI Commands

## NAME

gui - GUI commands (create windows, widgets, etc.)

## DESCRIPTION

The gui command provides access to TerminalX's graphical user interface capabilities. Create windows, widgets, and interactive GUI elements for enhanced user experience with 26 available commands.

## SYNOPSIS

```
gui window create <title>
gui window close <id>
gui window resize <id> <width> <height>
gui window move <id> <x> <y>
gui window maximize <id>
gui window minimize <id>
gui widget add <type> <params>
gui widget remove <id>
gui widget update <id> <params>
gui layout set <layout>
gui theme set <theme>
gui show <id>
gui hide <id>
gui focus <id>
gui dialog <type> <message>
gui menu create <name>
gui menu add <menu> <item>
gui toolbar create <name>
gui statusbar set <text>
gui tab add <tab>
gui tab remove <tab>
gui splash <image>
```

## OPTIONS

- `window create <title>` - Create a new window
- `window close <id>` - Close a window
- `widget add <type> <params>` - Add a widget (button, input, etc.)
- `widget remove <id>` - Remove a widget
- `layout set <layout>` - Set window layout
- `theme set <theme>` - Set GUI theme
- `show <id>` - Show window/widget
- `hide <id>` - Hide window/widget

## EXAMPLES

```
gui window create "My Window"
gui widget add button --text "Click Me"
gui theme set dark
gui show 1
```

## SEE ALSO

man(1), widgets(1), display(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
