"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkManager
  VERSION: 1.0.0
  MODULE CLASS: NetworkManager
  DESCRIPTION:
       Network connection management for TerminalX network operations

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

import asyncio
from typing import Dict, Any, Optional, List


class NetworkManager:
    """Network connection manager"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.active_connections: Dict[str, Dict] = {}
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize network manager"""
        self.config = config or {}
        
    async def connect(self, connection_id: str, host: str, port: int,
                     protocol: str = 'tcp') -> bool:
        """Establish a network connection"""
        try:
            if protocol.lower() == 'tcp':
                reader, writer = await asyncio.open_connection(host, port)
                
                self.active_connections[connection_id] = {
                    'id': connection_id,
                    'host': host,
                    'port': port,
                    'protocol': protocol,
                    'reader': reader,
                    'writer': writer,
                    'status': 'connected',
                }
                return True
                
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
        return False
        
    async def disconnect(self, connection_id: str) -> bool:
        """Close a network connection"""
        if connection_id not in self.active_connections:
            return False
            
        conn = self.active_connections[connection_id]
        
        try:
            if 'writer' in conn:
                conn['writer'].close()
                await conn['writer'].wait_closed()
                
            del self.active_connections[connection_id]
            return True
            
        except Exception as e:
            print(f"Disconnection error: {e}")
            return False
            
    async def send(self, connection_id: str, data: bytes) -> bool:
        """Send data over a connection"""
        if connection_id not in self.active_connections:
            return False
            
        conn = self.active_connections[connection_id]
        
        try:
            conn['writer'].write(data)
            await conn['writer'].drain()
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
            
    async def receive(self, connection_id: str, size: int = 4096) -> Optional[bytes]:
        """Receive data from a connection"""
        if connection_id not in self.active_connections:
            return None
            
        conn = self.active_connections[connection_id]
        
        try:
            data = await conn['reader'].read(size)
            return data
        except Exception as e:
            print(f"Receive error: {e}")
            return None
            
    async def get_connection(self, connection_id: str) -> Optional[Dict]:
        """Get connection info"""
        if connection_id in self.active_connections:
            conn = self.active_connections[connection_id].copy()
            # Remove non-serializable objects
            conn.pop('reader', None)
            conn.pop('writer', None)
            return conn
        return None
        
    async def list_connections(self) -> List[Dict]:
        """List all active connections"""
        connections = []
        
        for conn_id, conn in self.active_connections.items():
            conn_info = conn.copy()
            conn_info.pop('reader', None)
            conn_info.pop('writer', None)
            connections.append(conn_info)
            
        return connections
