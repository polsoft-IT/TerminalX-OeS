# fs - File System Commands

## NAME

fs - File system commands (ls, ls -a, ls -l, tree, cd, pwd, touch, open, stat, cp, mv, rm, mkdir, rmdir, rename, find, search, replace, du, df, chmod, chown, compress, extract, hash, compare, monitor, watch, bulk operations, path operations, resolve, filetype, mimetype, checksum, lock, unlock, temp, trash, restore)

## DESCRIPTION

The fs command provides comprehensive file system operations for TerminalX. Navigate, manipulate, monitor, and manage files and directories with advanced features including 43 available commands.

## SYNOPSIS

```
fs ls [path]
fs ls -a [path]
fs ls -l [path]
fs tree [path]
fs cd <path>
fs pwd
fs touch <file>
fs open <file>
fs stat <file>
fs cp <src> <dst>
fs mv <src> <dst>
fs rm <file>
fs mkdir <dir>
fs rmdir <dir>
fs rename <old> <new>
fs find <pattern>
fs search <query>
fs replace <old> <new>
fs du [path]
fs df
fs chmod <mode> <file>
fs chown <user> <file>
fs compress <file>
fs extract <archive>
fs hash <file>
fs compare <file1> <file2>
fs monitor <path>
fs watch <file>
fs bulk <operation>
fs path <operation>
fs resolve <path>
fs filetype <file>
fs mimetype <file>
fs checksum <file>
fs lock <file>
fs unlock <file>
fs temp create
fs trash <file>
fs restore <file>
```

## OPTIONS

- `ls [path]` - List directory contents
- `ls -a [path]` - List all files including hidden
- `ls -l [path]` - List with detailed information
- `tree [path]` - Display directory tree
- `cd <path>` - Change directory
- `pwd` - Print working directory
- `touch <file>` - Create empty file
- `open <file>` - Open file
- `stat <file>` - File statistics
- `cp <src> <dst>` - Copy file
- `mv <src> <dst>` - Move/rename file
- `rm <file>` - Remove file
- `mkdir <dir>` - Create directory
- `rmdir <dir>` - Remove directory
- `rename <old> <new>` - Rename file
- `find <pattern>` - Find files by pattern
- `search <query>` - Search file contents
- `replace <old> <new>` - Replace text in files
- `du [path]` - Disk usage
- `df` - Disk free space
- `chmod <mode> <file>` - Change file permissions
- `chown <user> <file>` - Change file owner
- `compress <file>` - Compress file
- `extract <archive>` - Extract archive
- `hash <file>` - Calculate file hash
- `compare <file1> <file2>` - Compare files
- `monitor <path>` - Monitor directory changes
- `watch <file>` - Watch file for changes
- `resolve <path>` - Resolve path
- `filetype <file>` - Detect file type
- `mimetype <file>` - Detect MIME type
- `checksum <file>` - Calculate checksum
- `lock <file>` - Lock file
- `unlock <file>` - Unlock file
- `temp create` - Create temporary file
- `trash <file>` - Move to trash
- `restore <file>` - Restore from trash

## EXAMPLES

```
fs ls
fs tree /home/user
fs cp file.txt backup.txt
fs find *.py
fs search "function"
fs monitor /home/user/documents
```

## SEE ALSO

man(1), sys(1), archive(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
