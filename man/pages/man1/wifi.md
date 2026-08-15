# wifi - WiFi Commands (PRO)

## NAME

wifi - WiFi Commands (PRO) - comprehensive technical descriptions for WiFi network management

## DESCRIPTION

The wifi command provides comprehensive WiFi management capabilities for TerminalX with 52 available professional commands. Includes advanced network analysis, security features, connection management, and diagnostic tools.

## SYNOPSIS

```
wifi on
wifi off
wifi scan
wifi scan full
wifi scan hidden
wifi connect <ssid> <password>
wifi connect enterprise <ssid>
wifi disconnect
wifi info
wifi rssi
wifi snr
wifi speed
wifi quality
wifi channel
wifi channels
wifi band
wifi width
wifi firewall
wifi block <ssid>
wifi allow <ssid>
wifi profiles
wifi profile add
wifi profile remove
wifi profile export
wifi profile import
wifi mac
wifi mac random
wifi mac reset
wifi monitor
wifi sniff
wifi deauth detect
wifi evil twin detect
wifi spoof detect
wifi spectrum
wifi analyzer
wifi dhcp
wifi dhcp renew
wifi dhcp release
wifi dns
wifi dns set <address>
wifi dns flush
wifi route
wifi arp
wifi publicip
wifi geoip
wifi speedtest
wifi doctor
wifi reset
wifi adapter
wifi adapter power <level>
wifi adapter capabilities
wifi multi
wifi route <ssid> <adapter>
wifi hotspot on
wifi hotspot off
wifi hotspot status
wifi fingerprint <bssid>
wifi security
wifi mitm detect
wifi log
wifi log clear
```

## OPTIONS

- `on` - Turn on WiFi adapter; activates radio and WLAN stack
- `off` - Turn off adapter; stops all connections and scanning
- `scan` - Scan available networks; detects SSID, RSSI, encryption
- `scan full` - Full scan: channels, RSSI, SNR, BSSID, bandwidth
- `scan hidden` - Detect hidden SSID (if possible)
- `connect <ssid> <password>` - Connect to network; supports WPA2/WPA3
- `connect enterprise <ssid>` - Enterprise connection EAP/PEAP/TTLS; certificates
- `disconnect` - Disconnect current connection
- `info` - Full connection info: SSID, BSSID, RSSI, SNR, channel, speed
- `rssi` - Signal strength; range diagnostics
- `snr` - Signal-to-noise ratio; critical for stability
- `speed` - PHY link speed (e.g., 866 Mb/s)
- `quality` - Connection quality (RSSI + SNR + stability)
- `channel` - Current channel
- `channels` - List channels and their load; interference analysis
- `band` - Band (2.4/5/6 GHz)
- `width` - Channel width (20/40/80/160 MHz)
- `firewall` - WiFi firewall status; blocks dangerous networks
- `block <ssid>` - Block network; prevents connection
- `allow <ssid>` - Remove block
- `profiles` - List saved profiles
- `profile add` - Add profile
- `profile remove` - Remove profile
- `profile export` - Export profile
- `profile import` - Import profile
- `mac` - Adapter MAC address
- `mac random` - Random MAC (privacy mode)
- `mac reset` - Restore real MAC
- `monitor` - Monitor WiFi traffic; packets, speed, loss
- `sniff` - Frame sniffing (monitor mode, if system allows)
- `deauth detect` - Detect deauth attacks
- `evil twin detect` - Detect fake access points
- `spoof detect` - Detect BSSID spoofing
- `spectrum` - Pseudo-spectrum analysis; channel load
- `analyzer` - Full signal analyzer: RSSI, SNR, interference
- `dhcp` - DHCP information
- `dhcp renew` - Renew DHCP
- `dhcp release` - Release DHCP
- `dns` - Current DNS
- `dns set <address>` - Set DNS
- `dns flush` - Flush DNS cache
- `route` - Routing table
- `arp` - ARP table
- `publicip` - Get public IP
- `geoip` - IP geolocation
- `speedtest` - Internet speed test
- `doctor` - WiFi diagnostics; detects signal, driver, DHCP, DNS issues
- `reset` - Reset WiFi stack; fixes connection errors
- `adapter` - Adapter info: standard (Wi-Fi 4/5/6/7), chipset, manufacturer
- `adapter power <level>` - Change transmitter power (if system allows)
- `adapter capabilities` - Full adapter capabilities
- `multi` - Multi-WiFi card support
- `route <ssid> <adapter>` - Assign network to specific card
- `hotspot on` - Start hotspot
- `hotspot off` - Stop hotspot
- `hotspot status` - Hotspot status
- `fingerprint <bssid>` - Router fingerprinting: manufacturer, model, capabilities
- `security` - Network security status
- `mitm detect` - Detect man-in-the-middle attacks
- `log` - WiFi logs
- `log clear` - Clear logs

## EXAMPLES

```
wifi on
wifi scan
wifi connect "MyNetwork" "password123"
wifi info
wifi channel
wifi doctor
wifi hotspot on
```

## SEE ALSO

man(1), network(1), lan(1), ethernet(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
