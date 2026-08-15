# network - TerminalX Network Commands

## NAME

network [nets] - network commands (scan, monitor, connect, etc.)

## DESCRIPTION

The network command provides comprehensive network tools for TerminalX including network scanning, monitoring, connection management, and diagnostic tools. Supports both IPv4 and IPv6 protocols with 47 available commands.

## SYNOPSIS

```
network ping <host>
network traceroute <host>
network trace <host>
network nslookup <domain>
network dig <domain>
network whois <domain>
network curl <url>
network wget <url>
network http <method> <url>
network tcping <host>
network speedtest
network netinfo
network ipconfig
network ifconfig
network netstat
network route
network arp
network scan <target>
network portscan <target>
network wifi scan
network wifi connect <ssid>
network wifi info
network wlan
network lan
network ethernet
network ssh <host>
network scp <src> <dst>
network ftp <host>
network sftp <host>
network telnet <host>
network mqtt <command>
network websocket <url>
network proxy <command>
network vpn connect <server>
network vpn status
network dns <command>
network dns flush
network dns set <server>
network hosts edit
network geoip <ip>
network publicip
network cloud ping
network cloud status
```

## OPTIONS

- `ping <host>` - Send ICMP echo requests to a host
- `traceroute <host>` - Trace route to target host
- `trace <host>` - Trace network path
- `nslookup <domain>` - DNS lookup for domain
- `dig <domain>` - Advanced DNS lookup
- `whois <domain>` - WHOIS domain information
- `curl <url>` - HTTP request with curl
- `wget <url>` - Download file with wget
- `http <method> <url>` - HTTP request method
- `tcping <host>` - TCP ping to host
- `speedtest` - Network speed test
- `netinfo` - Network information
- `ipconfig` - IP configuration
- `ifconfig` - Interface configuration
- `netstat` - Network statistics
- `route` - Routing table
- `arp` - ARP table
- `scan <target>` - Network scan for open ports and services
- `portscan <target>` - Port scanning
- `wifi scan` - Scan WiFi networks
- `wifi connect <ssid>` - Connect to WiFi network
- `wifi info` - WiFi information
- `wlan` - Wireless LAN commands
- `lan` - Local area network commands
- `ethernet` - Ethernet commands
- `ssh <host>` - SSH connection
- `scp <src> <dst>` - Secure copy
- `ftp <host>` - FTP connection
- `sftp <host>` - SFTP connection
- `telnet <host>` - Telnet connection
- `mqtt <command>` - MQTT commands
- `websocket <url>` - WebSocket connection
- `proxy <command>` - Proxy commands
- `vpn connect <server>` - Connect to VPN
- `vpn status` - VPN status
- `dns <command>` - DNS commands
- `dns flush` - Flush DNS cache
- `dns set <server>` - Set DNS server
- `hosts edit` - Edit hosts file
- `geoip <ip>` - Geolocation lookup
- `publicip` - Get public IP address
- `cloud ping` - Cloud ping
- `cloud status` - Cloud status

## EXAMPLES

```
network ping google.com
network scan 192.168.1.0/24
network traceroute example.com
network info
network connect ssh user@host
```

## SEE ALSO

man(1), wifi(1), lan(1), ethernet(1), ssh(1), ftp(1), vpn(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
