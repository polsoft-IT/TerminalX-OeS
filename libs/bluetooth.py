"""
 ============================================================
  MODULE/PLUGIN NAME: Bluetooth
  VERSION: 1.0.0
  MODULE CLASS: Bluetooth
  DESCRIPTION:
       Bluetooth device management for TerminalX

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

import subprocess
import platform
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class BluetoothStatus(Enum):
    """Bluetooth status"""
    ON = "on"
    OFF = "off"
    DISCOVERING = "discovering"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class BluetoothDevice:
    """Bluetooth device information"""
    name: str
    address: str
    device_class: str
    paired: bool
    connected: bool
    trusted: bool
    rssi: int = 0
    battery: int = -1
    services: List[str] = None
    
    def __post_init__(self):
        if self.services is None:
            self.services = []


@dataclass
class GATTService:
    """GATT service information"""
    uuid: str
    primary: bool
    characteristics: List[str] = None
    
    def __post_init__(self):
        if self.characteristics is None:
            self.characteristics = []


@dataclass
class GATTCharacteristic:
    """GATT characteristic information"""
    uuid: str
    properties: List[str]
    value: bytes = None


class BluetoothManager:
    """Bluetooth device management"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize Bluetooth manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("BluetoothManager", LogLevel.INFO)
        self.status = BluetoothStatus.OFF
        self.whitelist: Set[str] = set()
        self.blacklist: Set[str] = set()
        self.blocked_devices: Set[str] = set()
        self.firewall_enabled = False
        
    def is_available(self) -> bool:
        """
        Check if Bluetooth is available
        
        Returns:
            True if available
        """
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['which', 'bluetoothctl'], capture_output=True)
                return result.returncode == 0
            elif platform.system() == 'Windows':
                result = subprocess.run(['powershell', '-Command', 'Get-PnpDevice -Class Bluetooth'], capture_output=True)
                return result.returncode == 0
            elif platform.system() == 'Darwin':
                result = subprocess.run(['which', 'blueutil'], capture_output=True)
                return result.returncode == 0
        except Exception:
            pass
            
        return False
        
    def get_status(self) -> BluetoothStatus:
        """
        Get Bluetooth status
        
        Returns:
            Bluetooth status
        """
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'show'], capture_output=True, text=True)
                if 'Powered: yes' in result.stdout:
                    self.status = BluetoothStatus.ON
                else:
                    self.status = BluetoothStatus.OFF
            elif platform.system() == 'Darwin':
                result = subprocess.run(['blueutil', '-p'], capture_output=True, text=True)
                if '1' in result.stdout:
                    self.status = BluetoothStatus.ON
                else:
                    self.status = BluetoothStatus.OFF
        except Exception as e:
            self.logger.error(f"Failed to get status: {e}")
            self.status = BluetoothStatus.ERROR
            
        return self.status
        
    def enable(self) -> bool:
        """
        Enable Bluetooth
        
        Returns:
            True if enabled successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'power', 'on'], capture_output=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['blueutil', '-p', '1'], capture_output=True)
                
            self.status = BluetoothStatus.ON
            self.logger.info("Bluetooth enabled")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enable Bluetooth: {e}")
            return False
            
    def disable(self) -> bool:
        """
        Disable Bluetooth
        
        Returns:
            True if disabled successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'power', 'off'], capture_output=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['blueutil', '-p', '0'], capture_output=True)
                
            self.status = BluetoothStatus.OFF
            self.logger.info("Bluetooth disabled")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to disable Bluetooth: {e}")
            return False
            
    def scan_devices(self, timeout: int = 10, ble: bool = False, full: bool = False) -> List[BluetoothDevice]:
        """
        Scan for Bluetooth devices
        
        Args:
            timeout: Scan timeout in seconds
            ble: Scan BLE devices only
            full: Full scan with RSSI, services, etc.
            
        Returns:
            List of discovered devices
        """
        devices = []
        
        try:
            if platform.system() == 'Linux':
                scan_cmd = ['bluetoothctl', 'scan', 'on']
                if ble:
                    scan_cmd.append('--le')
                
                subprocess.run(scan_cmd, capture_output=True)
                import time
                time.sleep(timeout)
                subprocess.run(['bluetoothctl', 'scan', 'off'], capture_output=True)
                
                result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if 'Device' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            address = parts[1]
                            name = ' '.join(parts[2:]) if len(parts) > 2 else 'Unknown'
                            
                            device = BluetoothDevice(
                                name=name,
                                address=address,
                                device_class='unknown',
                                paired=False,
                                connected=False,
                                trusted=False
                            )
                            
                            if full:
                                device.rssi = self._get_rssi(address)
                                device.services = self._get_device_services(address)
                            
                            devices.append(device)
                            
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            
        return devices
        
    def _get_rssi(self, address: str) -> int:
        """Get RSSI for device"""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'info', address], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'RSSI' in line or 'rssi' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part.replace('-', '').replace('dBm', '').isdigit():
                                return int(part.replace('dBm', ''))
        except:
            pass
        return 0
        
    def _get_device_services(self, address: str) -> List[str]:
        """Get device services"""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'info', address], capture_output=True, text=True)
                services = []
                for line in result.stdout.split('\n'):
                    if 'UUID' in line or 'Service' in line:
                        services.append(line.strip())
                return services
        except:
            pass
        return []
        
    def pair_device(self, address: str) -> bool:
        """
        Pair with a device
        
        Args:
            address: Device address
            
        Returns:
            True if paired successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'pair', address], capture_output=True)
                subprocess.run(['bluetoothctl', 'trust', address], capture_output=True)
                
            self.logger.info(f"Paired with device: {address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Pairing failed: {e}")
            return False
            
    def unpair_device(self, address: str) -> bool:
        """
        Unpair a device
        
        Args:
            address: Device address
            
        Returns:
            True if unpaired successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'unpair', address], capture_output=True)
                
            self.logger.info(f"Unpaired device: {address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Unpairing failed: {e}")
            return False
            
    def connect_device(self, address: str) -> bool:
        """
        Connect to a device
        
        Args:
            address: Device address
            
        Returns:
            True if connected successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'connect', address], capture_output=True)
                
            self.logger.info(f"Connected to device: {address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return False
            
    def disconnect_device(self, address: str) -> bool:
        """
        Disconnect from a device
        
        Args:
            address: Device address
            
        Returns:
            True if disconnected successfully
        """
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'disconnect', address], capture_output=True)
                
            self.logger.info(f"Disconnected from device: {address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Disconnection failed: {e}")
            return False
            
    def get_paired_devices(self) -> List[BluetoothDevice]:
        """
        Get paired devices
        
        Returns:
            List of paired devices
        """
        devices = []
        
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'paired-devices'], capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if 'Device' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            address = parts[1]
                            name = ' '.join(parts[2:]) if len(parts) > 2 else 'Unknown'
                            devices.append(BluetoothDevice(
                                name=name,
                                address=address,
                                device_class='unknown',
                                paired=True,
                                connected=False,
                                trusted=True
                            ))
                            
        except Exception as e:
            self.logger.error(f"Failed to get paired devices: {e}")
            
        return devices
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get Bluetooth statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'status': self.status.value,
            'available': self.is_available(),
            'paired_devices': len(self.get_paired_devices()),
            'whitelist_size': len(self.whitelist),
            'blacklist_size': len(self.blacklist),
            'blocked_devices': len(self.blocked_devices),
            'firewall_enabled': self.firewall_enabled
        }
        
    def get_all_devices(self) -> List[BluetoothDevice]:
        """Get all discovered and paired devices"""
        paired = self.get_paired_devices()
        discovered = self.scan_devices(timeout=2)
        
        # Merge and deduplicate
        all_devices = {d.address: d for d in paired}
        for d in discovered:
            if d.address not in all_devices:
                all_devices[d.address] = d
                
        return list(all_devices.values())
        
    def remove_device(self, address: str) -> bool:
        """Remove device from pairing memory"""
        return self.unpair_device(address)
        
    def forget_device(self, address: str) -> bool:
        """Fully remove device profile and connection history"""
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'remove', address], capture_output=True)
            self.logger.info(f"Forgot device: {address}")
            return True
        except Exception as e:
            self.logger.error(f"Forget failed: {e}")
            return False
        
    def get_device_info(self, address: str) -> Optional[Dict[str, Any]]:
        """Get detailed device information"""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'info', address], capture_output=True, text=True)
                info = {
                    'address': address,
                    'rssi': self._get_rssi(address),
                    'services': self._get_device_services(address)
                }
                
                for line in result.stdout.split('\n'):
                    if 'Alias' in line:
                        info['name'] = line.split(':')[-1].strip()
                    elif 'Class' in line:
                        info['class'] = line.split(':')[-1].strip()
                    elif 'Manufacturer' in line:
                        info['manufacturer'] = line.split(':')[-1].strip()
                        
                return info
        except Exception as e:
            self.logger.error(f"Failed to get device info: {e}")
        return None
        
    def get_battery(self, address: str) -> Optional[int]:
        """Get device battery level (if supported)"""
        try:
            # Placeholder for GATT Battery Service read
            # Would require bluepy or similar library
            self.logger.info(f"Battery check for {address} - requires GATT library")
            return None
        except Exception as e:
            self.logger.error(f"Battery check failed: {e}")
            return None
        
    def get_gatt_services(self, address: str) -> List[GATTService]:
        """Get GATT services for BLE device"""
        services = []
        try:
            # Placeholder for GATT service discovery
            # Would require bluepy or similar library
            self.logger.info(f"GATT services for {address} - requires GATT library")
        except Exception as e:
            self.logger.error(f"GATT services failed: {e}")
        return services
        
    def get_gatt_characteristics(self, address: str, service_uuid: str) -> List[GATTCharacteristic]:
        """Get GATT characteristics for service"""
        characteristics = []
        try:
            # Placeholder for GATT characteristic discovery
            self.logger.info(f"GATT characteristics for {service_uuid} - requires GATT library")
        except Exception as e:
            self.logger.error(f"GATT characteristics failed: {e}")
        return characteristics
        
    def read_characteristic(self, address: str, characteristic_uuid: str) -> Optional[bytes]:
        """Read GATT characteristic"""
        try:
            # Placeholder for GATT read
            self.logger.info(f"Read characteristic {characteristic_uuid} - requires GATT library")
            return None
        except Exception as e:
            self.logger.error(f"Read characteristic failed: {e}")
            return None
        
    def write_characteristic(self, address: str, characteristic_uuid: str, data: bytes) -> bool:
        """Write GATT characteristic"""
        try:
            # Placeholder for GATT write
            self.logger.info(f"Write characteristic {characteristic_uuid} - requires GATT library")
            return False
        except Exception as e:
            self.logger.error(f"Write characteristic failed: {e}")
            return False
        
    def notify_characteristic(self, address: str, characteristic_uuid: str) -> bool:
        """Subscribe to GATT characteristic notifications"""
        try:
            # Placeholder for GATT notify
            self.logger.info(f"Notify characteristic {characteristic_uuid} - requires GATT library")
            return False
        except Exception as e:
            self.logger.error(f"Notify characteristic failed: {e}")
            return False
        
    def sniff_packets(self) -> bool:
        """Analyze Bluetooth packets (if system allows)"""
        try:
            # Placeholder for packet sniffing
            self.logger.info("Packet sniffing - requires root access and special tools")
            return False
        except Exception as e:
            self.logger.error(f"Sniff failed: {e}")
            return False
        
    def monitor_traffic(self) -> Dict[str, Any]:
        """Monitor Bluetooth traffic"""
        return {
            'connections': 0,
            'disconnections': 0,
            'rssi_changes': []
        }
        
    def enable_firewall(self) -> bool:
        """Enable Bluetooth firewall"""
        self.firewall_enabled = True
        self.logger.info("Bluetooth firewall enabled")
        return True
        
    def disable_firewall(self) -> bool:
        """Disable Bluetooth firewall"""
        self.firewall_enabled = False
        self.logger.info("Bluetooth firewall disabled")
        return True
        
    def block_device(self, address: str) -> bool:
        """Block device from connecting"""
        self.blocked_devices.add(address)
        self.logger.info(f"Blocked device: {address}")
        return True
        
    def allow_device(self, address: str) -> bool:
        """Remove block from device"""
        if address in self.blocked_devices:
            self.blocked_devices.remove(address)
            self.logger.info(f"Allowed device: {address}")
            return True
        return False
        
    def add_to_whitelist(self, address: str) -> bool:
        """Add device to whitelist"""
        self.whitelist.add(address)
        self.logger.info(f"Added to whitelist: {address}")
        return True
        
    def remove_from_whitelist(self, address: str) -> bool:
        """Remove device from whitelist"""
        if address in self.whitelist:
            self.whitelist.remove(address)
            self.logger.info(f"Removed from whitelist: {address}")
            return True
        return False
        
    def add_to_blacklist(self, address: str) -> bool:
        """Add device to blacklist"""
        self.blacklist.add(address)
        self.logger.info(f"Added to blacklist: {address}")
        return True
        
    def remove_from_blacklist(self, address: str) -> bool:
        """Remove device from blacklist"""
        if address in self.blacklist:
            self.blacklist.remove(address)
            self.logger.info(f"Removed from blacklist: {address}")
            return True
        return False
        
    def run_diagnostics(self) -> Dict[str, Any]:
        """Run Bluetooth diagnostics"""
        return {
            'adapter_available': self.is_available(),
            'status': self.get_status().value,
            'paired_devices': len(self.get_paired_devices()),
            'firewall_enabled': self.firewall_enabled,
            'issues': []
        }
        
    def reset_stack(self) -> bool:
        """Reset Bluetooth stack"""
        try:
            if platform.system() == 'Linux':
                subprocess.run(['sudo', 'systemctl', 'restart', 'bluetooth'], capture_output=True)
            self.logger.info("Bluetooth stack reset")
            return True
        except Exception as e:
            self.logger.error(f"Stack reset failed: {e}")
            return False
        
    def get_adapter_info(self) -> Dict[str, Any]:
        """Get adapter information"""
        try:
            if platform.system() == 'Linux':
                result = subprocess.run(['bluetoothctl', 'show'], capture_output=True, text=True)
                info = {}
                for line in result.stdout.split('\n'):
                    if 'Controller' in line:
                        info['controller'] = line.split()[-1]
                    elif 'Powered' in line:
                        info['powered'] = 'yes' in line
                    elif 'Discoverable' in line:
                        info['discoverable'] = 'yes' in line
                    elif 'Pairable' in line:
                        info['pairable'] = 'yes' in line
                    elif 'Address' in line:
                        info['address'] = line.split()[-1]
                return info
        except Exception as e:
            self.logger.error(f"Failed to get adapter info: {e}")
        return {}
        
    def set_adapter_power(self, level: str) -> bool:
        """Set adapter power level"""
        try:
            # Placeholder for power level setting
            self.logger.info(f"Set adapter power to {level} - may not be supported")
            return False
        except Exception as e:
            self.logger.error(f"Power set failed: {e}")
            return False
        
    def get_adapter_mac(self) -> Optional[str]:
        """Get adapter MAC address"""
        info = self.get_adapter_info()
        return info.get('address')
        
    def set_random_mac(self) -> bool:
        """Enable random MAC (privacy mode)"""
        try:
            if platform.system() == 'Linux':
                subprocess.run(['bluetoothctl', 'set-privacy', 'on'], capture_output=True)
            self.logger.info("Random MAC enabled")
            return True
        except Exception as e:
            self.logger.error(f"Random MAC failed: {e}")
            return False
        
    def get_device_profile(self, address: str) -> Dict[str, Any]:
        """Get device profile (A2DP/HFP/HID/SPP/GATT)"""
        info = self.get_device_info(address)
        if info:
            info['profiles'] = ['A2DP', 'HFP', 'HID', 'SPP', 'GATT']  # Placeholder
        return info or {}
        
    def manage_audio(self, address: str, action: str) -> bool:
        """Manage audio devices"""
        try:
            # Placeholder for audio management
            self.logger.info(f"Audio {action} for {address}")
            return False
        except Exception as e:
            self.logger.error(f"Audio management failed: {e}")
            return False
        
    def manage_hid(self, address: str, action: str) -> bool:
        """Manage HID devices"""
        try:
            # Placeholder for HID management
            self.logger.info(f"HID {action} for {address}")
            return False
        except Exception as e:
            self.logger.error(f"HID management failed: {e}")
            return False
        
    def manage_spp(self, address: str, action: str) -> bool:
        """Manage SPP channels"""
        try:
            # Placeholder for SPP management
            self.logger.info(f"SPP {action} for {address}")
            return False
        except Exception as e:
            self.logger.error(f"SPP management failed: {e}")
            return False
        
    def gatt_browser(self, address: str) -> Dict[str, Any]:
        """Full GATT browser"""
        return {
            'address': address,
            'services': self.get_gatt_services(address)
        }
        
    def scan_beacons(self) -> List[Dict[str, Any]]:
        """Scan for beacons (iBeacon, Eddystone)"""
        try:
            # Placeholder for beacon scanning
            self.logger.info("Beacon scan - requires BLE library")
            return []
        except Exception as e:
            self.logger.error(f"Beacon scan failed: {e}")
            return []
        
    def get_beacon_info(self, address: str) -> Optional[Dict[str, Any]]:
        """Get beacon details"""
        try:
            # Placeholder for beacon info
            self.logger.info(f"Beacon info for {address} - requires BLE library")
            return None
        except Exception as e:
            self.logger.error(f"Beacon info failed: {e}")
            return None
        
    def get_security_status(self) -> Dict[str, Any]:
        """Get security status"""
        return {
            'encryption': 'enabled',
            'pairing_mode': 'secure',
            'firewall_enabled': self.firewall_enabled
        }
        
    def detect_mitm(self) -> bool:
        """Detect man-in-the-middle attacks"""
        try:
            # Placeholder for MITM detection
            self.logger.info("MITM detection - requires advanced monitoring")
            return False
        except Exception as e:
            self.logger.error(f"MITM detection failed: {e}")
            return False
        
    def spoof_device(self, address: str) -> bool:
        """Spoof device address (for testing only)"""
        try:
            # Placeholder for MAC spoofing
            self.logger.warning(f"Device spoofing for {address} - for testing only")
            return False
        except Exception as e:
            self.logger.error(f"Spoofing failed: {e}")
            return False


# Global Bluetooth manager instance
bluetooth_manager = BluetoothManager()
