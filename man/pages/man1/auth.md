# auth - Authentication Commands

## NAME

auth - Authentication commands (login, logout, permissions)

## DESCRIPTION

The auth command provides access to TerminalX's authentication and authorization system. Manage user sessions, permissions, and security policies with 8 available commands.

## SYNOPSIS

```
auth login <user>
auth logout
auth permissions list
auth permissions grant <user> <perm>
auth permissions revoke <user> <perm>
auth status
auth users list
auth whoami
```

## OPTIONS

- `login <user>` - Login as a specific user
- `logout` - Logout current user
- `permissions list` - List all permissions
- `permissions grant <user> <perm>` - Grant permission to user
- `permissions revoke <user> <perm>` - Revoke permission from user
- `status` - Show authentication status
- `users list` - List all users
- `whoami` - Show current user

## EXAMPLES

```
auth login admin
auth permissions list
auth permissions grant john network_admin
auth status
auth whoami
```

## SEE ALSO

man(1), shield(1), kernel(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
