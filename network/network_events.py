"""
 ============================================================
  MODULE/PLUGIN NAME: NetworkEvents
  VERSION: 1.0.0
  MODULE CLASS: NetworkEvents
  DESCRIPTION:
       Network event handling for TerminalX network operations

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

from typing import Dict, Any, List, Callable


class NetworkEvents:
    """Network event handler"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        
    async def subscribe(self, event: str, callback: Callable):
        """Subscribe to network events"""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
        
    async def unsubscribe(self, event: str, callback: Callable):
        """Unsubscribe from network events"""
        if event in self.listeners and callback in self.listeners[event]:
            self.listeners[event].remove(callback)
            
    async def emit(self, event: str, data: Dict[str, Any]):
        """Emit a network event"""
        if event not in self.listeners:
            return
            
        for callback in self.listeners[event]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                print(f"Event handler error: {e}")
                
    async def emit_connection_established(self, connection_id: str, host: str, port: int):
        """Emit connection established event"""
        await self.emit('connection.established', {
            'connection_id': connection_id,
            'host': host,
            'port': port,
            'timestamp': asyncio.get_event_loop().time(),
        })
        
    async def emit_connection_closed(self, connection_id: str):
        """Emit connection closed event"""
        await self.emit('connection.closed', {
            'connection_id': connection_id,
            'timestamp': asyncio.get_event_loop().time(),
        })
        
    async def emit_data_received(self, connection_id: str, size: int):
        """Emit data received event"""
        await self.emit('data.received', {
            'connection_id': connection_id,
            'size': size,
            'timestamp': asyncio.get_event_loop().time(),
        })
        
    async def emit_data_sent(self, connection_id: str, size: int):
        """Emit data sent event"""
        await self.emit('data.sent', {
            'connection_id': connection_id,
            'size': size,
            'timestamp': asyncio.get_event_loop().time(),
        })
        
    async def emit_error(self, connection_id: str, error: str):
        """Emit error event"""
        await self.emit('network.error', {
            'connection_id': connection_id,
            'error': error,
            'timestamp': asyncio.get_event_loop().time(),
        })
