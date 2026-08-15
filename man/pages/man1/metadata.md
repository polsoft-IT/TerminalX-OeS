# metadata - Metadata Commands

## NAME

metadata [meta] - Metadata commands (scan, edit, sidecars)

## DESCRIPTION

The metadata command provides access to TerminalX's metadata management system. Scan, edit, and manage file metadata and sidecar files with 22 available commands.

## SYNOPSIS

```
metadata scan <path>
metadata edit <file> <key> <value>
metadata sidecar create <file>
metadata sidecar read <file>
metadata sidecar update <file>
metadata sidecar delete <file>
metadata extract <file>
metadata apply <file> <metadata>
metadata validate <file>
metadata compare <file1> <file2>
metadata export <file> <format>
metadata import <file> <format>
metadata tags add <file> <tag>
metadata tags remove <file> <tag>
metadata tags list <file>
metadata history <file>
metadata backup <file>
metadata restore <file>
```

## OPTIONS

- `scan <path>` - Scan files for metadata
- `edit <file> <key> <value>` - Edit file metadata
- `sidecar create <file>` - Create sidecar file
- `sidecar read <file>` - Read sidecar file
- `sidecar update <file>` - Update sidecar file
- `extract <file>` - Extract metadata from file
- `apply <file> <metadata>` - Apply metadata to file

## EXAMPLES

```
metadata scan /home/user/documents
metadata edit photo.jpg author "John Doe"
metadata sidecar create document.pdf
metadata extract image.png
```

## SEE ALSO

man(1), build(1), fs(1), report(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
