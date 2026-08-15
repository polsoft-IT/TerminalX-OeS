# lan - LAN Commands

## NAME

lan - LAN Commands - Local Area Network management and diagnostics

## DESCRIPTION

The lan command provides comprehensive LAN management capabilities for TerminalX with 15 available commands. Includes network configuration, device discovery, traffic monitoring, and LAN diagnostics.

## SYNOPSIS

```
lan scan
lan discover
lan devices
lan config
lan ip
lan dhcp
lan dns
lan gateway
lan subnet
lan vlan
lan trunk
lan mirror
lan bonding
lan aggregation
lan stats
```

## OPTIONS

- `scan` - Scan LAN for devices and network topology
- `discover` - Discover network devices using ARP and SNMP
- `devices` - List all devices on the LAN
- `config` - LAN configuration management
- `ip` - IP address configuration
- `dhcp` - DHCP server management
- `dns` - DNS server configuration
- `gateway` - Default gateway configuration
- `subnet` - Subnet mask and network configuration
- `vlan` - VLAN management
- `trunk` - Trunk port configuration
- `mirror` - Port mirroring for traffic analysis
- `bonding` - Network bonding configuration
- `aggregation` - Link aggregation setup
- `stats` - LAN traffic statistics

## EXAMPLES

```
lan scan
lan devices
lan config
lan stats
```

## SEE ALSO

man(1), network(1), wifi(1), ethernet(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
