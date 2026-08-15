"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkSandbox
  VERSION: 1.0.0
  MODULE CLASS: NetworkSandbox
  DESCRIPTION:
       Network sandboxing and isolation for TerminalX security

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

from typing import Dict, Any, List, Set


class NetworkSandbox:
    """Network sandbox for isolation"""
    
    def __init__(self):
        self.enabled = False
        self.allowed_hosts: Set[str] = set()
        self.allowed_ports: Set[int] = set()
        self.blocked_hosts: Set[str] = set()
        self.blocked_ports: Set[int] = set()
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize sandbox"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        
        self.allowed_hosts = set(self.config.get('allowed_hosts', []))
        self.allowed_ports = set(self.config.get('allowed_ports', []))
        self.blocked_hosts = set(self.config.get('blocked_hosts', []))
        self.blocked_ports = set(self.config.get('blocked_ports', []))
        
    async def allow_host(self, host: str):
        """Allow a host"""
        self.allowed_hosts.add(host)
        
    async def block_host(self, host: str):
        """Block a host"""
        self.blocked_hosts.add(host)
        
    async def allow_port(self, port: int):
        """Allow a port"""
        self.allowed_ports.add(port)
        
    async def block_port(self, port: int):
        """Block a port"""
        self.blocked_ports.add(port)
        
    async def check_connection(self, host: str, port: int) -> bool:
        """Check if connection is allowed"""
        if not self.enabled:
            return True
            
        # Check blocked
        if host in self.blocked_hosts:
            return False
        if port in self.blocked_ports:
            return False
            
        # Check allowed
        if self.allowed_hosts and host not in self.allowed_hosts:
            return False
        if self.allowed_ports and port not in self.allowed_ports:
            return False
            
        return True
        
    async def get_rules(self) -> Dict[str, List]:
        """Get current rules"""
        return {
            'allowed_hosts': list(self.allowed_hosts),
            'allowed_ports': list(self.allowed_ports),
            'blocked_hosts': list(self.blocked_hosts),
            'blocked_ports': list(self.blocked_ports),
        }
