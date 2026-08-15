# version - TerminalX Version Management System

## NAME

version [ver] - display and manage TerminalX version information

## DESCRIPTION

The version command is the TerminalX version management system. It provides comprehensive version information including semantic versioning, build numbers, release tags, and system metadata. The module supports multiple output formats and allows runtime version modification for development and testing purposes.

## SYNOPSIS

```
version version
version semver
version short
version info
version json
version json-compact
version all
version set-build <build_number>
version set-tag <tag>
version commands
version enable
version disable
```

## OPTIONS

- `version` - Display full version (semver + build + tag).
- `semver` - Display semantic version (major.minor.patch).
- `short` - Display short version form (name + semver + tag).
- `info` - Display human-readable, color-coded version information.
- `json` - Display version information in JSON format (pretty-printed).
- `json-compact` - Display version information in JSON format (compact).
- `all` - Display all version information (human + JSON).
- `set-build <build_number>` - Set the build number to specified value.
- `set-tag <tag>` - Set the version tag (e.g., alpha, beta, rc, stable).
- `commands` - Display list of available version commands.
- `enable` - Enable the version module.
- `disable` - Disable the version module.

## EXAMPLES

```
version version
version semver
version short
version info
version json
version set-build 1024
version set-tag beta
version all
```

## VERSION INFORMATION

The version system uses semantic versioning (SemVer) with the following format:

```
major.minor.patch+build.number-tag
```

- **major**: Major version number (incompatible API changes)
- **minor**: Minor version number (backwards-compatible functionality)
- **patch**: Patch version number (backwards-compatible bug fixes)
- **build**: Build number (incremental build identifier)
- **tag**: Release tag (stable, beta, alpha, rc, etc.)

## DEFAULT VALUES

- **name**: TerminalX
- **major**: 1
- **minor**: 0
- **patch**: 9
- **build**: 100
- **tag**: stable
- **api_level**: 1
- **engine_core**: hybrid-core
- **plugins_api**: v1

## OUTPUT FORMATS

### Human Format
Color-coded, human-readable output with all version details.

### JSON Format
Machine-readable JSON output for programmatic access.

### Short Format
Compact version string for quick reference.

## CONFIGURATION

The version module can be configured via the main TerminalX configuration file:

```json
{
  "version": {
    "enabled": true,
    "name": "TerminalX",
    "major": 1,
    "minor": 0,
    "patch": 9,
    "build": 100,
    "tag": "stable"
  }
}
```

## FILES

- `~/.terminalx/config/version/version.json` - Version configuration file
- `modules/version.py` - Version module implementation
- `commands/version.py` - Version command handlers

## SEE ALSO

help(1), commands(1), terminal(1), build(1), report(1), sysopt(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
