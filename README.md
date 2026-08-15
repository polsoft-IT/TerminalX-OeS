# TerminalX - Advanced Terminal System

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-success)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Architecture](https://img.shields.io/badge/arch-x86__64%20%7C%20ARM64-orange)

<!-- Images will be added later: pic.png and pic1.png -->
<!-- <div align="center">
  <img src="pic.png" alt="TerminalX Screenshot" width="45%"/>
  <img src="pic1.png" alt="TerminalX Interface" width="45%"/>
</div> -->

## 🚀 Overview

TerminalX is an advanced terminal system with GODMODE capabilities, featuring comprehensive system optimization, AI integration, network tools, security systems, and a powerful plugin architecture. Built for power users, developers, and system administrators who need maximum control over their systems.

### Key Features

- **🔥 GODMODE Systems**: Advanced kernel hooks, process monitoring, advanced shield, module manager, plugin system, and event bus
- **🤖 AI Integration**: AI analyzer, sentiment analysis, and AI sentinel for intelligent system monitoring
- **🌐 Network Tools**: Advanced network scanning, WiFi PRO, LAN management, Ethernet diagnostics, and Bluetooth device management
- **🛡️ Security**: Defender integration, firewall management, sandbox isolation, and threat intelligence
- **⚡ System Optimization v2**: Real Windows API pagefile flush, working set trim, system cache flush
- **🌍 Geolocation Engine v6**: GPS daemon, map engine, fusion positioning, and IP geolocation
- **📊 Event Bus v2**: Advanced event system with async/sync modes, filters, hooks, and diagnostics
- **📊 Report Engine**: Advanced report generation with plugin system and multiple output formats
- **📚 Version Management**: Semantic versioning with build numbers and release tags
- **🎨 Library Systems**: Emoji, Unicode, FIGLET, ANSI colors, animations, and GUI widgets
- **📁 File System**: Comprehensive file operations with bulk operations and monitoring
- **🔍 Metadata**: File metadata scanning, editing, and sidecar management
- **🏗️ Build System**: Parallel builds, dependency management, and build plugins
- **📋 Task Management**: Background tasks with scheduling, priorities, and dependencies
- **📖 Documentation**: 43 comprehensive man pages with search and caching

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [GODMODE Systems](#godmode-systems)
- [Standard Systems](#standard-systems)
- [Library Systems](#library-systems)
- [File System](#file-system)
- [Network Tools](#network-tools)
- [Configuration](#configuration)
- [Plugins](#plugins)
- [Commands Reference](#commands-reference)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Installation

### Requirements

- Python 3.10 or higher
- Windows / Linux / macOS / Android (TerminalOS Runtime)
- x86_64 or ARM64 architecture

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/polsoft-IT/TerminalX.git
cd TerminalX

# Install dependencies
pip install -r requirements.txt

# Run TerminalX
python terminal/main.py
```

### Dependencies

```
psutil>=5.9.0
asyncio>=3.4.3
ctypes>=1.1.0
dataclasses>=0.6
```

## 🚀 Quick Start

```bash
# Start TerminalX
python terminal/main.py

# Show help
help
?

# Show system status
status
info

# GODMODE examples
kernel status
proc scan
advshield status
modman list
plugin list
geo ipinfo 8.8.8.8
geo gps status
geo map render "New York"
geo fusion locate
sysopt clean_python_ram
sysopt flush_pagefile
event status
event emit test '{"key":"value"}'

# Standard examples
ai chat "Hello"
gui create window
net scan localhost
shield status
cloud status

# Network examples
wifi scan
wifi connect "MyNetwork"
lan discover
ethernet status
bluetooth status
bluetooth scan
bluetooth pair 00:11:22:33:44:55

# Report engine
report create "System Report"
report render <id> json
report save <id> report.txt

# Version management
version version
version semver
version info
```

## 🏗️ Architecture

TerminalX is built on a modular architecture with the following components:

### Core Components

- **CoreEngine**: Central engine managing all subsystems
- **NotificationSystem**: Unified notification management
- **Logger**: Advanced logging with multiple levels
- **PluginManager**: Dynamic plugin loading and management
- **ManEngine**: Manual page system with search and caching

### Subsystems

Each module is registered as a subsystem with the CoreEngine, enabling:
- Unified lifecycle management
- Inter-module communication
- Centralized configuration
- Performance monitoring

## 🔥 GODMODE Systems

### Kernel Hooks Engine

Advanced kernel-level system call hooking and monitoring.

```bash
kernel status
kernel hooks list
kernel events monitor
kernel traps add <rule>
```

**Features:**
- Syscall hooking
- Event monitoring
- Trap rules
- Filter chains
- Real-time kernel analysis

### Process Monitor Engine

Comprehensive process monitoring and control.

```bash
proc scan
proc monitor <pid>
proc kill <pid>
proc analyze <pid>
proc history
```

**Features:**
- Real-time process monitoring
- Resource usage analysis
- Process tree visualization
- Automatic process control
- Historical data tracking

### Advanced Shield

Security rules, snapshots, isolation, and heuristics.

```bash
advshield status
advshield rules list
advshield snapshot create
advshield isolate <pid>
advshield heuristics enable
```

**Features:**
- Rule-based security
- System snapshots
- Process isolation
- Heuristic analysis
- Threat detection

### Module Manager

Module loading, snapshots, diagnostics, and dependencies.

```bash
modman list
modman load <module>
modman unload <module>
modman snapshot create
modman diagnostics
modman dependencies
```

**Features:**
- Dynamic module loading
- Module snapshots
- Dependency resolution
- Diagnostics tools
- Version management

### Plugin System

Plugin loading, hooks, events, sandbox, and permissions.

```bash
plugin list
plugin load <plugin>
plugin unload <plugin>
plugin hooks list
plugin sandbox enable
plugin permissions
```

**Features:**
- Dynamic plugin loading
- Event hooks
- Sandbox execution
- Permission system
- Plugin marketplace

### Geolocation Engine v6

Advanced geolocation with GPS daemon, map engine, and fusion positioning.

```bash
geo ipinfo 8.8.8.8
geo reverse 40.7128 -74.0060
geo batch <file>
geo cache stats
geo gps status
geo gps track
geo map render <location>
geo fusion locate
```

**Features:**
- **GPS Daemon**: Real-time GPS tracking with NMEA parsing
- **Map Engine**: OSM and Google Maps rendering with multiple layers
- **Fusion Engine**: GPS/BTS/WiFi positioning for enhanced accuracy
- Multiple providers (IPInfo, GeoPy, FreeGeoIP, IPAPI)
- Reverse geocoding
- Batch processing
- Caching system
- Statistics tracking

### System Optimizer v2

Advanced RAM/CPU optimization with Windows API integration.

```bash
sysopt clean_python_ram
sysopt flush_pagefile
sysopt trim_working_sets
sysopt flush_system_cache
sysopt optimize_cpu
sysopt scan --kill
sysopt daemon start
```

**Features:**
- **Windows API Integration**:
  - Real pagefile flush using NT API
  - Working set trim using Win32 API
  - System cache flush using NT API
- Enhanced Python RAM cleaning
- CPU priority optimization
- Process scanning with auto-kill
- Daemon mode for continuous optimization

### Event Bus v2

Advanced event system with async/sync modes, filters, and hooks.

```bash
event emit <event> <data>
event status
event config show
event config set <key> <value>
event flush
event metadata
event errors
event autofix
event export
event api
```

**Features:**
- **Async/Sync Modes**: Flexible event processing modes
- **Global Filters**: Event filtering by type, source, and content
- **Event Hooks**: Pre/post event processing hooks
- **Comprehensive Logging**: Detailed event logging with multiple levels
- **Diagnostics**: Event bus health monitoring and diagnostics
- **State Management**: Event queue state management
- **Auto-Fix**: Automatic error detection and correction
- **API Interface**: Programmatic access to event bus functionality

## 📊 Standard Systems

### AI Commands

AI chat, analysis, sentiment, and intelligent monitoring.

```bash
ai chat "Hello"
ai analyze <text>
ai sentiment <text>
ai sentinel status
ai plugins list
```

**Features:**
- Natural language processing
- Sentiment analysis
- AI sentinel for monitoring
- Plugin system for AI models
- Context-aware responses

### GUI Commands

Window creation, widgets, and GUI management.

```bash
gui create window
gui add button
gui show
gui hide
```

**Features:**
- Window management
- Widget library
- Event handling
- Layout management
- Theme support

### Network Commands

Network scanning, monitoring, and diagnostics.

```bash
net scan localhost
net monitor
net ping google.com
net traceroute google.com
net speedtest
```

**Features:**
- Network scanning
- Real-time monitoring
- Protocol analysis
- Performance testing
- Security auditing

### Shield Commands

Defender, firewall, sandbox, and threat intelligence.

```bash
shield defender status
shield firewall status
shield sandbox create
shield threat intel
```

**Features:**
- Defender integration
- Firewall management
- Sandbox isolation
- Threat intelligence
- Security policies

### Cloud Commands

Cloud sync, storage, and backup.

```bash
cloud sync
cloud storage list
cloud backup create
cloud status
```

**Features:**
- Multi-cloud support
- Synchronization
- Storage management
- Backup automation
- Status monitoring

### Metadata Commands

File metadata scanning, editing, and sidecar management.

```bash
metadata scan <path>
metadata edit <file> <key> <value>
metadata sidecar create <file>
metadata extract <file>
```

**Features:**
- Metadata extraction
- Sidecar file management
- Batch operations
- Tag management
- History tracking

### Build Commands

Parallel builds, dependency management, and build plugins.

```bash
build start <project>
build parallel <projects>
build deps install
build plugins list
build status
```

**Features:**
- Parallel builds
- Dependency management
- Build plugins
- Optimization
- Deployment automation

### Task Commands

Background tasks with scheduling and priorities.

```bash
task add <command>
task run <id>
task list
task priority <id> <level>
task schedule <time> <command>
```

**Features:**
- Task scheduling
- Priority management
- Dependencies
- History tracking
- Log management

### Version Commands

Semantic versioning with build numbers and tags.

```bash
version version
version semver
version short
version info
version json
version set-build 1024
version set-tag beta
```

**Features:**
- Semantic versioning
- Build number management
- Release tags
- Multiple output formats
- Runtime modification

### Report Commands

Advanced report generation with plugin system.

```bash
report create <title>
report template <template> <data>
report render <id> <format>
report save <id> <file>
report display <id>
report plugins
report formats
```

**Features:**
- Template-based reports
- Multiple output formats (txt, md, json)
- Plugin system (templates, output, filters, post-processing)
- ANSI color display
- File export

## 🎨 Library Systems

### Emoji Library

```bash
emoji all
emoji cat
emoji find <query>
emoji page <n>
emoji random
emoji stats
```

### Unicode Library

```bash
unicode all
unicode page <n>
unicode find <query>
unicode block <name>
unicode info <char>
```

### FIGLET Engine

```bash
figlet render <text>
figlet fonts
figlet load <font>
figlet stats
```

### ANSI Colors

```bash
ansi rgb <r> <g> <b>
ansi gradient
ansi neon
ansi rainbow
ansi fire
ansi matrix
```

### Animations

```bash
anim matrix
anim fire
anim wave
anim spin
anim pulse
anim list
```

### GUI Widgets

```bash
widgets list
widgets stats
```

## 📁 File System

Comprehensive file operations:

```bash
fs ls
fs ls -a
fs ls -l
fs tree
fs cd <dir>
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
fs replace <pattern> <replacement>
fs du <path>
fs df
fs chmod <file> <mode>
fs chown <file> <user>
fs compress <file>
fs extract <archive>
fs hash <file>
fs compare <file1> <file2>
fs monitor <path>
fs watch <path>
```

## 🌐 Network Tools

### WiFi PRO Commands

```bash
wifi on
wifi off
wifi scan
wifi connect <ssid>
wifi info
wifi rssi
wifi snr
wifi speed
wifi quality
wifi channel
wifi firewall
wifi profiles
wifi mac
wifi monitor
wifi dhcp
wifi dns
wifi speedtest
wifi doctor
wifi adapter
wifi hotspot
wifi security
```

### LAN Commands

```bash
lan scan
lan discover
lan devices
lan config
lan ip
lan dhcp
lan dns
lan gateway
lan vlan
lan bonding
lan stats
```

### Ethernet Commands

```bash
ethernet status
ethernet config
ethernet speed
ethernet duplex
ethernet mtu
ethernet mac
ethernet cable test
ethernet statistics
ethernet diagnostics
```

### Bluetooth Commands

```bash
bluetooth status
bluetooth power_on
bluetooth power_off
bluetooth discoverable <on|off>
bluetooth scan [duration]
bluetooth pair <address> [pin]
bluetooth unpair <address>
bluetooth connect <address>
bluetooth disconnect <address>
bluetooth paired
bluetooth connected
bluetooth results
bluetooth sort_rssi
bluetooth filter_paired <true|false>
```

**Features:**
- Device scanning and discovery
- Pairing and connection management
- Signal strength analysis
- Device filtering
- Power control
- Discoverable mode management

### Network Commands

```bash
net ping <host>
net traceroute <host>
net trace <host>
net nslookup <domain>
net dig <domain>
net whois <domain>
net curl <url>
net wget <url>
net http <method> <url>
net tcping <host>
net speedtest
net netinfo
net ipconfig
net ifconfig
net netstat
net route
net arp
net scan <target>
net portscan <target>
net ssh <host>
net scp <src> <dst>
net ftp <host>
net sftp <host>
net telnet <host>
net mqtt <topic>
net websocket <url>
net proxy <url>
net vpn connect
net vpn status
net dns flush
net dns set
net hosts edit
net geoip <ip>
net publicip
net cloud ping
net cloud status
```

## ⚙️ Configuration

TerminalX uses a hierarchical configuration system:

### Main Configuration

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
  },
  "sysopt": {
    "ram_threshold_mb": 500,
    "cpu_threshold_percent": 80,
    "scan_interval": 3.0,
    "enable_pagefile_flush": true,
    "enable_workingset_trim": true,
    "enable_system_cache_flush": true
  },
  "event": {
    "enabled": true,
    "mode": "async",
    "log_level": "INFO",
    "max_queue_size": 1000,
    "auto_flush": true
  },
  "geo": {
    "enabled": true,
    "default_provider": "freegeoip",
    "timeout": 10,
    "max_retries": 3,
    "enable_fallback": true
  },
  "report": {
    "enabled": true,
    "plugin_paths": [],
    "default_format": "txt"
  }
}
```

### Configuration Files

- `~/.terminalx/config/config.json` - Main configuration
- `~/.terminalx/config/version/version.json` - Version configuration
- `~/.terminalx/config/sysopt/sysopt.json` - System optimizer configuration
- `~/.terminalx/config/event/event.json` - Event bus configuration
- `~/.terminalx/config/geo/geo.json` - Geolocation engine configuration
- `~/.terminalx/config/report/report.json` - Report engine configuration

## 🔌 Plugins

TerminalX features a powerful plugin system with:

### Plugin Types

- **Template Plugins**: Generate reports from templates
- **Output Plugins**: Render reports to different formats
- **Filter Plugins**: Modify report content
- **Post-Process Plugins**: Actions after report generation

### Plugin Management

```bash
plugin list
plugin load <plugin>
plugin unload <plugin>
plugin hooks list
plugin sandbox enable
plugin permissions
```

### Built-in Plugins

- **LoggerPlugin**: Logging integration
- **CachePlugin**: Performance caching
- **StatsPlugin**: Statistics tracking
- **SimpleTemplate**: Basic template engine
- **BasicTextOutput**: TXT/MD output
- **JsonOutput**: JSON output
- **UppercaseFilter**: Content filtering
- **LoggingPostprocess**: Post-processing logging

## 📖 Commands Reference

### Basic Commands

```
help [group]          - Show help for specific group
?                     - Alias for help
status                - Show system status
info                  - Show system information
clear                 - Clear screen
echo <text>           - Echo text
date                  - Show current date and time
version               - Show version information
history               - Show command history
uptime                - Show system uptime
env [var]             - Show environment variables
set <var> <val>       - Set environment variable
whoami                - Show current user
pwd                   - Print working directory
notify <title> <msg>  - Create notification
notifications         - Show notifications
exit                  - Exit terminal
```

### Man Pages

```
man show <page>       - Display man page
man search <query>    - Search man pages
man list [section]    - List man pages
man wildcard <pattern> - Wildcard search
man fuzzy <query>     - Fuzzy search
man add <name> <file> - Add custom man page
man remove <page>     - Remove man page
man export <page> <file> - Export man page
man stats             - Show statistics
man refresh           - Refresh from sources
man cache_clear       - Clear cache
man cache_stats       - Cache statistics
man cleanup           - Clean expired entries
man rebuild           - Rebuild cache
man source_stats      - Source statistics
```

## 🔧 API Reference

### Core Engine API

```python
from core import CoreEngine

# Initialize core engine
core = CoreEngine()
await core.initialize()

# Register subsystem
await core.register_subsystem('name', subsystem)

# Get subsystem
subsystem = core.get_subsystem('name')
```

### Module API

```python
from system_optimizer import SystemOptimizer, SystemOptConfig

# Create optimizer
config = SystemOptConfig(
    ram_threshold_mb=500,
    cpu_threshold_percent=80,
    scan_interval=3.0
)
optimizer = SystemOptimizer(config)

# Use optimizer
result = optimizer.clean_python_ram()
result = optimizer.flush_pagefile()
result = optimizer.trim_working_sets()
```

### Report Engine API

```python
from report import ReportEngine, create_default_engine

# Create report engine
engine = create_default_engine()
await engine.initialize()

# Create report
report = engine.create_report("My Report")
report.add_section("Section 1", "Content")

# Render report
output = engine.render(report, "json")
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Use meaningful commit messages
- Ensure all tests pass

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Sebastian Januchowski**
- polsoft.ITS™ Dev
- Email: polsoft.its@mail.com
- GitHub: polsoft-IT

## 🙏 Acknowledgments

- TerminalOS Runtime Team
- polsoft.ITS™ Development Team
- Open Source Community
- All contributors

## 📞 Support

For support, please:
- Open an issue on GitHub
- Email: polsoft.its@mail.com
- Check the man pages: `man show <command>`

## 🔗 Links

- [Documentation](https://github.com/polsoft-IT/TerminalX/wiki)
- [Issue Tracker](https://github.com/polsoft-IT/TerminalX/issues)
- [Releases](https://github.com/polsoft-IT/TerminalX/releases)

---

<div align="center">
  <b>Made with ❤️ by polsoft.ITS™ Dev</b>
</div>
