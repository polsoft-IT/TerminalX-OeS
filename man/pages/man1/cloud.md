# cloud - Cloud Commands

## NAME

cloud - Cloud commands (sync, storage, backup)

## DESCRIPTION

The cloud command provides access to TerminalX's cloud integration capabilities. Sync files, manage cloud storage, and perform backup operations with 24 available commands.

## SYNOPSIS

```
cloud sync <path>
cloud storage list
cloud storage upload <file>
cloud storage download <file>
cloud storage delete <file>
cloud storage info <file>
cloud backup create <path>
cloud backup restore <id>
cloud backup list
cloud backup delete <id>
cloud backup schedule <path> <schedule>
cloud status
cloud providers list
cloud providers set <provider>
cloud quota
cloud share <file> <user>
cloud collab enable <file>
cloud collab disable <file>
cloud logs
cloud security audit
```

## OPTIONS

- `sync <path>` - Sync local path with cloud
- `storage list` - List cloud storage contents
- `storage upload <file>` - Upload file to cloud
- `storage download <file>` - Download file from cloud
- `backup create <path>` - Create cloud backup
- `backup restore <id>` - Restore from cloud backup
- `backup list` - List available backups
- `status` - Show cloud connection status

## EXAMPLES

```
cloud sync /home/user/documents
cloud storage upload important_file.txt
cloud backup create /home/user
cloud status
```

## SEE ALSO

man(1), storage(1), sync(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
