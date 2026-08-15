# ============================================================
#  PLUGIN: AI Detector
#  VERSION: 2.0-ULTRA
#  CLASS: AIDetectorPlugin
#  DESCRIPTION:
#       Advanced AI-based anomaly detection for connections, files,
#       processes, and geolocation events with machine learning,
#       behavioral analysis, and real-time threat detection.
#
#  AUTHOR: Sebastian Januchowski
#  COMPANY: polsoft.ITS™ Dev
# ============================================================

import math
import re
import hashlib
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum

from libs.clean_logger import CleanLogger, LogLevel


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatType(Enum):
    """Threat type classification"""
    UNKNOWN = "unknown"
    MALWARE = "malware"
    PHISHING = "phishing"
    BOTNET = "botnet"
    DDOS = "ddos"
    INTRUSION = "intrusion"
    DATA_EXFILTRATION = "data_exfiltration"
    CRYPTO_MINING = "crypto_mining"
    SOCIAL_ENGINEERING = "social_engineering"
    ADVANCED_PERSISTENT_THREAT = "apt"


@dataclass
class DetectionResult:
    """Detection result"""
    score: float
    risk_level: RiskLevel
    threat_type: ThreatType
    confidence: float
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: str(datetime.now()))


@dataclass
class BehavioralProfile:
    """Behavioral profile for entities"""
    entity_id: str
    connection_patterns: List[Dict] = field(default_factory=list)
    file_patterns: List[Dict] = field(default_factory=list)
    process_patterns: List[Dict] = field(default_factory=list)
    risk_score: float = 0.0
    last_seen: str = field(default_factory=lambda: str(datetime.now()))


class AIDetectorPlugin:
    """
    ADVANCED AI DETECTOR PLUGIN:
    - Machine learning-based anomaly detection
    - Behavioral analysis and profiling
    - Real-time threat detection
    - Geolocation intelligence
    - Pattern recognition
    - Historical analysis
    - Alert system
    """

    def __init__(self):
        self.name = "ai-detector"
        self.version = "2.0-ULTRA"
        self.logger = CleanLogger("AIDetectorPlugin", LogLevel.INFO)
        
        # Behavioral profiles
        self.profiles: Dict[str, BehavioralProfile] = {}
        
        # Historical data
        self.history: deque = deque(maxlen=10000)
        
        # Threat patterns
        self.threat_patterns: Dict[str, List[Dict]] = defaultdict(list)
        
        # Suspicious indicators
        self.suspicious_ips: set = set()
        self.suspicious_domains: set = set()
        self.suspicious_hashes: set = set()
        
        # ML models (simplified - in production would use actual ML)
        self.models = {
            "connection": self._connection_score,
            "file": self._file_score,
            "process": self._process_score,
            "geolocation": self._geolocation_score,
        }
        
        # Configuration
        self.config = {
            "high_risk_threshold": 70.0,
            "medium_risk_threshold": 30.0,
            "enable_behavioral_analysis": True,
            "enable_historical_analysis": True,
            "enable_ml_detection": True,
            "alert_on_critical": True,
        }
        
        # Statistics
        self.stats = {
            "total_detections": 0,
            "high_risk_detections": 0,
            "medium_risk_detections": 0,
            "low_risk_detections": 0,
            "threats_blocked": 0,
        }

    # ============================================================
    # PLUGIN LIFECYCLE
    # ============================================================
    def register(self, engine):
        """Register plugin with engine"""
        self.logger.info(f"AI Detector Plugin v{self.version} registered")
        return self

    def initialize(self, config: Dict[str, Any] = None) -> bool:
        """Initialize plugin"""
        if config:
            self.config.update(config)
        
        self.logger.info("AI Detector Plugin initialized")
        return True

    def start(self) -> bool:
        """Start plugin"""
        self.logger.info("AI Detector Plugin started")
        return True

    def stop(self) -> bool:
        """Stop plugin"""
        self.logger.info("AI Detector Plugin stopped")
        return True

    def cleanup(self) -> bool:
        """Cleanup plugin resources"""
        self.profiles.clear()
        self.history.clear()
        self.logger.info("AI Detector Plugin cleaned up")
        return True

    # ============================================================
    # MAIN PROCESSING
    # ============================================================
    def process(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Process record and detect anomalies"""
        try:
            # Add timestamp if not present
            if "timestamp" not in record:
                record["timestamp"] = str(datetime.now())

            # Calculate base score
            base_score = self._calculate_score(record)
            
            # Apply behavioral analysis
            if self.config["enable_behavioral_analysis"]:
                behavioral_score = self._behavioral_analysis(record)
                base_score += behavioral_score * 0.3
            
            # Apply historical analysis
            if self.config["enable_historical_analysis"]:
                historical_score = self._historical_analysis(record)
                base_score += historical_score * 0.2
            
            # Normalize score
            final_score = min(max(base_score, 0), 100)
            
            # Determine risk level and threat type
            risk_level = self._determine_risk_level(final_score)
            threat_type = self._classify_threat(record, final_score)
            confidence = self._calculate_confidence(record, final_score)
            
            # Create detection result
            result = DetectionResult(
                score=final_score,
                risk_level=risk_level,
                threat_type=threat_type,
                confidence=confidence,
                details=self._extract_details(record),
            )
            
            # Update record
            record["ai_score"] = final_score
            record["ai_risk"] = risk_level.value
            record["ai_threat_type"] = threat_type.value
            record["ai_confidence"] = confidence
            record["ai_details"] = result.details
            
            # Store in history
            self.history.append(record)
            
            # Update statistics
            self.stats["total_detections"] += 1
            if risk_level == RiskLevel.HIGH or risk_level == RiskLevel.CRITICAL:
                self.stats["high_risk_detections"] += 1
            elif risk_level == RiskLevel.MEDIUM:
                self.stats["medium_risk_detections"] += 1
            else:
                self.stats["low_risk_detections"] += 1
            
            # Alert on critical
            if risk_level == RiskLevel.CRITICAL and self.config["alert_on_critical"]:
                self._send_alert(record, result)
            
            return record

        except Exception as e:
            self.logger.error(f"Error processing record: {e}")
            record["ai_score"] = 0
            record["ai_risk"] = "ERROR"
            return record

    # ============================================================
    # SCORE CALCULATION
    # ============================================================
    def _calculate_score(self, record: Dict[str, Any]) -> float:
        """Calculate base anomaly score"""
        record_type = record.get("type", "unknown")
        
        if record_type in self.models:
            return self.models[record_type](record)
        
        return 0.0

    def _connection_score(self, record: Dict[str, Any]) -> float:
        """Calculate connection anomaly score"""
        score = 0.0
        ip = record.get("remote_ip")
        geo = record.get("geo", {})
        
        # Suspicious IP
        if ip in self.suspicious_ips:
            score += 50
        
        # Geolocation analysis
        if geo and geo.get("status") == "success":
            country = geo.get("countryCode", "")
            
            # High-risk countries
            if country in ["RU", "CN", "KP", "IR", "SY"]:
                score += 40
            
            # Unusual location
            if self._is_unusual_location(geo):
                score += 25
            
            # Unknown ASN
            if geo.get("as") is None:
                score += 20
            
            # Tor/VPN indicators
            if self._is_tor_or_vpn(geo):
                score += 30
        
        # Connection status
        status = record.get("status", "")
        if status not in ["ESTABLISHED", "LISTEN", "TIME_WAIT"]:
            score += 15
        
        # Port analysis
        port = record.get("remote_port", 0)
        if self._is_suspicious_port(port):
            score += 20
        
        # Protocol analysis
        protocol = record.get("protocol", "")
        if protocol in ["irc", "torrent", "p2p"]:
            score += 35
        
        return score

    def _file_score(self, record: Dict[str, Any]) -> float:
        """Calculate file anomaly score"""
        score = 0.0
        path = record.get("path", "")
        size = record.get("size", 0)
        
        # Suspicious file extensions
        suspicious_extensions = [".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar"]
        if any(path.lower().endswith(ext) for ext in suspicious_extensions):
            score += 25
        
        # Empty files
        if size == 0:
            score += 10
        
        # Large files
        if size > 100 * 1024 * 1024:  # 100MB
            score += 15
        
        # Suspicious file names
        suspicious_names = ["hack", "crack", "keygen", "patch", "exploit", "payload", "dropper"]
        if any(name in path.lower() for name in suspicious_names):
            score += 40
        
        # Hidden files in unusual locations
        if path.startswith("/.") or path.startswith("C:\\$"):
            score += 30
        
        # Calculate file hash
        file_hash = self._calculate_hash(path)
        if file_hash in self.suspicious_hashes:
            score += 60
        
        # File entropy (potential encryption/packing)
        if self._calculate_entropy(path) > 7.5:
            score += 35
        
        return score

    def _process_score(self, record: Dict[str, Any]) -> float:
        """Calculate process anomaly score"""
        score = 0.0
        name = record.get("name", "").lower()
        pid = record.get("pid", 0)
        
        # Suspicious process names
        suspicious_processes = ["hack", "miner", "bot", "crypt", "steal", "inject", "hook"]
        if any(proc in name for proc in suspicious_processes):
            score += 50
        
        # System processes with unusual paths
        if name in ["svchost", "explorer", "lsass"] and not self._is_system_path(record.get("path", "")):
            score += 45
        
        # High resource usage
        cpu = record.get("cpu_percent", 0)
        memory = record.get("memory_percent", 0)
        if cpu > 80 or memory > 80:
            score += 20
        
        # Unusual parent process
        parent_pid = record.get("parent_pid", 0)
        if parent_pid == 0 or parent_pid == 1:
            score += 30
        
        # Network activity from unusual processes
        if record.get("has_network", False) and name not in ["chrome", "firefox", "edge", "opera"]:
            score += 25
        
        return score

    def _geolocation_score(self, record: Dict[str, Any]) -> float:
        """Calculate geolocation anomaly score"""
        score = 0.0
        geo = record.get("geo", {})
        
        if not geo or geo.get("status") != "success":
            return 15.0  # Penalty for missing geo data
        
        # Rapid location changes
        if self._detect_rapid_location_change(geo):
            score += 50
        
        # Impossible travel
        if self._detect_impossible_travel(geo):
            score += 60
        
        # Unusual time patterns
        if self._detect_unusual_timing(record):
            score += 25
        
        return score

    # ============================================================
    # BEHAVIORAL ANALYSIS
    # ============================================================
    def _behavioral_analysis(self, record: Dict[str, Any]) -> float:
        """Perform behavioral analysis"""
        score = 0.0
        entity_id = self._get_entity_id(record)
        
        # Get or create profile
        if entity_id not in self.profiles:
            self.profiles[entity_id] = BehavioralProfile(entity_id=entity_id)
        
        profile = self.profiles[entity_id]
        
        # Update profile
        self._update_profile(profile, record)
        
        # Analyze patterns
        if self._detect_anomalous_pattern(profile):
            score += 40
        
        # Check for escalation
        if self._detect_privilege_escalation(profile):
            score += 50
        
        # Check for lateral movement
        if self._detect_lateral_movement(profile):
            score += 45
        
        return score

    # ============================================================
    # HISTORICAL ANALYSIS
    # ============================================================
    def _historical_analysis(self, record: Dict[str, Any]) -> float:
        """Perform historical analysis"""
        score = 0.0
        
        # Check for similar past events
        similar_events = self._find_similar_events(record)
        
        # If similar high-risk events occurred recently
        if similar_events and len(similar_events) > 5:
            score += 30
        
        # Check for first-time occurrence
        if not self._has_occurred_before(record):
            score += 20
        
        # Check for frequency spikes
        if self._detect_frequency_spike(record):
            score += 35
        
        return score

    # ============================================================
    # THREAT CLASSIFICATION
    # ============================================================
    def _classify_threat(self, record: Dict[str, Any], score: float) -> ThreatType:
        """Classify threat type"""
        record_type = record.get("type", "")
        
        if score >= 80:
            if record_type == "connection":
                return ThreatType.INTRUSION
            elif record_type == "file":
                return ThreatType.MALWARE
            elif record_type == "process":
                return ThreatType.CRYPTO_MINING
        
        if score >= 60:
            if "miner" in record.get("name", "").lower():
                return ThreatType.CRYPTO_MINING
            elif "bot" in record.get("name", "").lower():
                return ThreatType.BOTNET
        
        return ThreatType.UNKNOWN

    # ============================================================
    # UTILITY METHODS
    # ============================================================
    def _determine_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level from score"""
        if score >= self.config["high_risk_threshold"]:
            return RiskLevel.HIGH
        if score >= self.config["medium_risk_threshold"]:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _calculate_confidence(self, record: Dict[str, Any], score: float) -> float:
        """Calculate detection confidence"""
        # More data points = higher confidence
        confidence = min(score / 100 + 0.1, 0.95)
        
        # Adjust based on data quality
        if record.get("geo", {}).get("status") != "success":
            confidence -= 0.2
        
        return max(confidence, 0.0)

    def _extract_details(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Extract detection details"""
        return {
            "type": record.get("type"),
            "timestamp": record.get("timestamp"),
            "indicators": self._get_indicators(record),
            "patterns": self._get_patterns(record),
        }

    def _get_entity_id(self, record: Dict[str, Any]) -> str:
        """Get entity identifier for profiling"""
        record_type = record.get("type", "")
        if record_type == "connection":
            return record.get("remote_ip", "unknown")
        elif record_type == "process":
            return record.get("name", "unknown")
        elif record_type == "file":
            return record.get("path", "unknown")
        return "unknown"

    def _update_profile(self, profile: BehavioralProfile, record: Dict[str, Any]) -> None:
        """Update behavioral profile"""
        record_type = record.get("type", "")
        
        if record_type == "connection":
            profile.connection_patterns.append(record)
        elif record_type == "file":
            profile.file_patterns.append(record)
        elif record_type == "process":
            profile.process_patterns.append(record)
        
        profile.last_seen = str(datetime.now())

    def _is_unusual_location(self, geo: Dict[str, Any]) -> bool:
        """Check if location is unusual"""
        # Simplified - in production would use historical data
        return False

    def _is_tor_or_vpn(self, geo: Dict[str, Any]) -> bool:
        """Check if connection is from Tor/VPN"""
        # Simplified - in production would use Tor/VPN databases
        return False

    def _is_suspicious_port(self, port: int) -> bool:
        """Check if port is suspicious"""
        suspicious_ports = [6666, 6667, 6668, 6669, 31337, 12345, 54321, 445]
        return port in suspicious_ports

    def _calculate_hash(self, path: str) -> str:
        """Calculate file hash"""
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return ""

    def _calculate_entropy(self, path: str) -> float:
        """Calculate file entropy"""
        try:
            with open(path, "rb") as f:
                data = f.read(4096)  # Sample first 4KB
                if not data:
                    return 0.0
                
                # Calculate Shannon entropy
                byte_counts = [0] * 256
                for byte in data:
                    byte_counts[byte] += 1
                
                entropy = 0.0
                for count in byte_counts:
                    if count > 0:
                        probability = count / len(data)
                        entropy -= probability * math.log2(probability)
                
                return entropy
        except:
            return 0.0

    def _is_system_path(self, path: str) -> bool:
        """Check if path is system path"""
        system_paths = [
            "C:\\Windows\\System32",
            "C:\\Windows\\SysWOW64",
            "/usr/bin",
            "/usr/sbin",
            "/bin",
            "/sbin",
        ]
        return any(path.startswith(sys_path) for sys_path in system_paths)

    def _detect_rapid_location_change(self, geo: Dict[str, Any]) -> bool:
        """Detect rapid location changes"""
        # Simplified - would use historical geo data
        return False

    def _detect_impossible_travel(self, geo: Dict[str, Any]) -> bool:
        """Detect impossible travel"""
        # Simplified - would use timing and distance analysis
        return False

    def _detect_unusual_timing(self, record: Dict[str, Any]) -> bool:
        """Detect unusual timing patterns"""
        # Simplified - would use time series analysis
        return False

    def _detect_anomalous_pattern(self, profile: BehavioralProfile) -> bool:
        """Detect anomalous behavioral patterns"""
        # Simplified - would use ML pattern recognition
        return False

    def _detect_privilege_escalation(self, profile: BehavioralProfile) -> bool:
        """Detect privilege escalation"""
        # Simplified - would analyze permission changes
        return False

    def _detect_lateral_movement(self, profile: BehavioralProfile) -> bool:
        """Detect lateral movement"""
        # Simplified - would analyze connection patterns
        return False

    def _find_similar_events(self, record: Dict[str, Any]) -> List[Dict]:
        """Find similar historical events"""
        # Simplified - would use similarity algorithms
        return []

    def _has_occurred_before(self, record: Dict[str, Any]) -> bool:
        """Check if event has occurred before"""
        # Simplified - would use pattern matching
        return False

    def _detect_frequency_spike(self, record: Dict[str, Any]) -> bool:
        """Detect frequency spikes"""
        # Simplified - would use frequency analysis
        return False

    def _get_indicators(self, record: Dict[str, Any]) -> List[str]:
        """Get threat indicators"""
        indicators = []
        
        if record.get("remote_ip") in self.suspicious_ips:
            indicators.append("suspicious_ip")
        
        if record.get("path", "").endswith(".exe"):
            indicators.append("executable")
        
        return indicators

    def _get_patterns(self, record: Dict[str, Any]) -> List[str]:
        """Get threat patterns"""
        patterns = []
        
        if record.get("type") == "connection":
            patterns.append("network_activity")
        
        return patterns

    def _send_alert(self, record: Dict[str, Any], result: DetectionResult) -> None:
        """Send security alert"""
        self.logger.warning(f"CRITICAL THREAT DETECTED: {result.threat_type.value} - Score: {result.score}")

    # ============================================================
    # PLUGIN API
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get plugin metadata"""
        return {
            "name": self.name,
            "version": self.version,
            "author": "Sebastian Januchowski",
            "company": "polsoft.ITS™ Dev",
            "description": "Advanced AI-based anomaly detection with ML and behavioral analysis",
            "dependencies": [],
            "compatibility": {
                "min_version": "2.5.0",
                "max_version": "3.0.0",
            },
            "api_methods": ["process", "get_stats", "get_config", "set_config"],
            "plugins": [],
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get plugin statistics"""
        return self.stats

    def get_config(self) -> Dict[str, Any]:
        """Get plugin configuration"""
        return self.config

    def set_config(self, key: str, value: Any) -> bool:
        """Set plugin configuration"""
        if key in self.config:
            self.config[key] = value
            self.logger.info(f"Config updated: {key} = {value}")
            return True
        return False

    def diagnose(self) -> Dict[str, Any]:
        """Run plugin diagnostics"""
        return {
            "status": "healthy",
            "profiles_count": len(self.profiles),
            "history_size": len(self.history),
            "suspicious_ips": len(self.suspicious_ips),
            "suspicious_hashes": len(self.suspicious_hashes),
        }

    def auto_fix(self) -> bool:
        """Run auto-fix"""
        # Clear old profiles
        cutoff = datetime.now() - timedelta(days=7)
        self.profiles = {
            k: v for k, v in self.profiles.items()
            if datetime.fromisoformat(v.last_seen) > cutoff
        }
        self.logger.info("Auto-fix executed: cleaned old profiles")
        return True
