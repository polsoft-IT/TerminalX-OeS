"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkManager
  VERSION: 1.0.0
  MODULE CLASS: NetworkManager
  DESCRIPTION:
       Network management system for TerminalX

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

import socket
import subprocess
import platform
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class NetworkStatus(Enum):
    """Network status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    ERROR = "error"


@dataclass
class NetworkInterface:
    """Network interface information"""
    name: str
    ip_address: str
    netmask: str
    mac_address: str
    status: NetworkStatus
    is_up: bool


@dataclass
class ConnectionInfo:
    """Connection information"""
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    protocol: str
    state: str


class NetworkManager:
    """Network management system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize network manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("NetworkManager", LogLevel.INFO)
        self.monitored_ports: Set[int] = set()
        self.connection_history: List[ConnectionInfo] = []
        
    def get_interfaces(self) -> List[NetworkInterface]:
        """
        Get network interfaces
        
        Returns:
            List of network interfaces
        """
        interfaces = []
        
        try:
            # Get interfaces based on platform
            if platform.system() == 'Windows':
                interfaces = self._get_windows_interfaces()
            else:
                interfaces = self._get_unix_interfaces()
                
        except Exception as e:
            self.logger.error(f"Failed to get interfaces: {e}")
            
        return interfaces
        
    def _get_windows_interfaces(self) -> List[NetworkInterface]:
        """Get Windows network interfaces"""
        interfaces = []
        
        try:
            result = subprocess.run(
                ['ipconfig', '/all'],
                capture_output=True,
                text=True
            )
            
            # Parse ipconfig output (simplified)
            current_interface = None
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                if line.startswith('Ethernet adapter') or line.startswith('Wireless LAN adapter'):
                    if current_interface:
                        interfaces.append(current_interface)
                    current_interface = NetworkInterface(
                        name=line.split('adapter')[1].strip().rstrip(':'),
                        ip_address='',
                        netmask='',
                        mac_address='',
                        status=NetworkStatus.CONNECTED,
                        is_up=True
                    )
                elif current_interface:
                    if 'IPv4 Address' in line:
                        current_interface.ip_address = line.split(':')[-1].strip()
                    elif 'Physical Address' in line:
                        current_interface.mac_address = line.split(':')[-1].strip()
                        
            if current_interface:
                interfaces.append(current_interface)
                
        except Exception as e:
            self.logger.error(f"Windows interface detection failed: {e}")
            
        return interfaces
        
    def _get_unix_interfaces(self) -> List[NetworkInterface]:
        """Get Unix network interfaces"""
        interfaces = []
        
        try:
            result = subprocess.run(
                ['ifconfig', '-a'],
                capture_output=True,
                text=True
            )
            
            # Parse ifconfig output (simplified)
            current_interface = None
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                if line and not line.startswith(' ') and ':' in line:
                    if current_interface:
                        interfaces.append(current_interface)
                    
                    name = line.split(':')[0]
                    is_up = 'UP' in line or 'RUNNING' in line
                    
                    current_interface = NetworkInterface(
                        name=name,
                        ip_address='',
                        netmask='',
                        mac_address='',
                        status=NetworkStatus.CONNECTED if is_up else NetworkStatus.DISCONNECTED,
                        is_up=is_up
                    )
                elif current_interface:
                    if 'inet ' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == 'inet' and i + 1 < len(parts):
                                current_interface.ip_address = parts[i + 1]
                                break
                    elif 'ether' in line or 'HWaddr' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ['ether', 'HWaddr'] and i + 1 < len(parts):
                                current_interface.mac_address = parts[i + 1]
                                break
                                
            if current_interface:
                interfaces.append(current_interface)
                
        except Exception as e:
            self.logger.error(f"Unix interface detection failed: {e}")
            
        return interfaces
        
    def get_active_connections(self) -> List[ConnectionInfo]:
        """
        Get active network connections
        
        Returns:
            List of connection info
        """
        connections = []
        
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(
                    ['netstat', '-ano'],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['netstat', '-tuln'],
                    capture_output=True,
                    text=True
                )
                
            # Parse netstat output (simplified)
            for line in result.stdout.split('\n'):
                if 'TCP' in line or 'UDP' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        protocol = parts[0]
                        local = parts[1].split(':')
                        remote = parts[2].split(':')
                        state = parts[3] if len(parts) > 3 else ''
                        
                        connections.append(ConnectionInfo(
                            local_address=local[0] if len(local) > 0 else '',
                            local_port=int(local[-1]) if len(local) > 1 else 0,
                            remote_address=remote[0] if len(remote) > 0 else '',
                            remote_port=int(remote[-1]) if len(remote) > 1 else 0,
                            protocol=protocol,
                            state=state
                        ))
                        
        except Exception as e:
            self.logger.error(f"Failed to get connections: {e}")
            
        return connections
        
    def check_port(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if port is open
        
        Args:
            host: Host address
            port: Port number
            timeout: Connection timeout
            
        Returns:
            True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception as e:
            self.logger.error(f"Port check failed: {e}")
            return False
            
    def scan_ports(self, host: str, ports: List[int], timeout: float = 1.0) -> Dict[int, bool]:
        """
        Scan multiple ports
        
        Args:
            host: Host address
            ports: List of ports to scan
            timeout: Connection timeout
            
        Returns:
            Dictionary of port -> open status
        """
        results = {}
        
        for port in ports:
            results[port] = self.check_port(host, port, timeout)
            
        return results
        
    def get_dns_servers(self) -> List[str]:
        """
        Get DNS servers
        
        Returns:
            List of DNS server addresses
        """
        dns_servers = []
        
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(
                    ['nslookup', 'localhost'],
                    capture_output=True,
                    text=True
                )
                # Parse DNS from nslookup output
                for line in result.stdout.split('\n'):
                    if 'Server:' in line:
                        dns = line.split(':')[-1].strip()
                        if dns:
                            dns_servers.append(dns)
            else:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1].strip()
                            dns_servers.append(dns)
                            
        except Exception as e:
            self.logger.error(f"Failed to get DNS servers: {e}")
            
        return dns_servers
        
    def ping(self, host: str, count: int = 4) -> Dict[str, Any]:
        """
        Ping a host
        
        Args:
            host: Host address
            count: Number of pings
            
        Returns:
            Ping results
        """
        try:
            if platform.system() == 'Windows':
                cmd = ['ping', '-n', str(count), host]
            else:
                cmd = ['ping', '-c', str(count), host]
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                'host': host,
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            self.logger.error(f"Ping failed: {e}")
            return {
                'host': host,
                'success': False,
                'output': '',
                'error': str(e)
            }
            
    def get_hostname(self) -> str:
        """
        Get system hostname
        
        Returns:
            Hostname
        """
        try:
            return socket.gethostname()
        except Exception as e:
            self.logger.error(f"Failed to get hostname: {e}")
            return "unknown"
            
    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address or None
        """
        try:
            return socket.gethostbyname(hostname)
        except Exception as e:
            self.logger.error(f"Failed to resolve {hostname}: {e}")
            return None
            
    def monitor_port(self, port: int) -> bool:
        """
        Start monitoring a port
        
        Args:
            port: Port to monitor
            
        Returns:
            True if monitoring started
        """
        self.monitored_ports.add(port)
        self.logger.info(f"Monitoring port: {port}")
        return True
        
    def unmonitor_port(self, port: int) -> bool:
        """
        Stop monitoring a port
        
        Args:
            port: Port to unmonitor
            
        Returns:
            True if unmonitored
        """
        if port in self.monitored_ports:
            self.monitored_ports.remove(port)
            self.logger.info(f"Stopped monitoring port: {port}")
            return True
        return False
        
    def get_monitored_ports(self) -> Set[int]:
        """
        Get monitored ports
        
        Returns:
            Set of monitored ports
        """
        return self.monitored_ports.copy()
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get network manager statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'interfaces': len(self.get_interfaces()),
            'connections': len(self.get_active_connections()),
            'monitored_ports': len(self.monitored_ports),
            'hostname': self.get_hostname()
        }


# Global network manager instance
network_manager = NetworkManager()
