# bluetooth - Bluetooth Manager v1 [GODMODE]

## NAME

bluetooth [bt] - Bluetooth Manager v1 [GODMODE] - Bluetooth device management and scanning

## DESCRIPTION

The bluetooth command provides access to TerminalX's Bluetooth management system. This GODMODE system offers device pairing, connection management, device scanning, and comprehensive Bluetooth operations for wireless device control.

## SYNOPSIS

```
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

## OPTIONS

### Power Management
- `power_on` - Power on Bluetooth adapter
- `power_off` - Power off Bluetooth adapter
- `status` - Get current Bluetooth status

### Discovery Mode
- `discoverable <on|off>` - Set discoverable mode for other devices

### Device Scanning
- `scan [duration]` - Scan for Bluetooth devices (default: 10 seconds)
- `results` - Get last scan results
- `sort_rssi` - Sort scan results by signal strength (RSSI)
- `filter_paired <true|false>` - Filter scan results by paired status

### Device Pairing
- `pair <address> [pin]` - Pair with a Bluetooth device
- `unpair <address>` - Unpair a Bluetooth device
- `paired` - List all paired devices

### Device Connection
- `connect <address>` - Connect to a paired device
- `disconnect <address>` - Disconnect from a device
- `connected` - List all connected devices

## EXAMPLES

### Power Management
```
bluetooth power_on
bluetooth status
bluetooth power_off
```

### Device Discovery
```
bluetooth discoverable on
bluetooth scan 15
bluetooth results
bluetooth sort_rssi
```

### Device Pairing
```
bluetooth scan
bluetooth pair 00:11:22:33:44:55 1234
bluetooth paired
```

### Device Connection
```
bluetooth connect 00:11:22:33:44:55
bluetooth connected
bluetooth disconnect 00:11:22:33:44:55
```

### Filtering
```
bluetooth scan
bluetooth filter_paired true
bluetooth filter_paired false
```

## BLUETOOTH MANAGER

The BluetoothManager provides core device management functionality:

### Power Control
- **power_on()**: Enable Bluetooth adapter
- **power_off()**: Disable Bluetooth adapter
- **set_discoverable(bool)**: Set device discoverable mode

### Device Management
- **pair(address, pin)**: Pair with device using optional PIN
- **unpair(address)**: Remove device pairing
- **connect(address)**: Connect to paired device
- **disconnect(address)**: Disconnect from device

### Device Information
- **get_paired_devices()**: List all paired devices
- **get_connected_devices()**: List all connected devices
- **get_status()**: Get current Bluetooth status

## BLUETOOTH SCANNER

The BluetoothScanner provides device discovery functionality:

### Scanning
- **scan(duration)**: Scan for devices with specified duration
- **get_results()**: Get last scan results

### Results Processing
- **sort_by_rssi()**: Sort results by signal strength
- **filter_by_paired(bool)**: Filter by paired status

### Device Information
Each scanned device includes:
- **address**: MAC address (e.g., 00:11:22:33:44:55)
- **name**: Device name
- **rssi**: Signal strength (negative dBm)
- **class**: Device class (Audio, Peripheral, etc.)
- **paired**: Pairing status

## DEVICE CLASSES

Common Bluetooth device classes:
- **Audio**: Headphones, speakers, microphones
- **Peripheral**: Mouse, keyboard, gamepad
- **Phone**: Mobile phones, smartphones
- **Computer**: Laptops, desktops
- **Network**: Access points, routers
- **Imaging**: Cameras, scanners
- **Wearable**: Smartwatches, fitness trackers

## COMPATIBILITY

The Bluetooth system supports:
- ✅ Windows (via Windows Bluetooth API)
- ✅ Linux (via BlueZ)
- ✅ macOS (via IOBluetooth)
- ✅ Android (via BluetoothAdapter)

## REQUIREMENTS

- Bluetooth hardware support
- Appropriate Bluetooth drivers
- Root/admin privileges for some operations
- Python 3.10+

## TROUBLESHOOTING

### Bluetooth not powering on
- Check if Bluetooth hardware is available
- Verify Bluetooth drivers are installed
- Ensure Bluetooth service is running

### Scan returns no devices
- Ensure Bluetooth is powered on
- Set discoverable mode if needed
- Increase scan duration
- Check for interference

### Pairing fails
- Verify device is in pairing mode
- Check PIN is correct
- Ensure device is within range
- Try removing and re-adding device

## SEE ALSO

man(1), wifi(1), lan(1), network(1)

## AUTHOR

Sebastian Januchowski - polsoft.ITS™ Dev
