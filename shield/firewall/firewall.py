"""
 ============================================================
  MODULE/PLUGIN NAME: Firewall
  VERSION: 1.0.0
  MODULE CLASS: Firewall
  DESCRIPTION:
       Network firewall protection for TerminalX security

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
from typing import Dict, Any, List, Set, Optional
from ipaddress import ip_network, ip_address
from datetime import datetime
from enum import Enum


class RuleAction(Enum):
    """Firewall rule actions"""
    ALLOW = "allow"
    BLOCK = "block"
    LOG = "log"


class RuleDirection(Enum):
    """Rule direction"""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BOTH = "both"


class Firewall:
    """Network firewall"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.rules: List[Dict] = []
        self.blocked_ips: Set[str] = set()
        self.allowed_ips: Set[str] = set()
        self.blocked_ports: Set[int] = set()
        self.allowed_ports: Set[int] = set()
        self.blocked_domains: Set[str] = set()
        self.log: List[Dict] = []
        self.default_policy = "allow"  # allow or block
        self.notification_callback = None
        self.connection_stats = {
            'total_checks': 0,
            'allowed': 0,
            'blocked': 0,
        }
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize firewall"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.default_policy = self.config.get('default_policy', 'allow')
        
        # Load default rules
        self.blocked_ips = set(self.config.get('blocked_ips', []))
        self.allowed_ips = set(self.config.get('allowed_ips', []))
        self.blocked_ports = set(self.config.get('blocked_ports', []))
        self.allowed_ports = set(self.config.get('allowed_ports', []))
        self.blocked_domains = set(self.config.get('blocked_domains', []))
        
    def set_notification_callback(self, callback):
        """Set callback for firewall notifications"""
        self.notification_callback = callback
        
    async def add_rule(self, rule: Dict[str, Any]) -> bool:
        """Add a firewall rule"""
        rule['id'] = f"rule_{len(self.rules)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        rule['created'] = datetime.now().isoformat()
        rule['enabled'] = rule.get('enabled', True)
        
        # Validate rule
        if 'action' not in rule:
            rule['action'] = RuleAction.BLOCK.value
        
        if 'direction' not in rule:
            rule['direction'] = RuleDirection.BOTH.value
            
        self.rules.append(rule)
        return True
        
    async def remove_rule(self, rule_id: str) -> bool:
        """Remove a firewall rule"""
        for i, rule in enumerate(self.rules):
            if rule['id'] == rule_id:
                self.rules.pop(i)
                return True
        return False
        
    async def block_ip(self, ip: str) -> bool:
        """Block an IP address"""
        try:
            ip_address(ip)  # Validate IP
            self.blocked_ips.add(ip)
            
            # Send notification
            if self.notification_callback:
                await self.notification_callback(
                    f"IP blocked: {ip}",
                    f"IP address {ip} has been added to blocklist",
                    'security',
                    'high'
                )
            return True
        except ValueError:
            return False
            
    async def unblock_ip(self, ip: str) -> bool:
        """Unblock an IP address"""
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            return True
        return False
            
    async def allow_ip(self, ip: str) -> bool:
        """Allow an IP address"""
        try:
            ip_address(ip)  # Validate IP
            self.allowed_ips.add(ip)
            return True
        except ValueError:
            return False
            
    async def block_domain(self, domain: str) -> bool:
        """Block a domain"""
        if domain:
            self.blocked_domains.add(domain.lower())
            return True
        return False
        
    async def unblock_domain(self, domain: str) -> bool:
        """Unblock a domain"""
        domain_lower = domain.lower()
        if domain_lower in self.blocked_domains:
            self.blocked_domains.remove(domain_lower)
            return True
        return False
            
    async def block_port(self, port: int) -> bool:
        """Block a port"""
        if 0 <= port <= 65535:
            self.blocked_ports.add(port)
            return True
        return False
            
    async def unblock_port(self, port: int) -> bool:
        """Unblock a port"""
        if port in self.blocked_ports:
            self.blocked_ports.remove(port)
            return True
        return False
        
    async def allow_port(self, port: int) -> bool:
        """Allow a port"""
        if 0 <= port <= 65535:
            self.allowed_ports.add(port)
            return True
        return False
            
    async def check_connection(self, source_ip: str, dest_ip: str, 
                              dest_port: int, dest_domain: str = None) -> Dict[str, Any]:
        """Check if connection is allowed"""
        self.connection_stats['total_checks'] += 1
        
        result = {
            'allowed': True,
            'reason': 'default_allow',
            'timestamp': datetime.now().isoformat(),
        }
        
        if not self.enabled:
            result['reason'] = 'firewall_disabled'
            self.connection_stats['allowed'] += 1
            return result
            
        # Check blocked IPs
        if source_ip in self.blocked_ips or dest_ip in self.blocked_ips:
            result['allowed'] = False
            result['reason'] = 'blocked_ip'
            self.connection_stats['blocked'] += 1
            
            # Send notification for blocked connection
            if self.notification_callback:
                await self.notification_callback(
                    f"Connection blocked: {source_ip} -> {dest_ip}:{dest_port}",
                    f"Blocked IP detected in connection attempt",
                    'network',
                    'high'
                )
            
        # Check blocked domains
        if dest_domain and dest_domain.lower() in self.blocked_domains:
            result['allowed'] = False
            result['reason'] = 'blocked_domain'
            self.connection_stats['blocked'] += 1
            
        # Check blocked ports
        if dest_port in self.blocked_ports:
            result['allowed'] = False
            result['reason'] = 'blocked_port'
            self.connection_stats['blocked'] += 1
            
        # Check allowed list (if configured)
        if self.allowed_ips and dest_ip not in self.allowed_ips:
            result['allowed'] = False
            result['reason'] = 'not_allowed_ip'
            self.connection_stats['blocked'] += 1
            
        if self.allowed_ports and dest_port not in self.allowed_ports:
            result['allowed'] = False
            result['reason'] = 'not_allowed_port'
            self.connection_stats['blocked'] += 1
            
        # Check custom rules
        for rule in self.rules:
            if not rule.get('enabled', True):
                continue
                
            rule_match = False
            
            # Check IP match
            if 'source_ip' in rule and rule['source_ip'] == source_ip:
                rule_match = True
            if 'dest_ip' in rule and rule['dest_ip'] == dest_ip:
                rule_match = True
            if 'dest_port' in rule and rule['dest_port'] == dest_port:
                rule_match = True
                
            if rule_match:
                if rule['action'] == RuleAction.BLOCK.value:
                    result['allowed'] = False
                    result['reason'] = f"rule_{rule['id']}"
                    self.connection_stats['blocked'] += 1
                elif rule['action'] == RuleAction.ALLOW.value:
                    result['allowed'] = True
                    result['reason'] = f"rule_{rule['id']}"
                    self.connection_stats['allowed'] += 1
                    
        if result['allowed']:
            self.connection_stats['allowed'] += 1
            
        # Log the check
        self.log.append({
            'source_ip': source_ip,
            'dest_ip': dest_ip,
            'dest_port': dest_port,
            'dest_domain': dest_domain,
            'allowed': result['allowed'],
            'reason': result['reason'],
            'timestamp': result['timestamp'],
        })
        
        # Keep only last 1000 log entries
        if len(self.log) > 1000:
            self.log = self.log[-1000:]
            
        return result
        
    async def get_rules(self) -> List[Dict]:
        """Get all firewall rules"""
        return self.rules.copy()
        
    async def get_log(self, limit: int = 100) -> List[Dict]:
        """Get firewall log"""
        return self.log[-limit:]
        
    async def get_blocked_ips(self) -> Set[str]:
        """Get blocked IPs"""
        return self.blocked_ips.copy()
        
    async def get_allowed_ips(self) -> Set[str]:
        """Get allowed IPs"""
        return self.allowed_ips.copy()
        
    async def get_blocked_ports(self) -> Set[int]:
        """Get blocked ports"""
        return self.blocked_ports.copy()
        
    async def get_allowed_ports(self) -> Set[int]:
        """Get allowed ports"""
        return self.allowed_ports.copy()
        
    async def get_blocked_domains(self) -> Set[str]:
        """Get blocked domains"""
        return self.blocked_domains.copy()
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get firewall statistics"""
        return {
            'enabled': self.enabled,
            'default_policy': self.default_policy,
            'rules_count': len(self.rules),
            'blocked_ips_count': len(self.blocked_ips),
            'allowed_ips_count': len(self.allowed_ips),
            'blocked_ports_count': len(self.blocked_ports),
            'allowed_ports_count': len(self.allowed_ports),
            'blocked_domains_count': len(self.blocked_domains),
            'log_entries': len(self.log),
            'connection_stats': self.connection_stats.copy(),
        }
        
    async def enable(self):
        """Enable firewall"""
        self.enabled = True
        
    async def disable(self):
        """Disable firewall"""
        self.enabled = False
        
    async def set_default_policy(self, policy: str) -> bool:
        """Set default policy (allow or block)"""
        if policy in ['allow', 'block']:
            self.default_policy = policy
            return True
        return False
