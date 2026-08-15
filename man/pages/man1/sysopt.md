# sysopt - System Optimizer v2 [GODMODE]

## NAME

sysopt - System Optimizer v2 [GODMODE] - Advanced RAM cleaning, CPU optimization, Windows API pagefile flush, working set trim

## DESCRIPTION

The sysopt command provides access to TerminalX's advanced system optimization capabilities. This GODMODE system v2 offers enhanced RAM cleaning, CPU optimization, process scanning, and system performance tuning with real Windows API integration for pagefile flush, working set trim, and system cache flush.

## SYNOPSIS

```
sysopt clean_ram
sysopt clean_python_ram
sysopt flush_pagefile
sysopt trim_working_sets
sysopt flush_system_cache
sysopt clean_pagefile
sysopt optimize_cpu
sysopt scan [--kill|-k]
sysopt info
sysopt stats
sysopt config [key=value]
sysopt daemon [start|stop|status]
sysopt plugins
sysopt reset_stats
```

## OPTIONS

### RAM Optimization (v2 Enhanced)
- `clean_ram` - Legacy RAM cleaning method
- `clean_python_ram` - Enhanced Python RAM cleaner with detailed reporting (v2)

### Windows API Features (v2 - Windows only)
- `flush_pagefile` - Real pagefile flush using NT API (v2)
- `trim_working_sets` - Working set trim using Win32 API (v2)
- `flush_system_cache` - System cache flush using NT API (v2)

### Legacy Methods
- `clean_pagefile` - Legacy pagefile cleaning (Windows only)

### CPU & Process Management
- `optimize_cpu` - Optimize CPU by adjusting process priorities
- `scan [--kill|-k]` - Scan for resource-intensive processes (optional auto-kill)
- `info` - Get current system resource information

### Configuration & Management
- `stats` - Get optimizer statistics
- `config [key=value]` - Show or update configuration
- `daemon [start|stop|status]` - Control optimization daemon
- `plugins` - List installed plugins
- `reset_stats` - Reset optimizer statistics

## CONFIGURATION OPTIONS

- `ram_threshold_mb` - RAM threshold in MB for process scanning (default: 500)
- `cpu_threshold_percent` - CPU threshold percentage (default: 80)
- `scan_interval` - Daemon scan interval in seconds (default: 3.0)
- `enable_pagefile_clean` - Enable legacy pagefile cleaning (default: False)
- `enable_pagefile_flush` - Enable real pagefile flush using NT API (default: True) - v2
- `enable_workingset_trim` - Enable working set trim using Win32 API (default: True) - v2
- `enable_system_cache_flush` - Enable system cache flush using NT API (default: True) - v2
- `enable_priority_opt` - Enable CPU priority optimization (default: True)
- `enable_auto_kill` - Enable automatic process killing (default: False)
- `enable_cache_flush` - Enable Python cache flushing (default: True)
- `daemon_enabled` - Enable daemon mode (default: False)

## EXAMPLES

```
sysopt clean_python_ram
sysopt flush_pagefile
sysopt trim_working_sets
sysopt flush_system_cache
sysopt optimize_cpu
sysopt scan
sysopt scan --kill
sysopt info
sysopt stats
sysopt config enable_pagefile_flush=true
sysopt daemon start
sysopt daemon status
sysopt daemon stop
```

## WINDOWS API FEATURES (v2)

The v2 SystemOptimizer includes real Windows API integration for advanced memory management:

- **Pagefile Flush**: Uses NT API `NtSetSystemInformation` with `SystemMemoryListInformation` (0x50) to flush modified pages
- **Working Set Trim**: Uses Win32 API `EmptyWorkingSet` and `SetProcessWorkingSetSize` to trim working sets for all processes
- **System Cache Flush**: Uses NT API to flush the system standby list

These features require Windows and appropriate privileges. They are automatically disabled on non-Windows platforms.

## SEE ALSO

man(1), sys(1), proc(1), version(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
