# man - TerminalX Manual Page System v2

## NAME

man - display manual pages for TerminalX commands and documentation with enhanced search, statistics, and organization features

## DESCRIPTION

The man command is the TerminalX manual page system v2. It provides comprehensive documentation for all TerminalX commands, modules, and features with advanced search capabilities, relevance scoring, usage statistics, category organization, cross-references, and quick reference summaries. Man pages are organized by section and can be searched, displayed, and exported in various formats.

## SYNOPSIS

```
man show <page_name> [section]
man search <query>
man list [section]
man wildcard <pattern>
man fuzzy <query>
man add <name> <content_file> [section]
man remove <page_name>
man export <page_name> <output_file> [format]
man stats
man refresh
man cache_clear
man cache_stats
man cleanup
man rebuild
man source_stats
man readme
man categories
man category <name>
man usage_stats
man cross_refs <page_name>
man quick_ref <page_name>
```

## OPTIONS

### Basic Commands
- `show <page_name> [section]` - Display a specific man page. Optional section number can be specified.
- `search <query>` - Search for man pages matching the query with relevance scoring.
- `list [section]` - List all available man pages, optionally filtered by section.
- `wildcard <pattern>` - Search for man pages using wildcard patterns.
- `fuzzy <query>` - Fuzzy search for man pages with approximate matching and similarity scores.

### Management Commands
- `add <name> <content_file> [section]` - Add a custom man page from a file.
- `remove <page_name>` - Remove a custom man page.
- `export <page_name> <output_file> [format]` - Export a man page to a file in specified format (md, html, txt).

### Cache Management
- `stats` - Display man engine statistics.
- `refresh` - Refresh man pages from sources.
- `cache_clear` - Clear the man page cache.
- `cache_stats` - Display cache statistics.
- `cleanup` - Clean up expired cache entries.
- `rebuild` - Rebuild the man page cache from all sources.
- `source_stats` - Display statistics about man page sources.

### Enhanced Features (v2)
- `readme` - Display the man module README file.
- `categories` - List all categories and their pages.
- `category <name>` - Get pages in a specific category.
- `usage_stats` - Display usage statistics (most viewed, most searched).
- `cross_refs <page_name>` - Get cross-references for a page.
- `quick_ref <page_name>` - Get quick reference summary for a page.

## EXAMPLES

### Basic Usage
```
man show man
man show man 1
man search network
man wildcard *net*
man fuzzy network
man list
man list 1
```

### Management
```
man add mycommand mycommand.md 1
man remove mycommand
man export man man_output.html html
```

### Cache Management
```
man stats
man cache_clear
man rebuild
man source_stats
```

### Enhanced Features (v2)
```
man readme
man categories
man category godmode
man usage_stats
man cross_refs man
man quick_ref kernel
```

## ENHANCED FEATURES (v2)

### Relevance Scoring
Search results are now scored by relevance:
- Exact name match: 100 points
- Name contains query: 50 points
- Description contains query: 30 points
- Keywords match: 20 points
- Partial name match: 15 points
- Fuzzy match: 10 points

### Usage Statistics
Track page views and search queries:
- Most viewed pages
- Most searched terms
- Search history (last 100 entries)
- Reset statistics option

### Category Organization
Pages organized into logical categories:
- godmode: Advanced systems (kernel, proc, advshield, etc.)
- standard: Standard systems (ai, gui, network, etc.)
- library: Library systems (emoji, unicode, figlet, etc.)
- network: Network tools (wifi, lan, ethernet)
- filesystem: File system commands
- system: System commands
- documentation: Documentation tools

### Cross-References
Automatic cross-references between related pages based on SEE ALSO sections.

### Quick Reference
Concise summaries showing:
- Name and description
- Synopsis (first 5 lines)
- Key options (first 5 options)

## SECTIONS

1. General commands
2. System calls
3. Library functions
4. Special files
5. File formats
6. Games
7. Miscellaneous
8. System administration
9. Kernel

## FILES

- `~/.terminalx/man/cache/` - Cache directory for parsed man pages
- `~/.terminalx/config/man/man.json` - Configuration file for man system

## SEE ALSO

help(1), commands(1), terminal(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
