# ethernet - Ethernet Commands

## NAME

ethernet [enet] - Ethernet Commands - Wired network management and diagnostics

## DESCRIPTION

The ethernet command provides comprehensive Ethernet management capabilities for TerminalX with 18 available commands. Includes cable testing, interface configuration, link layer diagnostics, and performance monitoring.

## SYNOPSIS

```
ethernet status
ethernet config
ethernet speed
ethernet duplex
ethernet mtu
ethernet mac
ethernet phy
ethernet cable test
ethernet link local
ethernet link remote
ethernet flow control
ethernet storm control
ethernet jumbo frames
ethernet offload
ethernet statistics
ethernet reset
ethernet loopback
ethernet vendor
ethernet diagnostics
```

## OPTIONS

- `status` - Ethernet interface status
- `config` - Ethernet configuration
- `speed` - Link speed configuration
- `duplex` - Duplex mode configuration
- `mtu` - Maximum Transmission Unit
- `mac` - MAC address management
- `phy` - PHY layer information
- `cable test` - Cable diagnostics
- `link local` - Local link status
- `link remote` - Remote link status
- `flow control` - Flow control configuration
- `storm control` - Storm control settings
- `jumbo frames` - Jumbo frame support
- `offload` - Hardware offload features
- `statistics` - Ethernet statistics
- `reset` - Reset Ethernet interface
- `loopback` - Loopback testing
- `vendor` - Vendor information
- `diagnostics` - Full diagnostics

## EXAMPLES

```
ethernet status
ethernet config
ethernet cable test
ethernet statistics
```

## SEE ALSO

man(1), network(1), wifi(1), lan(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
