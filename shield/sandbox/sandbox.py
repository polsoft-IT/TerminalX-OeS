"""
 ============================================================
  MODULE/PLUGIN NAME: Sandbox
  VERSION: 1.0.0
  MODULE CLASS: Sandbox
  DESCRIPTION:
       Application sandboxing for TerminalX security isolation

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
import os
import tempfile
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class SandboxStatus(Enum):
    """Sandbox status"""
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    DESTROYED = "destroyed"
    ERROR = "error"


class Sandbox:
    """Application sandbox"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.active_sandboxes: Dict[str, Dict] = {}
        self.sandbox_dir: Optional[str] = None
        self.notification_callback = None
        self.sandbox_history: List[Dict] = []
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize sandbox"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        
        # Create sandbox directory
        self.sandbox_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 'sandbox'
        )
        os.makedirs(self.sandbox_dir, exist_ok=True)
        
    def set_notification_callback(self, callback):
        """Set callback for sandbox notifications"""
        self.notification_callback = callback
        
    async def create_sandbox(self, sandbox_id: str, 
                            restrictions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new sandbox"""
        if not self.enabled:
            return {'success': False, 'error': 'Sandbox disabled'}
            
        if sandbox_id in self.active_sandboxes:
            return {'success': False, 'error': 'Sandbox already exists'}
            
        sandbox_path = os.path.join(self.sandbox_dir, sandbox_id)
        
        try:
            os.makedirs(sandbox_path, exist_ok=True)
            
            # Create isolated directories
            os.makedirs(os.path.join(sandbox_path, 'home'), exist_ok=True)
            os.makedirs(os.path.join(sandbox_path, 'tmp'), exist_ok=True)
            os.makedirs(os.path.join(sandbox_path, 'var'), exist_ok=True)
            os.makedirs(os.path.join(sandbox_path, 'etc'), exist_ok=True)
            
            sandbox_info = {
                'id': sandbox_id,
                'path': sandbox_path,
                'restrictions': restrictions or {},
                'status': SandboxStatus.CREATED.value,
                'created': datetime.now().isoformat(),
                'active': True,
                'processes': [],
            }
            
            self.active_sandboxes[sandbox_id] = sandbox_info
            
            # Add to history
            self.sandbox_history.append({
                'action': 'created',
                'sandbox_id': sandbox_id,
                'timestamp': datetime.now().isoformat(),
            })
            
            # Send notification
            if self.notification_callback:
                await self.notification_callback(
                    f"Sandbox created: {sandbox_id}",
                    f"New sandbox environment created at {sandbox_path}",
                    'system',
                    'low'
                )
            
            return {'success': True, 'sandbox': sandbox_info}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
    async def destroy_sandbox(self, sandbox_id: str) -> Dict[str, Any]:
        """Destroy a sandbox"""
        if sandbox_id not in self.active_sandboxes:
            return {'success': False, 'error': 'Sandbox not found'}
            
        sandbox = self.active_sandboxes[sandbox_id]
        sandbox_path = sandbox['path']
        
        # Remove sandbox directory
        try:
            shutil.rmtree(sandbox_path)
            
            # Add to history
            self.sandbox_history.append({
                'action': 'destroyed',
                'sandbox_id': sandbox_id,
                'timestamp': datetime.now().isoformat(),
            })
            
            # Send notification
            if self.notification_callback:
                await self.notification_callback(
                    f"Sandbox destroyed: {sandbox_id}",
                    f"Sandbox environment removed",
                    'system',
                    'low'
                )
            
            del self.active_sandboxes[sandbox_id]
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    async def run_in_sandbox(self, sandbox_id: str, command: List[str]) -> Dict[str, Any]:
        """Run a command in a sandbox"""
        if sandbox_id not in self.active_sandboxes:
            return {'success': False, 'error': 'Sandbox not found'}
            
        sandbox = self.active_sandboxes[sandbox_id]
        
        # Update sandbox status
        sandbox['status'] = SandboxStatus.RUNNING.value
        
        # Placeholder for actual sandboxed execution
        # In a real implementation, this would use chroot, containers, etc.
        result = {
            'success': True,
            'sandbox_id': sandbox_id,
            'command': command,
            'output': f"Executed in sandbox: {sandbox_id}",
            'exit_code': 0,
            'timestamp': datetime.now().isoformat(),
        }
        
        # Add to history
        self.sandbox_history.append({
            'action': 'executed',
            'sandbox_id': sandbox_id,
            'command': command,
            'timestamp': datetime.now().isoformat(),
        })
        
        sandbox['status'] = SandboxStatus.STOPPED.value
        return result
        
    async def get_sandbox_info(self, sandbox_id: str) -> Optional[Dict]:
        """Get sandbox information"""
        if sandbox_id in self.active_sandboxes:
            return self.active_sandboxes[sandbox_id].copy()
        return None
        
    async def list_sandboxes(self) -> List[Dict]:
        """List all active sandboxes"""
        return list(self.active_sandboxes.values())
        
    async def add_restriction(self, sandbox_id: str, 
                              restriction_type: str, value: Any) -> Dict[str, Any]:
        """Add a restriction to a sandbox"""
        if sandbox_id not in self.active_sandboxes:
            return {'success': False, 'error': 'Sandbox not found'}
            
        sandbox = self.active_sandboxes[sandbox_id]
        
        if 'restrictions' not in sandbox:
            sandbox['restrictions'] = {}
            
        if restriction_type not in sandbox['restrictions']:
            sandbox['restrictions'][restriction_type] = []
            
        sandbox['restrictions'][restriction_type].append(value)
        return {'success': True}
        
    async def remove_restriction(self, sandbox_id: str, 
                                 restriction_type: str, value: Any) -> Dict[str, Any]:
        """Remove a restriction from a sandbox"""
        if sandbox_id not in self.active_sandboxes:
            return {'success': False, 'error': 'Sandbox not found'}
            
        sandbox = self.active_sandboxes[sandbox_id]
        
        if restriction_type in sandbox['restrictions']:
            if value in sandbox['restrictions'][restriction_type]:
                sandbox['restrictions'][restriction_type].remove(value)
                return {'success': True}
                
        return {'success': False, 'error': 'Restriction not found'}
        
    async def get_history(self, limit: int = 50) -> List[Dict]:
        """Get sandbox history"""
        return self.sandbox_history[-limit:]
        
    async def enable(self):
        """Enable sandbox"""
        self.enabled = True
        
    async def disable(self):
        """Disable sandbox"""
        self.enabled = False
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get sandbox statistics"""
        return {
            'enabled': self.enabled,
            'active_sandboxes': len(self.active_sandboxes),
            'history_entries': len(self.sandbox_history),
        }
