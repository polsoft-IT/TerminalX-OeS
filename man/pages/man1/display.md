# display - Display Commands

## NAME

display - Display commands (color test, ansi test, fps, theme, font)

## DESCRIPTION

The display command provides access to TerminalX's display and terminal capabilities. Test colors, check performance, change themes, and manage display settings with 21 available commands.

## SYNOPSIS

```
display color test
display ansi test
display fps
display theme list
display theme set <theme>
display theme current
display font list
display font set <font>
display font current
display resolution
display info
display brightness <level>
display contrast <level>
display gamma <level>
display reset
display calibrate
display screenshot
```

## OPTIONS

- `color test` - Test terminal color capabilities
- `ansi test` - Test ANSI escape sequences
- `fps` - Display frame rate information
- `theme list` - List available themes
- `theme set <theme>` - Set display theme
- `font list` - List available fonts
- `font set <font>` - Set terminal font
- `resolution` - Display resolution information
- `info` - Show display information

## EXAMPLES

```
display color test
display fps
display theme list
display theme set dark
display font set monospace
```

## SEE ALSO

man(1), ansi(1), gui(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
