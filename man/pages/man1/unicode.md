# unicode - Unicode Commands

## NAME

unicode - Unicode commands (all, page, find, block, info, cat, random, stats)

## DESCRIPTION

The unicode command provides access to TerminalX's Unicode library. Browse, search, and use Unicode characters in your terminal with 18 available commands.

## SYNOPSIS

```
unicode all
unicode page <number>
unicode find <name>
unicode block <block>
unicode info <char>
unicode cat <category>
unicode random
unicode stats
unicode search <query>
unicode blocks list
unicode blocks info <block>
unicode convert <char> <format>
unicode test <char>
unicode validate <text>
```

## OPTIONS

- `all` - Display all available Unicode characters
- `page <number>` - Display Unicode characters on a specific page
- `find <name>` - Find Unicode characters by name
- `block <block>` - Display Unicode block
- `info <char>` - Get information about a Unicode character
- `cat <category>` - Display Unicode by category
- `random` - Display a random Unicode character
- `stats` - Show Unicode library statistics

## EXAMPLES

```
unicode all
unicode block Latin
unicode find heart
unicode random
unicode stats
```

## SEE ALSO

man(1), emoji(1), figlet(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
