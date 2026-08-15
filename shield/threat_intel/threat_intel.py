"""
 ============================================================
  MODULE/PLUGIN NAME: ThreatIntel
  VERSION: 1.0.0
  MODULE CLASS: ThreatIntel
  DESCRIPTION:
       Threat intelligence and analysis for TerminalX security

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
import json
import os
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from enum import Enum


class ThreatSeverity(Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IOCType(Enum):
    """Indicator of compromise types"""
    IP = "ip"
    DOMAIN = "domain"
    HASH = "hash"
    URL = "url"
    EMAIL = "email"


class ThreatIntel:
    """Threat intelligence"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.ioc_database: Dict[str, Dict] = {}
        self.threat_feeds: List[str] = []
        self.alerts: List[Dict] = []
        self.notification_callback = None
        self.last_feed_update = None
        self.feed_update_interval = 3600  # 1 hour
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize threat intel"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.feed_update_interval = self.config.get('feed_update_interval', 3600)
        
        # Load IOC database
        await self._load_ioc_database()
        
        # Start feed update task if enabled
        if self.enabled and self.config.get('auto_update_feeds', False):
            asyncio.create_task(self._feed_update_loop())
            
    def set_notification_callback(self, callback):
        """Set callback for threat notifications"""
        self.notification_callback = callback
        
    async def _load_ioc_database(self):
        """Load indicators of compromise database"""
        # Try to load from file
        ioc_file = os.path.join(
            os.path.dirname(__file__), '..', '..', 'config', 'shield', 'ioc_database.json'
        )
        
        if os.path.exists(ioc_file):
            try:
                with open(ioc_file, 'r') as f:
                    self.ioc_database = json.load(f)
                return
            except Exception:
                pass
        
        # Default IOC database
        self.ioc_database = {
            'malicious_ips': {
                '192.0.2.1': {'source': 'internal', 'confidence': 0.9, 'severity': 'high'},
                '203.0.113.1': {'source': 'external', 'confidence': 0.8, 'severity': 'medium'},
            },
            'malicious_domains': {
                'malicious.example.com': {'source': 'external', 'confidence': 0.9, 'severity': 'critical'},
            },
            'malicious_hashes': {
                '44d88612fea8a8f36de82e1278abb02f': {'source': 'eicar', 'confidence': 1.0, 'severity': 'critical'},
            },
            'malicious_urls': {
                'http://malicious.example.com/payload': {'source': 'external', 'confidence': 0.85, 'severity': 'high'},
            },
        }
        
    async def check_ip(self, ip: str) -> Dict[str, Any]:
        """Check if IP is malicious"""
        if not self.enabled:
            return {'malicious': False, 'reason': 'Threat intel disabled'}
            
        malicious_ips = self.ioc_database.get('malicious_ips', {})
        
        if ip in malicious_ips:
            result = {
                'malicious': True,
                'confidence': malicious_ips[ip]['confidence'],
                'source': malicious_ips[ip]['source'],
                'severity': malicious_ips[ip].get('severity', 'medium'),
                'timestamp': datetime.now().isoformat(),
            }
            
            # Send notification for malicious IP
            if self.notification_callback:
                await self.notification_callback(
                    f"Malicious IP detected: {ip}",
                    f"Confidence: {result['confidence']}%, Severity: {result['severity']}",
                    'security',
                    result['severity']
                )
            
            return result
            
        return {
            'malicious': False,
            'timestamp': datetime.now().isoformat(),
        }
        
    async def check_domain(self, domain: str) -> Dict[str, Any]:
        """Check if domain is malicious"""
        if not self.enabled:
            return {'malicious': False, 'reason': 'Threat intel disabled'}
            
        malicious_domains = self.ioc_database.get('malicious_domains', {})
        
        if domain in malicious_domains:
            result = {
                'malicious': True,
                'confidence': malicious_domains[domain]['confidence'],
                'source': malicious_domains[domain]['source'],
                'severity': malicious_domains[domain].get('severity', 'medium'),
                'timestamp': datetime.now().isoformat(),
            }
            
            # Send notification for malicious domain
            if self.notification_callback:
                await self.notification_callback(
                    f"Malicious domain detected: {domain}",
                    f"Confidence: {result['confidence']}%, Severity: {result['severity']}",
                    'security',
                    result['severity']
                )
            
            return result
            
        return {
            'malicious': False,
            'timestamp': datetime.now().isoformat(),
        }
        
    async def check_hash(self, file_hash: str) -> Dict[str, Any]:
        """Check if file hash is malicious"""
        if not self.enabled:
            return {'malicious': False, 'reason': 'Threat intel disabled'}
            
        malicious_hashes = self.ioc_database.get('malicious_hashes', {})
        
        if file_hash in malicious_hashes:
            result = {
                'malicious': True,
                'confidence': malicious_hashes[file_hash]['confidence'],
                'source': malicious_hashes[file_hash]['source'],
                'severity': malicious_hashes[file_hash].get('severity', 'critical'),
                'timestamp': datetime.now().isoformat(),
            }
            
            # Send notification for malicious hash
            if self.notification_callback:
                await self.notification_callback(
                    f"Malicious hash detected: {file_hash}",
                    f"Confidence: {result['confidence']}%, Severity: {result['severity']}",
                    'security',
                    result['severity']
                )
            
            return result
            
        return {
            'malicious': False,
            'timestamp': datetime.now().isoformat(),
        }
        
    async def check_url(self, url: str) -> Dict[str, Any]:
        """Check if URL is malicious"""
        if not self.enabled:
            return {'malicious': False, 'reason': 'Threat intel disabled'}
            
        malicious_urls = self.ioc_database.get('malicious_urls', {})
        
        if url in malicious_urls:
            result = {
                'malicious': True,
                'confidence': malicious_urls[url]['confidence'],
                'source': malicious_urls[url]['source'],
                'severity': malicious_urls[url].get('severity', 'high'),
                'timestamp': datetime.now().isoformat(),
            }
            
            # Send notification for malicious URL
            if self.notification_callback:
                await self.notification_callback(
                    f"Malicious URL detected: {url}",
                    f"Confidence: {result['confidence']}%, Severity: {result['severity']}",
                    'security',
                    result['severity']
                )
            
            return result
            
        return {
            'malicious': False,
            'timestamp': datetime.now().isoformat(),
        }
        
    async def add_ioc(self, ioc_type: str, value: str, 
                     source: str = 'manual', confidence: float = 0.5, 
                     severity: str = 'medium') -> bool:
        """Add an indicator of compromise"""
        if ioc_type not in self.ioc_database:
            self.ioc_database[ioc_type] = {}
            
        self.ioc_database[ioc_type][value] = {
            'source': source,
            'confidence': confidence,
            'severity': severity,
            'added': datetime.now().isoformat(),
        }
        
        return True
        
    async def remove_ioc(self, ioc_type: str, value: str) -> bool:
        """Remove an indicator of compromise"""
        if ioc_type in self.ioc_database and value in self.ioc_database[ioc_type]:
            del self.ioc_database[ioc_type][value]
            return True
        return False
        
    async def get_iocs(self, ioc_type: str = None) -> Dict[str, Dict]:
        """Get indicators of compromise"""
        if ioc_type:
            return self.ioc_database.get(ioc_type, {}).copy()
        return self.ioc_database.copy()
        
    async def update_feeds(self) -> bool:
        """Update threat intelligence feeds"""
        # Placeholder for feed updates
        self.last_feed_update = datetime.now().isoformat()
        return True
        
    async def _feed_update_loop(self):
        """Background task to update feeds periodically"""
        while self.enabled:
            try:
                await asyncio.sleep(self.feed_update_interval)
                await self.update_feeds()
            except asyncio.CancelledError:
                break
            except Exception:
                pass
        
    async def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get threat alerts"""
        return self.alerts[-limit:]
        
    async def create_alert(self, alert_type: str, ioc: str, 
                          severity: str = 'medium') -> Dict:
        """Create a threat alert"""
        alert = {
            'type': alert_type,
            'ioc': ioc,
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
        }
        
        self.alerts.append(alert)
        
        # Keep only last 1000 alerts
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
            
        return alert
        
    async def enable(self):
        """Enable threat intel"""
        self.enabled = True
        
    async def disable(self):
        """Disable threat intel"""
        self.enabled = False
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get threat intel statistics"""
        total_iocs = sum(len(db) for db in self.ioc_database.values())
        
        return {
            'enabled': self.enabled,
            'total_iocs': total_iocs,
            'ioc_types': list(self.ioc_database.keys()),
            'alerts_count': len(self.alerts),
            'last_feed_update': self.last_feed_update,
        }
        
    async def export_iocs(self, filepath: str):
        """Export IOC database to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.ioc_database, f, indent=2)
            
    async def import_iocs(self, filepath: str):
        """Import IOC database from JSON file"""
        with open(filepath, 'r') as f:
            self.ioc_database = json.load(f)
