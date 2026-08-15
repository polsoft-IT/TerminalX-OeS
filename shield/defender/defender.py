"""
 ============================================================
  MODULE/PLUGIN NAME: Defender
  VERSION: 1.0.0
  MODULE CLASS: Defender
  DESCRIPTION:
       Malware protection and scanning for TerminalX security

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
import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class ScanStatus(Enum):
    """Scan status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ThreatLevel(Enum):
    """Threat level"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Defender:
    """Malware defender"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.signatures: Dict[str, Dict] = {}
        self.quarantine: Dict[str, Dict] = {}
        self.scan_results: List[Dict] = []
        self.active_scans: Dict[str, Dict] = {}
        self.real_time_monitoring = False
        self.monitor_tasks: List[asyncio.Task] = []
        self.notification_callback = None
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize defender"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.real_time_monitoring = self.config.get('real_time_monitoring', False)
        
        # Load signatures
        await self._load_signatures()
        
        # Start real-time monitoring if enabled
        if self.real_time_monitoring and self.enabled:
            await self.start_monitoring()
            
    def set_notification_callback(self, callback):
        """Set callback for threat notifications"""
        self.notification_callback = callback
        
    async def _load_signatures(self):
        """Load malware signatures"""
        # Load from file if exists
        sig_file = os.path.join(
            os.path.dirname(__file__), '..', '..', 'config', 'shield', 'signatures.json'
        )
        
        if os.path.exists(sig_file):
            try:
                with open(sig_file, 'r') as f:
                    self.signatures = json.load(f)
                return
            except Exception:
                pass
        
        # Default signatures
        self.signatures = {
            'eicar': {
                'hash': '44d88612fea8a8f36de82e1278abb02f',
                'name': 'EICAR Test File',
                'severity': 'critical',
                'description': 'Standard antivirus test file'
            },
        }
        
    async def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan a file for malware"""
        if not self.enabled:
            return {'safe': True, 'threat_level': ThreatLevel.SAFE.value, 'reason': 'Defender disabled'}
            
        try:
            # Calculate file hash
            file_hash = await self._calculate_hash(file_path)
            
            # Check against signatures
            threat_found = None
            for sig_name, sig_data in self.signatures.items():
                if sig_data['hash'] == file_hash:
                    threat_found = {
                        'name': sig_data['name'],
                        'severity': sig_data['severity'],
                        'description': sig_data.get('description', ''),
                    }
                    break
            
            if threat_found:
                result = {
                    'safe': False,
                    'threat_level': ThreatLevel.CRITICAL.value,
                    'threat': threat_found['name'],
                    'severity': threat_found['severity'],
                    'description': threat_found['description'],
                    'hash': file_hash,
                    'file_path': file_path,
                    'timestamp': datetime.now().isoformat(),
                }
                self.scan_results.append(result)
                
                # Send notification
                if self.notification_callback:
                    await self.notification_callback(
                        f"Threat detected: {threat_found['name']}",
                        f"File: {file_path}\nHash: {file_hash}",
                        'security',
                        'critical'
                    )
                
                return result
                
            # Heuristic check
            suspicious = await self._heuristic_check(file_path)
            
            if suspicious:
                result = {
                    'safe': False,
                    'threat_level': ThreatLevel.MEDIUM.value,
                    'threat': 'suspicious',
                    'reason': suspicious,
                    'hash': file_hash,
                    'file_path': file_path,
                    'timestamp': datetime.now().isoformat(),
                }
                self.scan_results.append(result)
                
                # Send notification
                if self.notification_callback:
                    await self.notification_callback(
                        "Suspicious file detected",
                        f"File: {file_path}\nReason: {suspicious}",
                        'security',
                        'high'
                    )
                
                return result
                
            return {
                'safe': True,
                'threat_level': ThreatLevel.SAFE.value,
                'hash': file_hash,
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
            }
            
        except Exception as e:
            return {
                'safe': False,
                'threat_level': ThreatLevel.LOW.value,
                'error': str(e),
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
            }
            
    async def _calculate_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file"""
        md5 = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception:
            return ''
        
    async def _heuristic_check(self, file_path: str) -> Optional[str]:
        """Heuristic malware detection"""
        # Check file extension
        suspicious_extensions = ['.exe', '.dll', '.bat', '.cmd', '.scr', '.vbs', '.ps1', '.js']
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in suspicious_extensions:
            return 'suspicious_extension'
            
        # Check file size (very small executables are suspicious)
        try:
            size = os.path.getsize(file_path)
            if size < 1024 and ext in ['.exe', '.dll']:
                return 'suspicious_size'
            if size > 100 * 1024 * 1024:  # > 100MB
                return 'large_suspicious_file'
        except:
            pass
            
        # Check for double extensions
        filename = os.path.basename(file_path)
        if '.' in filename:
            parts = filename.split('.')
            if len(parts) > 2:
                return 'double_extension'
            
        return None
        
    async def scan_directory(self, directory: str, recursive: bool = True) -> Dict[str, Any]:
        """Scan a directory"""
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        self.active_scans[scan_id] = {
            'id': scan_id,
            'directory': directory,
            'status': ScanStatus.RUNNING.value,
            'started': datetime.now().isoformat(),
            'files_scanned': 0,
            'threats_found': 0,
        }
        
        results = []
        threats_found = 0
        files_scanned = 0
        
        try:
            if recursive:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        result = await self.scan_file(file_path)
                        results.append({
                            'file': file_path,
                            'result': result,
                        })
                        files_scanned += 1
                        if not result.get('safe', True):
                            threats_found += 1
            else:
                for item in os.listdir(directory):
                    file_path = os.path.join(directory, item)
                    if os.path.isfile(file_path):
                        result = await self.scan_file(file_path)
                        results.append({
                            'file': file_path,
                            'result': result,
                        })
                        files_scanned += 1
                        if not result.get('safe', True):
                            threats_found += 1
            
            self.active_scans[scan_id]['status'] = ScanStatus.COMPLETED.value
            self.active_scans[scan_id]['files_scanned'] = files_scanned
            self.active_scans[scan_id]['threats_found'] = threats_found
            self.active_scans[scan_id]['completed'] = datetime.now().isoformat()
            
            return {
                'scan_id': scan_id,
                'results': results,
                'summary': {
                    'files_scanned': files_scanned,
                    'threats_found': threats_found,
                    'status': ScanStatus.COMPLETED.value,
                }
            }
            
        except Exception as e:
            self.active_scans[scan_id]['status'] = ScanStatus.FAILED.value
            self.active_scans[scan_id]['error'] = str(e)
            return {
                'scan_id': scan_id,
                'error': str(e),
                'summary': {'status': ScanStatus.FAILED.value}
            }
        
    async def quarantine_file(self, file_path: str) -> bool:
        """Quarantine a file"""
        try:
            # Move to quarantine directory
            quarantine_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'quarantine'
            )
            os.makedirs(quarantine_dir, exist_ok=True)
            
            quarantine_path = os.path.join(
                quarantine_dir,
                os.path.basename(file_path) + '.quarantine'
            )
            
            os.rename(file_path, quarantine_path)
            
            self.quarantine[file_path] = {
                'original_path': file_path,
                'quarantine_path': quarantine_path,
                'timestamp': datetime.now().isoformat(),
            }
            
            return True
            
        except Exception as e:
            print(f"Quarantine error: {e}")
            return False
            
    async def restore_file(self, file_path: str) -> bool:
        """Restore a quarantined file"""
        if file_path not in self.quarantine:
            return False
            
        try:
            quarantine_info = self.quarantine[file_path]
            os.rename(quarantine_info['quarantine_path'], file_path)
            del self.quarantine[file_path]
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
            
    async def get_scan_results(self, limit: int = 100) -> List[Dict]:
        """Get recent scan results"""
        return self.scan_results[-limit:]
        
    async def get_quarantined_files(self) -> List[Dict]:
        """Get quarantined files"""
        return list(self.quarantine.values())
        
    async def get_scan_status(self, scan_id: str) -> Optional[Dict]:
        """Get scan status"""
        return self.active_scans.get(scan_id)
        
    async def get_all_scans(self) -> List[Dict]:
        """Get all scans"""
        return list(self.active_scans.values())
        
    async def enable(self):
        """Enable defender"""
        self.enabled = True
        if self.real_time_monitoring:
            await self.start_monitoring()
            
    async def disable(self):
        """Disable defender"""
        self.enabled = False
        await self.stop_monitoring()
        
    async def start_monitoring(self):
        """Start real-time monitoring"""
        if not self.real_time_monitoring:
            self.real_time_monitoring = True
            
        # Start monitor task
        task = asyncio.create_task(self._monitor_loop())
        self.monitor_tasks.append(task)
        
    async def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.real_time_monitoring = False
        
        # Cancel monitor tasks
        for task in self.monitor_tasks:
            task.cancel()
        self.monitor_tasks.clear()
        
    async def _monitor_loop(self):
        """Real-time monitoring loop"""
        while self.real_time_monitoring:
            try:
                # Monitor common directories
                monitor_dirs = [
                    os.path.expanduser('~/Downloads'),
                    os.path.expanduser('~/Desktop'),
                    os.path.expanduser('~/Documents'),
                ]
                
                for directory in monitor_dirs:
                    if os.path.exists(directory):
                        for item in os.listdir(directory):
                            file_path = os.path.join(directory, item)
                            if os.path.isfile(file_path):
                                # Check if file was recently created (last 5 seconds)
                                try:
                                    stat = os.stat(file_path)
                                    if stat.st_ctime > (asyncio.get_event_loop().time() - 5):
                                        await self.scan_file(file_path)
                                except:
                                    pass
                                    
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(5)
                
    async def add_signature(self, name: str, hash_value: str, severity: str = 'medium', 
                           description: str = '') -> bool:
        """Add a malware signature"""
        self.signatures[name] = {
            'hash': hash_value,
            'name': name,
            'severity': severity,
            'description': description,
        }
        return True
        
    async def remove_signature(self, name: str) -> bool:
        """Remove a malware signature"""
        if name in self.signatures:
            del self.signatures[name]
            return True
        return False
        
    async def get_signatures(self) -> Dict[str, Dict]:
        """Get all signatures"""
        return self.signatures.copy()
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get defender statistics"""
        return {
            'enabled': self.enabled,
            'real_time_monitoring': self.real_time_monitoring,
            'signatures_count': len(self.signatures),
            'quarantined_count': len(self.quarantine),
            'scan_results_count': len(self.scan_results),
            'active_scans_count': len(self.active_scans),
        }
