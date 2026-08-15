# figlet - FIGLET Commands

## NAME

figlet - FIGLET commands (render, fonts, load, unload, stats)

## DESCRIPTION

The figlet command provides access to TerminalX's FIGLET text rendering engine. Create ASCII art text with various fonts with 7 available commands.

## SYNOPSIS

```
figlet render <text>
figlet fonts list
figlet fonts load <font>
figlet fonts unload <font>
figlet fonts default <font>
figlet stats
figlet preview <font>
```

## OPTIONS

- `render <text>` - Render text as ASCII art
- `fonts list` - List available FIGLET fonts
- `fonts load <font>` - Load a FIGLET font
- `fonts unload <font>` - Unload a FIGLET font
- `fonts default <font>` - Set default font
- `stats` - Show FIGLET engine statistics
- `preview <font>` - Preview a font

## EXAMPLES

```
figlet render "Hello World"
figlet fonts list
figlet fonts load big
figlet render "Test"
```

## SEE ALSO

man(1), ansi(1), unicode(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
