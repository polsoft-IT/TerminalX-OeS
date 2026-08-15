# ansi - ANSI Commands

## NAME

ansi - ANSI commands (rgb, gradient, neon, rainbow, fire, matrix, ocean, sunset, stats)

## DESCRIPTION

The ansi command provides access to TerminalX's ANSI color engine. Create colorful terminal output with various color effects and animations with 20 available commands.

## SYNOPSIS

```
ansi rgb <r> <g> <b> <text>
ansi gradient <text>
ansi neon <text>
ansi rainbow <text>
ansi fire <text>
ansi matrix <text>
ansi ocean <text>
ansi sunset <text>
ansi stats
ansi reset
ansi bold <text>
ansi dim <text>
ansi underline <text>
ansi blink <text>
ansi reverse <text>
ansi strikethrough <text>
```

## OPTIONS

- `rgb <r> <g> <b> <text>` - Display text in RGB color
- `gradient <text>` - Display text with gradient effect
- `neon <text>` - Display text with neon effect
- `rainbow <text>` - Display text with rainbow effect
- `fire <text>` - Display text with fire effect
- `matrix <text>` - Display text with matrix effect
- `ocean <text>` - Display text with ocean effect
- `sunset <text>` - Display text with sunset effect
- `stats` - Show ANSI engine statistics

## EXAMPLES

```
ansi rgb 255 0 0 "Red Text"
ansi gradient "Gradient Text"
ansi neon "Neon Text"
ansi rainbow "Rainbow Text"
```

## SEE ALSO

man(1), anim(1), display(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
